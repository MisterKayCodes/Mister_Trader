"""add user_id to voice notes

Revision ID: 59b1233e3eb7
Revises: a25b6278d920
Create Date: 2026-01-06 15:21:28.892281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59b1233e3eb7'
down_revision: Union[str, Sequence[str], None] = 'a25b6278d920'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rule 7 & 13: Use batch_alter_table to handle SQLite's ALTER limitations
    with op.batch_alter_table('trade_voice_notes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_index(batch_op.f('ix_trade_voice_notes_user_id'), ['user_id'], unique=False)
        batch_op.create_foreign_key('fk_voice_notes_user', 'users', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('trade_voice_notes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_voice_notes_user', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_trade_voice_notes_user_id'))
        batch_op.drop_column('user_id')
