"""enforce_non_nullable_user_id_on_trades

Revision ID: 05b33615462e
Revises: 59b1233e3eb7
Create Date: 2026-01-06 15:42:53.853086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05b33615462e'
down_revision: Union[str, Sequence[str], None] = '59b1233e3eb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('trades', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)


def downgrade() -> None:
    with op.batch_alter_table('trades', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
