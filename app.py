"""CampusFind: a campus lost-and-found web application."""
import math
import os
import re
import sqlite3
from datetime import date, datetime, timezone
from functools import wraps

from flask import (
    Flask, abort, flash, g, jsonify, redirect, render_template, request, session, url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import get_config
from database.init_db import connect, db_path_from_url, init_db

CATEGORIES = ["electronics", "bags", "stationery", "clothing", "keys", "accessories", "other"]
ITEM_TYPES = ["lost", "found"]
STATUSES = ["open", "claimed", "resolved"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")


# ---------------------------------------------------------------- database

def get_db():
    if "db" not in g:
        from flask import current_app
        g.db = connect(current_app.config["DB_PATH"])
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ---------------------------------------------------------------- helpers

def current_user():
    uid = session.get("user_id")
    if uid is None:
        return None
    return get_db().execute("SELECT id, username, email FROM users WHERE id = ?", (uid,)).fetchone()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def get_item_or_404(item_id):
    item = get_db().execute(
        "SELECT items.*, users.username AS owner_name FROM items "
        "LEFT JOIN users ON users.id = items.user_id WHERE items.id = ?",
        (item_id,),
    ).fetchone()
    if item is None:
        abort(404)
    return item


def get_owned_item(item_id):
    item = get_item_or_404(item_id)
    if item["user_id"] != session.get("user_id"):
        abort(403)
    return item


def validate_item(form):
    """Return (clean_data, errors) for an item form."""
    data = {k: (form.get(k) or "").strip() for k in
            ("title", "description", "category", "item_type", "location", "item_date",
             "image_url", "contact_email")}
    errors = []
    if not 3 <= len(data["title"]) <= 100:
        errors.append("Title must be between 3 and 100 characters.")
    if not 10 <= len(data["description"]) <= 1000:
        errors.append("Description must be between 10 and 1000 characters.")
    if data["category"] not in CATEGORIES:
        errors.append("Please choose a valid category.")
    if data["item_type"] not in ITEM_TYPES:
        errors.append("Item type must be 'lost' or 'found'.")
    if not 2 <= len(data["location"]) <= 150:
        errors.append("Location must be between 2 and 150 characters.")
    try:
        parsed = date.fromisoformat(data["item_date"])
        if parsed > date.today():
            errors.append("Date cannot be in the future.")
    except ValueError:
        errors.append("Please enter a valid date (YYYY-MM-DD).")
    if not EMAIL_RE.match(data["contact_email"]):
        errors.append("Please enter a valid contact email.")
    if data["image_url"]:
        if not data["image_url"].startswith(("http://", "https://")) or len(data["image_url"]) > 500:
            errors.append("Image URL must start with http:// or https://.")
    else:
        data["image_url"] = None
    return data, errors


# ---------------------------------------------------------------- factory

def create_app(config_name=None, overrides=None):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    if overrides:
        app.config.update(overrides)
    app.config["DB_PATH"] = db_path_from_url(app.config["DATABASE_URL"])

    with app.app_context():
        conn = connect(app.config["DB_PATH"])
        init_db(conn)
        conn.close()

    app.teardown_appcontext(close_db)

    @app.context_processor
    def inject_globals():
        return {
            "user": current_user(),
            "CATEGORIES": CATEGORIES,
            "ITEM_TYPES": ITEM_TYPES,
            "STATUSES": STATUSES,
            "today": date.today().isoformat(),
            "version": app.config["VERSION"],
        }

    # ------------------------------------------------------------ home

    @app.route("/")
    def index():
        db = get_db()
        stats = db.execute(
            "SELECT COUNT(*) AS total, "
            "COALESCE(SUM(item_type = 'lost'), 0) AS lost, "
            "COALESCE(SUM(item_type = 'found'), 0) AS found, "
            "COALESCE(SUM(status = 'resolved'), 0) AS resolved FROM items"
        ).fetchone()

        q = request.args.get("q", "").strip()
        category = request.args.get("category", "")
        item_type = request.args.get("type", "")
        status = request.args.get("status", "")

        clauses, params = [], []
        if q:
            clauses.append("(title LIKE ? OR description LIKE ? OR location LIKE ?)")
            like = f"%{q}%"
            params += [like, like, like]
        if category in CATEGORIES:
            clauses.append("category = ?")
            params.append(category)
        if item_type in ITEM_TYPES:
            clauses.append("item_type = ?")
            params.append(item_type)
        if status in STATUSES:
            clauses.append("status = ?")
            params.append(status)
        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""

        count = db.execute(f"SELECT COUNT(*) FROM items{where}", params).fetchone()[0]
        per_page = app.config["ITEMS_PER_PAGE"]
        pages = max(1, math.ceil(count / per_page))
        page = min(max(request.args.get("page", 1, type=int), 1), pages)
        items = db.execute(
            f"SELECT * FROM items{where} ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?",
            params + [per_page, (page - 1) * per_page],
        ).fetchall()

        filters = {"q": q, "category": category, "type": item_type, "status": status}
        return render_template(
            "index.html", stats=stats, items=items, filters=filters,
            page=page, pages=pages, result_count=count,
            filtered=any(filters.values()),
        )

    # ------------------------------------------------------------ auth

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            confirm = request.form.get("confirm_password", "")
            errors = []
            if not USERNAME_RE.match(username):
                errors.append("Username must be 3-30 characters (letters, numbers, . _ -).")
            if not EMAIL_RE.match(email):
                errors.append("Please enter a valid email address.")
            if len(password) < 8:
                errors.append("Password must be at least 8 characters.")
            if password != confirm:
                errors.append("Passwords do not match.")
            db = get_db()
            if not errors and db.execute(
                "SELECT 1 FROM users WHERE username = ? OR email = ?", (username, email)
            ).fetchone():
                errors.append("That username or email is already registered.")
            if errors:
                for e in errors:
                    flash(e, "error")
                return render_template("register.html", form=request.form), 400
            cur = db.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, generate_password_hash(password)),
            )
            db.commit()
            session.clear()
            session["user_id"] = cur.lastrowid
            flash(f"Welcome to CampusFind, {username}!", "success")
            return redirect(url_for("index"))
        return render_template("register.html", form={})

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            identifier = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            row = get_db().execute(
                "SELECT * FROM users WHERE lower(email) = ? OR lower(username) = ?",
                (identifier, identifier),
            ).fetchone()
            if row is None or not check_password_hash(row["password_hash"], password):
                flash("Invalid email or password.", "error")
                return render_template("login.html", form=request.form), 401
            session.clear()
            session["user_id"] = row["id"]
            flash(f"Logged in as {row['username']}.", "success")
            nxt = request.args.get("next", "")
            # Only allow local redirects to avoid open-redirect abuse.
            if nxt.startswith("/") and not nxt.startswith("//"):
                return redirect(nxt)
            return redirect(url_for("index"))
        return render_template("login.html", form={})

    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been logged out.", "success")
        return redirect(url_for("index"))

    # ------------------------------------------------------------ items

    @app.route("/items/new", methods=["GET", "POST"])
    @login_required
    def new_item():
        if request.method == "POST":
            data, errors = validate_item(request.form)
            if errors:
                for e in errors:
                    flash(e, "error")
                return render_template("report_item.html", form=request.form), 400
            db = get_db()
            cur = db.execute(
                "INSERT INTO items (user_id, title, description, category, item_type, location, "
                "item_date, image_url, contact_email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (session["user_id"], data["title"], data["description"], data["category"],
                 data["item_type"], data["location"], data["item_date"], data["image_url"],
                 data["contact_email"]),
            )
            db.commit()
            flash("Item reported successfully.", "success")
            return redirect(url_for("item_detail", item_id=cur.lastrowid))
        return render_template("report_item.html", form={"contact_email": current_user()["email"]})

    @app.route("/items/<int:item_id>")
    def item_detail(item_id):
        item = get_item_or_404(item_id)
        is_owner = item["user_id"] is not None and item["user_id"] == session.get("user_id")
        return render_template("item_detail.html", item=item, is_owner=is_owner)

    @app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_item(item_id):
        item = get_owned_item(item_id)
        if request.method == "POST":
            data, errors = validate_item(request.form)
            status = request.form.get("status", item["status"])
            if status not in STATUSES:
                errors.append("Invalid status.")
            if errors:
                for e in errors:
                    flash(e, "error")
                return render_template("edit_item.html", item=item, form=request.form), 400
            db = get_db()
            db.execute(
                "UPDATE items SET title = ?, description = ?, category = ?, item_type = ?, "
                "location = ?, item_date = ?, image_url = ?, contact_email = ?, status = ?, "
                "updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (data["title"], data["description"], data["category"], data["item_type"],
                 data["location"], data["item_date"], data["image_url"], data["contact_email"],
                 status, item_id),
            )
            db.commit()
            flash("Item updated.", "success")
            return redirect(url_for("item_detail", item_id=item_id))
        return render_template("edit_item.html", item=item, form=dict(item))

    @app.route("/items/<int:item_id>/status", methods=["POST"])
    @login_required
    def update_status(item_id):
        get_owned_item(item_id)
        status = request.form.get("status", "")
        if status not in STATUSES:
            flash("Invalid status.", "error")
            return redirect(url_for("item_detail", item_id=item_id))
        db = get_db()
        db.execute(
            "UPDATE items SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, item_id),
        )
        db.commit()
        flash(f"Status changed to {status}.", "success")
        return redirect(url_for("item_detail", item_id=item_id))

    @app.route("/items/<int:item_id>/delete", methods=["POST"])
    @login_required
    def delete_item(item_id):
        get_owned_item(item_id)
        db = get_db()
        db.execute("DELETE FROM items WHERE id = ?", (item_id,))
        db.commit()
        flash("Item deleted.", "success")
        return redirect(url_for("index"))

    # ------------------------------------------------------------ health

    @app.route("/health")
    def health():
        try:
            get_db().execute("SELECT 1").fetchone()
        except Exception as exc:  # any DB failure means unhealthy
            return jsonify(status="unhealthy", database="disconnected", error=str(exc)), 503
        return jsonify(
            status="healthy", database="connected",
            timestamp=datetime.now(timezone.utc).isoformat(),
            version=app.config["VERSION"],
        ), 200

    # ------------------------------------------------------------ errors

    @app.errorhandler(403)
    def forbidden(_e):
        return render_template("error.html", code=403,
                               message="You do not have permission to do that."), 403

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("error.html", code=404,
                               message="The page or item you requested does not exist."), 404

    @app.errorhandler(500)
    def server_error(_e):
        return render_template("error.html", code=500,
                               message="Something went wrong on our side."), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["PORT"], debug=app.config["DEBUG"])
