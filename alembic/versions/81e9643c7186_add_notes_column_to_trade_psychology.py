"""Add notes column to trade_psychology

Revision ID: 81e9643c7186
Revises: 159ad850179a
Create Date: 2026-01-06 06:37:40.822526
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "81e9643c7186"
down_revision: Union[str, Sequence[str], None] = "159ad850179a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add notes column to trade_psychology."""
    op.add_column(
        "trade_psychology",
        sa.Column("notes", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    """Remove notes column from trade_psychology."""
    op.drop_column("trade_psychology", "notes")
