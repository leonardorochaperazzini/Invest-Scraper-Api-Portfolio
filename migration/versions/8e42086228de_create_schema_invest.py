"""create schema invest

Revision ID: 8e42086228de
Revises: 
Create Date: 2024-11-19 11:52:15.109870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e42086228de'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS invest;')


def downgrade() -> None:
    op.execute('DROP SCHEMA IF EXISTS invest CASCADE;')
