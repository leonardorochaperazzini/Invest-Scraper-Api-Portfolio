#!/bin/sh

# uncomment to revert the database to the initial state
# alembic downgrade base

alembic upgrade head

set -e

ls -all

cd app

ls -all

exec uvicorn api:app --host 0.0.0.0 --port 8000 --reload