"""Add plan_id, emotions, day_of_week to trades

Revision ID: 76ff70659865
Revises: 654bda37ed6f
Create Date: 2026-01-09 00:39:02.854129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76ff70659865'
down_revision: Union[str, Sequence[str], None] = '654bda37ed6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('trades', sa.Column('plan_id', sa.Integer(), nullable=True))
    op.add_column('trades', sa.Column('pre_trade_emotion', sa.String(length=30), nullable=True))
    op.add_column('trades', sa.Column('post_trade_emotion', sa.String(length=30), nullable=True))
    op.add_column('trades', sa.Column('day_of_week', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_trades_plan_id'), 'trades', ['plan_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_trades_plan_id'), table_name='trades')
    op.drop_column('trades', 'day_of_week')
    op.drop_column('trades', 'post_trade_emotion')
    op.drop_column('trades', 'pre_trade_emotion')
    op.drop_column('trades', 'plan_id')
