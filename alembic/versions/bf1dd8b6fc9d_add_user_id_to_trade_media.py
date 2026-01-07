"""add user_id to trade media

Revision ID: bf1dd8b6fc9d
Revises: 05b33615462e
Create Date: 2026-01-06 20:18:38.590777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf1dd8b6fc9d'
down_revision: Union[str, Sequence[str], None] = '05b33615462e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rule 13: Mandatory Batch Mode for SQLite to add Foreign Key constraints
    with op.batch_alter_table('trade_media', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_index(batch_op.f('ix_trade_media_user_id'), ['user_id'], unique=False)
        batch_op.create_foreign_key('fk_trade_media_user', 'users', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    with op.batch_alter_table('trade_media', schema=None) as batch_op:
        batch_op.drop_constraint('fk_trade_media_user', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_trade_media_user_id'))
        batch_op.drop_column('user_id')
