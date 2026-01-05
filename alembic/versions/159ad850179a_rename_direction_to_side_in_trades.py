"""Rename direction to side in trades with table existence check

Revision ID: 159ad850179a
Revises: e47d963c62bc
Create Date: 2026-01-05 08:22:08.907014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision: str = '159ad850179a'
down_revision: Union[str, Sequence[str], None] = 'e47d963c62bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)
    tables = inspector.get_table_names()

    if 'trades_new' not in tables:
        # Create new trades table with new schema (side, quantity, no direction)
        op.create_table(
            'trades_new',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('user_id', sa.Integer, nullable=True),
            sa.Column('account_id', sa.Integer, sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('symbol', sa.String(length=20), nullable=False),
            sa.Column('side', sa.String(length=10), nullable=False),
            sa.Column('quantity', sa.Float, nullable=False),
            sa.Column('entry_price', sa.Float, nullable=True),
            sa.Column('exit_price', sa.Float, nullable=True),
            sa.Column('state', sa.String(length=20), nullable=True),
            sa.Column('open_timestamp', sa.DateTime, nullable=True),
            sa.Column('close_timestamp', sa.DateTime, nullable=True),
            sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
            sa.Column('updated_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
        )

        # Copy data from old trades table to new table, mapping direction to side, quantity default 0
        op.execute("""
            INSERT INTO trades_new (
                id, user_id, account_id, symbol, side, quantity, entry_price, exit_price,
                state, open_timestamp, close_timestamp, created_at, updated_at
            )
            SELECT
                id, user_id, account_id, symbol, direction, 0, entry_price, exit_price,
                state, open_timestamp, close_timestamp, created_at, updated_at
            FROM trades
        """)

        # Drop old trades table
        op.drop_table('trades')

        # Rename new table to trades
        op.rename_table('trades_new', 'trades')
    else:
        print("Table 'trades_new' already exists, skipping creation.")


def downgrade() -> None:
    """Downgrade schema."""

    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)
    tables = inspector.get_table_names()

    if 'trades_old' not in tables:
        # Create old trades table with direction column (no side, no quantity)
        op.create_table(
            'trades_old',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('user_id', sa.Integer, nullable=True),
            sa.Column('account_id', sa.Integer, sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
            sa.Column('symbol', sa.String(length=20), nullable=False),
            sa.Column('direction', sa.String(length=10), nullable=False),
            sa.Column('entry_price', sa.Float, nullable=True),
            sa.Column('exit_price', sa.Float, nullable=True),
            sa.Column('state', sa.String(length=20), nullable=True),
            sa.Column('open_timestamp', sa.DateTime, nullable=True),
            sa.Column('close_timestamp', sa.DateTime, nullable=True),
            sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
            sa.Column('updated_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
        )

        # Copy data from current trades to old trades table, mapping side -> direction, ignore quantity
        op.execute("""
            INSERT INTO trades_old (
                id, user_id, account_id, symbol, direction, entry_price, exit_price,
                state, open_timestamp, close_timestamp, created_at, updated_at
            )
            SELECT
                id, user_id, account_id, symbol, side, entry_price, exit_price,
                state, open_timestamp, close_timestamp, created_at, updated_at
            FROM trades
        """)

        # Drop current trades table
        op.drop_table('trades')

        # Rename old trades table back to trades
        op.rename_table('trades_old', 'trades')
    else:
        print("Table 'trades_old' already exists, skipping creation.")
