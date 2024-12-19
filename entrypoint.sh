#!/bin/sh

set -e 

if [ "$ENV" = "TEST" ]; then
    alembic downgrade base
    alembic upgrade head
    export PYTHONPATH=/usr/app
    sleep 3
    echo "Running tests..."
    pytest test/integration/api/ --cov=app/api/ --cov=app/service --cov-report=html -s
else
    alembic upgrade head
    exec uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
fi