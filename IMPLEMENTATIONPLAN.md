# Agent Execution Directive: Build CampusFind (DevOps Mini-Project)

> **Role & Persona:** You are an expert Principal Full-Stack Engineer and Senior DevOps Architect.
> **Objective:** Build, test, containerize, and configure the complete end-to-end repository for **CampusFind**, a production-grade lost-and-found web application featuring an automated CI/CD and DevSecOps pipeline.
> **Target Audience:** College DevOps Lab Mini-Project (practical demonstration for faculty evaluation).
> **Execution Standard:** Zero placeholders, zero TODOs, zero pseudocode, zero mock data files. Every single file must be complete, syntactically valid, mutually consistent, and fully functional.

---

## 1. Non-Negotiable System Constraints & Rules

1. **Self-Contained & Deterministic:** Everything must run from a clean clone without requiring paid API keys or proprietary third-party SaaS beyond standard free-tier GitHub and container hosting.
2. **DevOps First:** While the web app must be polished, responsive, and robust, the primary grading criteria is the **complete automated CI/CD and DevSecOps pipeline**.
3. **Database Portability:** Support local development and isolated testing using **SQLite** (`sqlite:///campusfind.db` or in-memory), with seamless production support for **PostgreSQL** or persistent SQLite volume mount via the `DATABASE_URL` environment variable.
4. **Security by Design:**
   - Parameterized queries / ORM only (zero raw SQL string concatenation).
   - Session-based authentication with `Werkzeug` secure password hashing (`generate_password_hash`, `check_password_hash`).
   - Auto-escaped Jinja2 templates (prevent XSS).
   - Container runs strictly as an unprivileged non-root user (`appuser`, UID 10001).
   - Automated Trivy vulnerability scanning blocking releases on High/Critical findings.
5. **No Broken Links / No Dead Buttons:** All forms, filters, badges, modal dialogs, and navigation links must work with actual backend endpoints and real database records.

---

## 2. Target Project File Structure

You must implement every file listed below:

```text
campusfind/
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # Complete 5-stage GitHub Actions CI/CD/DevSecOps pipeline
├── database/
│   ├── init_db.py                # Schema initialization & table creation script
│   └── schema.sql                # Raw SQL schema definition (DDL)
├── static/
│   ├── css/
│   │   └── style.css             # Polished, modern CSS (responsive, CSS custom properties, cards, badges)
│   └── js/
│       └── main.js               # Dynamic client-side UI (live filter toggle, flash message dismiss, confirmation dialogs)
├── templates/
│   ├── base.html                 # Master layout (navbar, flash alerts, footer, responsive meta)
│   ├── index.html                # Landing page + statistics counters + item card grid + search/filters
│   ├── report_item.html          # Form to report a Lost or Found item
│   ├── item_detail.html          # Detailed view of an item with owner action controls
│   ├── edit_item.html            # Edit form for item owner
│   ├── login.html                # User login form
│   └── register.html             # User registration form
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures: isolated test app, temporary DB, authenticated client
│   ├── test_home.py              # Home route, stats calculation, and empty state tests
│   ├── test_items.py             # CRUD operations, ownership authorization, state transitions
│   ├── test_validation.py        # Input boundary validation, SQL injection safety, invalid types
│   └── test_health.py            # /health endpoint under normal and degraded/failed DB conditions
├── scripts/
│   ├── seed_demo_data.py         # Populates 10-12 diverse, realistic lost & found sample records
│   └── smoke_test.py             # Post-deployment HTTP verification script with configurable URL
├── .dockerignore                 # Excludes .git, venv, pycache, tests, local .db, secrets
├── .gitignore                    # Standard Python, IDE, OS, and local database exclusions
├── Dockerfile                    # Multi-stage/slim secure containerfile with Gunicorn & non-root user
├── config.py                     # Environment-driven config (Development, Testing, Production)
├── app.py                        # Main Flask application factory, routes, and error handlers
├── requirements.txt              # Pinned production and test dependencies
├── pytest.ini                    # Pytest configuration flags and test path discovery
└── README.md                     # Comprehensive faculty-ready documentation, architecture, & demo guide
```

---

## 3. Detailed Component Specifications

### 3.1. Database Schema (`database/schema.sql`)

Create tables with appropriate constraints:

1. **`users` Table:**
   - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
   - `username`: TEXT UNIQUE NOT NULL
   - `email`: TEXT UNIQUE NOT NULL
   - `password_hash`: TEXT NOT NULL
   - `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

2. **`items` Table:**
   - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
   - `user_id`: INTEGER REFERENCES users(id) ON DELETE CASCADE
   - `title`: TEXT NOT NULL (Length: 3 to 100 characters)
   - `description`: TEXT NOT NULL (Length: 10 to 1000 characters)
   - `category`: TEXT NOT NULL (Restricted to: `'electronics'`, `'bags'`, `'stationery'`, `'clothing'`, `'keys'`, `'accessories'`, `'other'`)
   - `item_type`: TEXT NOT NULL (Restricted to: `'lost'`, `'found'`)
   - `location`: TEXT NOT NULL
   - `item_date`: DATE NOT NULL
   - `image_url`: TEXT NULL
   - `contact_email`: TEXT NOT NULL
   - `status`: TEXT NOT NULL DEFAULT `'open'` (Restricted to: `'open'`, `'claimed'`, `'resolved'`)
   - `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   - `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### 3.2. Application Architecture & Endpoints (`app.py`)

- **Configuration:** Reads `SECRET_KEY`, `DATABASE_URL`, `PORT`, `FLASK_ENV` from environment with secure defaults for development.
- **Routes to implement:**
  - `GET /`: Landing dashboard with summary metrics (`total`, `lost`, `found`, `resolved`), search query (`q`), filter by `category`, `type`, and `status`. Displays paginated or clean card list. Gracefully handles 0 items with an attractive empty-state illustration/banner.
  - `GET, POST /register`: Student registration with password hashing.
  - `GET, POST /login`: Authentication creating a session cookie.
  - `GET /logout`: Clears session.
  - `GET, POST /items/new`: Create listing (requires login). Validates all inputs.
  - `GET /items/<int:item_id>`: Detail page showing item metadata, status badge, and contact info. Shows Edit/Delete/Change Status buttons only if logged in as the owner.
  - `GET, POST /items/<int:item_id>/edit`: Edit listing (owner-only authorization).
  - `POST /items/<int:item_id>/status`: Quick status update endpoint (owner-only).
  - `POST /items/<int:item_id>/delete`: Delete listing (owner-only authorization).
  - `GET /health`: **Health Check Endpoint**
    - Executes a quick DB query (e.g., `SELECT 1`).
    - On success: returns HTTP 200 JSON `{"status": "healthy", "database": "connected", "timestamp": "...", "version": "1.0.0"}`.
    - On database failure: returns HTTP 503 JSON `{"status": "unhealthy", "database": "disconnected", "error": "..."}`.

### 3.3. Frontend & Styling (`templates/` & `static/`)

- Use modern semantic HTML5 with Vanilla CSS (CSS Grid, Flexbox, custom color tokens).
- Distinct color-coded status badges:
  - `open`: Amber / Indigo
  - `claimed`: Blue
  - `resolved`: Emerald Green
  - `lost`: Crimson Red
  - `found`: Teal
- Interactive search and filter bar that submits cleanly via GET parameters and retains active filter states in the UI.
- Flash alert banners (success, error, warning) with close buttons.
- Fully mobile-responsive navbar with accessible hamburger/collapsible menu.

### 3.4. Seed & Utilities (`scripts/seed_demo_data.py`)

- Must populate at least 1 default demo user (`demo@campus.edu` / `DemoPassword123!`) and 10+ realistic records (e.g., "Blue Hydro Flask in Library 2nd Floor", "Sony WH-1000XM4 Headphones near Cafeteria", "TI-84 Plus Calculator in Room 302", "Dorm Room Keys on Red Lanyard").
- Mix of statuses (`open`, `claimed`, `resolved`) across various categories.

---

## 4. Automated Testing Suite (`tests/`)

Use `pytest` with Flask's test client and an isolated, in-memory or temporary SQLite database. Tests must never touch production files.

Implement the following mandatory test coverage across files:
1. **`test_home.py`**:
   - `test_home_page_status_code`: Verifies HTTP 200 and presence of CampusFind branding.
   - `test_dashboard_statistics`: Verifies item counts (total, lost, found, resolved) match database state.
   - `test_empty_database_render`: Verifies home page renders cleanly with empty-state UI when no items exist.
2. **`test_items.py`**:
   - `test_create_item_authenticated`: Successful item creation redirect and persistence in DB.
   - `test_create_item_unauthenticated`: Redirects to login page.
   - `test_item_detail_view`: Correct item info displayed.
   - `test_update_item_owner`: Owner can edit title/description and change status to `claimed` or `resolved`.
   - `test_unauthorized_edit_forbidden`: Non-owner user receives HTTP 403 or redirect on edit attempt.
   - `test_delete_item`: Owner can delete item; record removed from DB.
3. **`test_validation.py`**:
   - `test_missing_required_fields`: Form submission fails gracefully with error message.
   - `test_invalid_item_type`: Reject values other than `'lost'` or `'found'`.
   - `test_invalid_category`: Reject unsupported categories.
   - `test_sql_injection_resilience`: Malicious payloads (e.g., `' OR '1'='1`) treated as literal text without breaking query or exposing unauthorized data.
   - `test_search_and_filtering`: Keyword search filters title/description; category and status filters accurately filter result set.
4. **`test_health.py`**:
   - `test_health_endpoint_healthy`: Returns HTTP 200 with JSON status `healthy`.
   - `test_health_endpoint_db_failure`: Simulating a database disconnection returns HTTP 503 with JSON status `unhealthy`.

---

## 5. Docker Containerization (`Dockerfile` & `.dockerignore`)

- Base image: `python:3.11-slim`.
- Optimization: Run `apt-get clean && rm -rf /var/lib/apt/lists/*` to keep image small.
- Security:
  - Create a dedicated non-root system group and user: `addgroup --system appgroup && adduser --system --ingroup appgroup appuser`.
  - Set working directory to `/app`.
  - Switch to `USER appuser`.
- Configuration:
  - Expose port via environment variable `ENV PORT=5000` and `EXPOSE 5000`.
  - Production WSGI command: `CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:app"]`.
  - Built-in container health check: `HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD curl -f http://localhost:5000/health || exit 1`.

---

## 6. CI/CD & DevSecOps Pipeline (`.github/workflows/ci-cd.yml`)

Implement a complete, deterministic GitHub Actions pipeline triggered on `push` and `pull_request` to `main`:

```yaml
# Pipeline Architecture:
# [Job 1: test] -> [Job 2: security-scan] -> [Job 3: build-and-push] -> [Job 4: deploy] -> [Job 5: smoke-test]
```

### Required Jobs:
1. **`test` Job:**
   - Runs on `ubuntu-latest`.
   - Checks out code, sets up Python 3.11 with pip cache.
   - Installs dependencies from `requirements.txt`.
   - Runs `pytest --maxfail=1 --disable-warnings -v`.
   - Fails the workflow immediately if any test fails.
2. **`security-scan` Job:**
   - Needs: `test`.
   - Builds the Docker image locally: `docker build -t campusfind:scan-test .`.
   - Runs **Trivy Vulnerability Scanner** (`aquasecurity/trivy-action@master`):
     - `scan-type: 'image'`
     - `format: 'table'`
     - `severity: 'CRITICAL,HIGH'`
     - `exit-code: '1'` (blocks the pipeline on critical/high vulnerabilities).
   - Generates and uploads a scan summary.
3. **`build-and-push` Job:**
   - Needs: `security-scan`.
   - Only runs on `push` to `main` (not on unmerged PRs).
   - Authenticates to **GitHub Container Registry (GHCR)** using `${{ secrets.GITHUB_TOKEN }}`.
   - Tags image with immutable commit SHA (`ghcr.io/${{ github.repository }}:${{ github.sha }}`) and `latest`.
   - Pushes image to GHCR.
4. **`deploy` Job:**
   - Needs: `build-and-push`.
   - Deploys the application using a verified deployment hook (e.g., Render Deploy Hook URL or container restart webhook via `${{ secrets.RENDER_DEPLOY_HOOK_URL }}`).
   - If secrets are missing during local forks, includes safe step conditionals so the job outputs a clear informative setup guide rather than crashing silently.
5. **`smoke-test` Job:**
   - Needs: `deploy`.
   - Executes `python scripts/smoke_test.py --url ${{ secrets.APP_URL || 'http://localhost:5000' }}`.
   - Verifies `/health` returns 200 and `/` returns 200 with expected HTML signature.
   - Fails release if smoke test returns non-zero exit code.

---

## 7. Post-Deployment Smoke Test Script (`scripts/smoke_test.py`)

- Accepts `--url` argument with timeout options.
- Performs sequential HTTP assertions:
  1. `GET <URL>/health` -> Asserts status 200 and JSON `status == 'healthy'`.
  2. `GET <URL>/` -> Asserts status 200 and presence of `<title>CampusFind` or main header.
  3. `GET <URL>/items/new` -> Asserts status 200 or 302 (redirect to login).
- Prints formatted check status with timestamps.
- Exits with `0` on 100% pass, `1` on any failure.

---

## 8. Faculty-Facing Documentation (`README.md`)

The README must be publication-grade and include:
1. **Project Overview & Academic Purpose:** Problem statement, solution, why DevOps is the core focus.
2. **Architecture & Pipeline Diagrams:** ASCII or Mermaid diagrams illustrating application flow and the 5-stage DevSecOps pipeline.
3. **Technology Stack Table:** Component, Tool, Purpose, and Rationale.
4. **Local Quickstart Guide (Step-by-step for macOS & Linux):**
   - Virtualenv creation & dependency installation.
   - Database migration & seed command (`python scripts/seed_demo_data.py`).
   - Running the local development server.
   - Running the test suite (`pytest`).
5. **Docker Execution Instructions:**
   - Build container: `docker build -t campusfind:local .`
   - Run container: `docker run --rm -p 5000:5000 -e SECRET_KEY=demo campusfind:local`
   - Inspect health: `curl http://localhost:5000/health`
6. **GitHub Actions & Secrets Setup Guide:**
   - Instructions on configuring `RENDER_DEPLOY_HOOK_URL` and `APP_URL`.
7. **8-Step Live Faculty Demonstration Script:**
   - Exact steps to demonstrate (App tour -> Code change push -> CI test pass -> DevSecOps Trivy gate -> Docker local run -> Live deployment -> Intentional test failure demo -> Health verification).
8. **Failure Handling & Rollback Protocol:**
   - Documented rollback procedure if a deployment fails smoke testing.

---

## 9. Phased Execution Instructions for the Agent

Execute this project sequentially through the following 8 phases. At the end of each phase, run the verification command to confirm completion before proceeding:

- **Phase 1: Project Setup & Dependencies**
  - Create directory layout, `.gitignore`, `.dockerignore`, `pytest.ini`, and `requirements.txt` with pinned versions (`Flask`, `gunicorn`, `pytest`, `requests`, `werkzeug`).
- **Phase 2: Database Layer**
  - Implement `database/schema.sql`, `database/init_db.py`, and `config.py`.
- **Phase 3: Core Application & Authentication**
  - Implement `app.py` with session auth, item CRUD, parameterized SQL, input validators, error handlers, and `/health`.
- **Phase 4: Frontend Templates & Styling**
  - Implement `templates/base.html`, `index.html`, `report_item.html`, `item_detail.html`, `edit_item.html`, `login.html`, `register.html`, `static/css/style.css`, and `static/js/main.js`.
- **Phase 5: Demo Seed Data & Smoke Test Script**
  - Implement `scripts/seed_demo_data.py` and `scripts/smoke_test.py`.
- **Phase 6: Automated Test Suite**
  - Implement `tests/conftest.py`, `test_home.py`, `test_items.py`, `test_validation.py`, and `test_health.py`.
  - **Verification:** Run `pytest` locally and ensure all tests pass.
- **Phase 7: Containerization & CI/CD Pipeline**
  - Implement `Dockerfile` and `.github/workflows/ci-cd.yml`.
- **Phase 8: Comprehensive Documentation & Demo Guide**
  - Implement `README.md` containing all diagrams, setup commands, and faculty presentation checklist.

Begin immediate execution of Phase 1 through Phase 8. Do not stop until all files are generated and verified.
