"""create fks scrappers and tickers

Revision ID: 62a9e41c6008
Revises: a7c6180722d3
Create Date: 2024-11-21 12:24:13.344738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62a9e41c6008'
down_revision: Union[str, None] = 'a7c6180722d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        ALTER TABLE invest."scrapper_runs_tickers" 
        ADD CONSTRAINT scrapper_runs_tickers_scrapper_run_id_fkey
        FOREIGN KEY("scrapper_run_id") 
        REFERENCES invest."scrapper_runs"("id")
        ON UPDATE NO ACTION ON DELETE CASCADE;
               
        ALTER TABLE invest."tickers"
        ADD CONSTRAINT tickers_ticker_type_id_fkey
        FOREIGN KEY("ticker_type_id") 
        REFERENCES invest."tickers_types"("id")
        ON UPDATE NO ACTION ON DELETE CASCADE;
               
        ALTER TABLE invest."scrapper_runs_tickers"
        ADD CONSTRAINT scrapper_runs_tickers_ticket_id_fkey
        FOREIGN KEY("ticket_id") 
        REFERENCES invest."tickers"("id")
        ON UPDATE NO ACTION ON DELETE NO ACTION;
    ''')


def downgrade() -> None:
    op.execute('''
        ALTER TABLE invest."scrapper_runs_tickers" 
        DROP CONSTRAINT scrapper_runs_tickers_scrapper_run_id_fkey;
               
        ALTER TABLE invest."tickers"
        DROP CONSTRAINT tickers_ticker_type_id_fkey;
               
        ALTER TABLE invest."scrapper_runs_tickers"
        DROP CONSTRAINT scrapper_runs_tickers_ticket_id_fkey;
    ''')