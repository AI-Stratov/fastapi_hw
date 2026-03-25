#!/bin/sh
set -e

uv run --no-sync alembic -c infrastructure/psql/alembic.ini upgrade head

exec uv run --no-sync uvicorn infrastructure.web.app:app --host 0.0.0.0 --port 5000