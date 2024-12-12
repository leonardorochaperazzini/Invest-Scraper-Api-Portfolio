"""create view scraper_run_tickers_data

Revision ID: 525526077ad1
Revises: e1fafcd21851
Create Date: 2024-12-12 11:42:28.789083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '525526077ad1'
down_revision: Union[str, None] = 'e1fafcd21851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute('''
        CREATE OR REPLACE VIEW invest.scraper_run_tickers_data AS 
            SELECT
                c."name" AS ticker_name
                , d."name" AS ticker_type_name
                , a."data"->>'price' as ticker_price
                , a."data"->>'pvp' as ticker_pvp
                , a."data"->>'dy' as ticker_dy
                , a."data"->>'roe' as ticker_roe
                , b.started_at AS scraper_started_at
                , b.ended_at AS scraper_ended_at
            FROM 
                invest.scraper_tickers_data AS a
            JOIN
                invest.scraper_runs_tickers AS b ON b.id = a.scraper_run_ticker_id
            JOIN
                invest.tickers AS c ON c.id = b.ticker_id 
            JOIN
                invest.tickers_types AS d ON d.id = c.ticker_type_id
            ORDER by
                b.started_at
            DESC
    ''')


def downgrade() -> None:
    op.execute('''
        DROP VIEW invest."scraper_run_tickers_data";
    ''')
