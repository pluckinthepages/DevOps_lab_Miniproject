# ---------- Stage 1: build wheels ----------
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
# Runtime needs only the web stack; test/smoke-test tools (pytest, requests) stay out of the image.
RUN grep -Ei '^(flask|werkzeug|gunicorn)==' requirements.txt > runtime-requirements.txt \
 && pip wheel --no-cache-dir --wheel-dir /wheels -r runtime-requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=5000 \
    DATABASE_URL=sqlite:////app/data/campusfind.db

# curl is needed for HEALTHCHECK; upgrade base packages to pick up security fixes.
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends curl \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN addgroup --system --gid 10001 appgroup \
 && adduser --system --uid 10001 --ingroup appgroup --no-create-home appuser

WORKDIR /app
COPY --from=builder /wheels /wheels
# Remove packaging tools afterwards: they are unused at runtime and carry CVEs.
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels \
 && pip uninstall -y pip setuptools wheel

COPY --chown=appuser:appgroup . .
RUN mkdir -p /app/data && chown -R appuser:appgroup /app/data

USER appuser

EXPOSE 5000
VOLUME ["/app/data"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:app"]
