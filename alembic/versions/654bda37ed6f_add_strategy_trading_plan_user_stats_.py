"""Add strategy, trading_plan, user_stats, reminder tables and trade enhancements

Revision ID: 654bda37ed6f
Revises: bf1dd8b6fc9d
Create Date: 2026-01-08 23:36:10.889034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '654bda37ed6f'
down_revision: Union[str, Sequence[str], None] = 'bf1dd8b6fc9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('reminders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('reminder_type', sa.String(length=50), nullable=False),
    sa.Column('is_enabled', sa.Boolean(), nullable=False),
    sa.Column('time_utc', sa.Time(), nullable=True),
    sa.Column('days_of_week', sa.String(length=20), nullable=True),
    sa.Column('message', sa.String(length=500), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reminders_id'), 'reminders', ['id'], unique=False)
    op.create_index(op.f('ix_reminders_user_id'), 'reminders', ['user_id'], unique=False)
    
    op.create_table('strategies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('rules', sa.Text(), nullable=True),
    sa.Column('entry_criteria', sa.Text(), nullable=True),
    sa.Column('exit_criteria', sa.Text(), nullable=True),
    sa.Column('risk_per_trade', sa.String(length=50), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_strategies_id'), 'strategies', ['id'], unique=False)
    op.create_index(op.f('ix_strategies_user_id'), 'strategies', ['user_id'], unique=False)
    
    op.create_table('trading_plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('plan_date', sa.Date(), nullable=True),
    sa.Column('market_bias', sa.String(length=50), nullable=True),
    sa.Column('key_levels', sa.Text(), nullable=True),
    sa.Column('watchlist', sa.Text(), nullable=True),
    sa.Column('news_events', sa.Text(), nullable=True),
    sa.Column('mental_state', sa.String(length=100), nullable=True),
    sa.Column('max_trades', sa.Integer(), nullable=True),
    sa.Column('max_loss', sa.String(length=50), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trading_plans_id'), 'trading_plans', ['id'], unique=False)
    op.create_index(op.f('ix_trading_plans_user_id'), 'trading_plans', ['user_id'], unique=False)
    
    op.create_table('user_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('total_trades', sa.Integer(), nullable=False),
    sa.Column('winning_trades', sa.Integer(), nullable=False),
    sa.Column('losing_trades', sa.Integer(), nullable=False),
    sa.Column('breakeven_trades', sa.Integer(), nullable=False),
    sa.Column('total_pnl', sa.Float(), nullable=False),
    sa.Column('best_trade_pnl', sa.Float(), nullable=False),
    sa.Column('worst_trade_pnl', sa.Float(), nullable=False),
    sa.Column('current_streak', sa.Integer(), nullable=False),
    sa.Column('current_streak_type', sa.String(length=10), nullable=True),
    sa.Column('best_win_streak', sa.Integer(), nullable=False),
    sa.Column('worst_loss_streak', sa.Integer(), nullable=False),
    sa.Column('avg_risk_reward', sa.Float(), nullable=False),
    sa.Column('london_wins', sa.Integer(), nullable=False),
    sa.Column('london_losses', sa.Integer(), nullable=False),
    sa.Column('newyork_wins', sa.Integer(), nullable=False),
    sa.Column('newyork_losses', sa.Integer(), nullable=False),
    sa.Column('asian_wins', sa.Integer(), nullable=False),
    sa.Column('asian_losses', sa.Integer(), nullable=False),
    sa.Column('sydney_wins', sa.Integer(), nullable=False),
    sa.Column('sydney_losses', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_stats_id'), 'user_stats', ['id'], unique=False)
    op.create_index(op.f('ix_user_stats_user_id'), 'user_stats', ['user_id'], unique=True)
    
    op.add_column('trades', sa.Column('strategy_id', sa.Integer(), nullable=True))
    op.add_column('trades', sa.Column('stop_loss', sa.Float(), nullable=True))
    op.add_column('trades', sa.Column('take_profit', sa.Float(), nullable=True))
    op.add_column('trades', sa.Column('risk_reward_ratio', sa.Float(), nullable=True))
    op.add_column('trades', sa.Column('pnl', sa.Float(), nullable=True))
    op.add_column('trades', sa.Column('outcome', sa.String(length=20), nullable=True))
    op.add_column('trades', sa.Column('trading_session', sa.String(length=20), nullable=True))
    op.add_column('trades', sa.Column('notes', sa.Text(), nullable=True))
    op.create_index(op.f('ix_trades_strategy_id'), 'trades', ['strategy_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_trades_strategy_id'), table_name='trades')
    op.drop_column('trades', 'notes')
    op.drop_column('trades', 'trading_session')
    op.drop_column('trades', 'outcome')
    op.drop_column('trades', 'pnl')
    op.drop_column('trades', 'risk_reward_ratio')
    op.drop_column('trades', 'take_profit')
    op.drop_column('trades', 'stop_loss')
    op.drop_column('trades', 'strategy_id')
    op.drop_index(op.f('ix_user_stats_user_id'), table_name='user_stats')
    op.drop_index(op.f('ix_user_stats_id'), table_name='user_stats')
    op.drop_table('user_stats')
    op.drop_index(op.f('ix_trading_plans_user_id'), table_name='trading_plans')
    op.drop_index(op.f('ix_trading_plans_id'), table_name='trading_plans')
    op.drop_table('trading_plans')
    op.drop_index(op.f('ix_strategies_user_id'), table_name='strategies')
    op.drop_index(op.f('ix_strategies_id'), table_name='strategies')
    op.drop_table('strategies')
    op.drop_index(op.f('ix_reminders_user_id'), table_name='reminders')
    op.drop_index(op.f('ix_reminders_id'), table_name='reminders')
    op.drop_table('reminders')
