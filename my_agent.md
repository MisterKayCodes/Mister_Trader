# Mister Trader

## Overview
Mister Trader is a comprehensive trading journal and management system built with FastAPI, React (Vite + Tailwind CSS), and a Telegram bot interface.

## System Architecture

### Backend Architecture (FastAPI)
- **Primary Database**: `mister_trader.db` (SQLite)
- **ORM**: SQLAlchemy with Alembic for migrations
- **Communication**: REST API for frontend and Telegram bot interaction
- **Port**: 5000 (backend API)

### Database Models
| Model | Purpose |
|-------|---------|
| `User` | Telegram user authentication |
| `Account` | Trading accounts/vaults |
| `Trade` | Individual trades with outcomes, session, strategy |
| `Strategy` | Trading strategies with entry/exit criteria |
| `TradingPlan` | Daily trading plans |
| `UserStats` | Aggregated statistics per user |
| `Activity` | Daily activity logs |
| `TradePsychology` | Psychology notes per trade |
| `TradeMedia` | Screenshots/charts |
| `VoiceNote` | Voice recordings |
| `Reminder` | Notification settings |

### Telegram Bot Architecture (Aiogram)
- **Handlers** (all follow `*_handlers.py` naming convention):
    - `auth_handlers.py` - /start, /signup, /login
    - `account_handlers.py` - Vault/Account CRUD
    - `trade_handlers.py` - Trade logging, closing
    - `stats_handlers.py` - /stats with inline keyboard navigation
    - `export_handlers.py` - /export CSV download
    - `strategy_handlers.py` - /strategy CRUD
    - `plan_handlers.py` - /plan trading plan CRUD
    - `voice_handlers.py` - Voice note recording
    - `psychology_handlers.py` - Psychology logging
    - `media_handlers.py` - Screenshot uploads
    - `activity_handlers.py` - Daily activity
    - `menu_handlers.py` - Navigation
- **Persistence**: Uses `SQLStorage` (`fsm_storage.db`) for session data

### Frontend Architecture (React)
- **Framework**: Vite + React + Tailwind CSS
- **Served from**: FastAPI on port 5000 (built static files in `react/dist/`)
- **Pages**: Dashboard, Trade Journal, Strategies, Trading Plans, Settings
- **API Client**: `/react/src/utils/api.js` (uses relative `/api/v1` paths)
- **Build command**: `cd react && npm run build` (outputs to `react/dist/`)

### Key Utilities
- `app/utils/session_utils.py` - Trading session detection (London/NY/Asian/Sydney)
- `app/utils/trade_utils.py` - Win/loss/breakeven detection
- `app/utils/streak_utils.py` - Streak calculation
- `app/utils/validation_utils.py` - Trade entry validation

## User Preferences
- Preferred communication style: Simple, everyday language
- Database: Exclusively SQLite for development

## API URL Conventions (CRITICAL)
When calling backend from Telegram handlers:
- **Analytics endpoints**: NO trailing slash (`/api/v1/analytics/stats`, `/api/v1/analytics/sessions`)
- **Strategy/Plan list & create**: WITH trailing slash (`/api/v1/strategies/`, `/api/v1/plans/`)
- **Strategy/Plan by ID**: NO trailing slash (`/api/v1/strategies/{id}`, `/api/v1/plans/{id}`)
- **Export CSV**: `/api/v1/export/trades/csv`

## Stats Response Fields (CRITICAL)
Backend `/api/v1/analytics/stats` returns:
- `winning_trades` (NOT `total_wins`)
- `losing_trades` (NOT `total_losses`)
- `total_trades`, `win_rate`, `total_pnl`
- `best_trade_pnl`, `worst_trade_pnl`
- `current_streak`, `current_streak_type`, `best_win_streak`, `worst_loss_streak`

## Recent Changes (2026-01-09)
- **Fixed R:R bug**: Risk:Reward now correctly parses "1:2" format (was only extracting "1" instead of full ratio)
- **React frontend integrated with FastAPI**: Built React app now served from FastAPI on port 5000
- Removed separate React workflow - single server architecture
- Added CORS middleware to FastAPI for browser requests
- Added new analytics endpoints: `/api/v1/analytics/days`, `/api/v1/analytics/symbols`, `/api/v1/analytics/psychology`
- Added day-of-week performance analysis
- Added symbol/pair performance tracking
- Added psychology insights (win rate by emotion, emotion+symbol combinations)
- Added weekly summary scheduler (APScheduler) - sends summaries every Sunday at 20:00 UTC
- Updated stats inline keyboard with new tabs: Pairs, Days, Psychology
- Stats handlers now show actionable insights like "You win X% when feeling Y on Z"

## Previous Changes (2026-01-09 early)
- Fixed API URL trailing slash issues causing 307 redirects
- Fixed stats handlers to use correct response field names
- Fixed export URL to use `/trades/csv`
- All Telegram handlers now have FSM states defined inline (StrategyStates, PlanStates)
- Removed app/telegram/utils/auth.py - all handlers check access_token from state directly

## Previous Changes (2026-01-08)
- Added Strategy model and CRUD handlers
- Added TradingPlan model and CRUD handlers
- Added UserStats for aggregated analytics
- Added /stats command with inline keyboard (overview, sessions, strategies, streaks, time)
- Added /export command for CSV download
- Added session detection utility (London/NY/Asian/Sydney)
- Added streak tracking utility
- Added trade validation utility
- Created React frontend with Vite + Tailwind CSS
- Created comprehensive INSTRUCTIONS.md documentation
- Updated README.md with full feature list
- **Added main menu buttons** for Stats, Export, Strategies, Plans (previously only accessible via commands)
- Added inline keyboards for Strategy and Plan management
