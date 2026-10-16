"""Post-deployment smoke test for CampusFind.

Usage: python scripts/smoke_test.py --url https://campusfind.example.com [--timeout 10] [--retries 5]
Exits 0 when every check passes, 1 otherwise.
"""
import argparse
import sys
import time
from datetime import datetime

import requests


def log(ok, name, detail):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{stamp}] [{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def check_health(base, timeout):
    r = requests.get(f"{base}/health", timeout=timeout)
    body = r.json()
    ok = r.status_code == 200 and body.get("status") == "healthy"
    return ok, f"HTTP {r.status_code}, status={body.get('status')}, db={body.get('database')}"


def check_home(base, timeout):
    r = requests.get(f"{base}/", timeout=timeout)
    ok = r.status_code == 200 and "<title>CampusFind" in r.text
    return ok, f"HTTP {r.status_code}, signature {'found' if '<title>CampusFind' in r.text else 'missing'}"


def check_report_page(base, timeout):
    r = requests.get(f"{base}/items/new", timeout=timeout, allow_redirects=False)
    ok = r.status_code in (200, 302)
    return ok, f"HTTP {r.status_code}" + (f" -> {r.headers.get('Location')}" if r.status_code == 302 else "")


CHECKS = [("GET /health", check_health), ("GET /", check_home), ("GET /items/new", check_report_page)]


def run(base, timeout, retries, delay):
    base = base.rstrip("/")
    print(f"Smoke testing {base}")
    failures = 0
    for name, fn in CHECKS:
        for attempt in range(1, retries + 1):
            try:
                ok, detail = fn(base, timeout)
            except (requests.RequestException, ValueError) as exc:
                ok, detail = False, f"{type(exc).__name__}: {exc}"
            if ok or attempt == retries:
                break
            print(f"  attempt {attempt}/{retries} failed ({detail}); retrying in {delay}s")
            time.sleep(delay)
        log(ok, name, detail)
        failures += not ok
    total = len(CHECKS)
    print(f"Result: {total - failures}/{total} checks passed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="CampusFind post-deployment smoke test")
    p.add_argument("--url", default="http://localhost:5000", help="base URL of the deployed app")
    p.add_argument("--timeout", type=float, default=10.0, help="per-request timeout in seconds")
    p.add_argument("--retries", type=int, default=5, help="attempts per check (allows for cold starts)")
    p.add_argument("--delay", type=float, default=10.0, help="seconds between retries")
    a = p.parse_args()
    sys.exit(run(a.url, a.timeout, a.retries, a.delay))
