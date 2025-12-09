# ============================================================
# STAGE 1 — BUILDER
# ============================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from the same folder (correct path)
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r /app/requirements.txt


# ============================================================
# STAGE 2 — RUNTIME
# ============================================================
FROM python:3.11-slim AS runtime

WORKDIR /app

# Create non-root user
RUN useradd -m appuser

# Copy installed dependencies
COPY --from=builder /install /usr/local

# Copy application code to root (so main.py is at /app/main.py)
COPY app/ /app/
COPY requirements.txt /app/ 

# Permissions
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Command correct: main.py is now at the root
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]