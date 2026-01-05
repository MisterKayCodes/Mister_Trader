"""
add trade drafts (sqlite-safe)

Revision ID: 9a952e9202ae
Revises: 51be39ac8ab6
Create Date: 2026-01-05 07:04:06.610362
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9a952e9202ae"
down_revision: Union[str, Sequence[str], None] = "51be39ac8ab6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    SQLite does NOT support ALTER COLUMN.
    Since this is early development, we safely drop and recreate the table.
    """

    # Drop existing table if it exists
    op.drop_table("trade_drafts")

    # Recreate table with the correct schema
    op.create_table(
        "trade_drafts",
        sa.Column("id", sa.Integer, primary_key=True),

        sa.Column(
            "account_id",
            sa.Integer,
            sa.ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),

        sa.Column("symbol", sa.String(length=20), nullable=False),
        sa.Column("side", sa.String(length=10), nullable=False),
        sa.Column("quantity", sa.Float, nullable=False),
        sa.Column("price", sa.Float, nullable=True),

        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="draft",
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """
    Downgrade simply removes trade_drafts.
    Old schema is intentionally not restored.
    """

    op.drop_table("trade_drafts")
