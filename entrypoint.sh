#!/bin/sh

# uncomment to revert the database to the initial state
# alembic downgrade base

alembic upgrade head

python -u ./main.py