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
- **Port**: 5173 (dev server)
- **Pages**: Dashboard, Trades, Strategies, Plans, Settings
- **API Client**: `/react/src/utils/api.js`

### Key Utilities
- `app/utils/session_utils.py` - Trading session detection (London/NY/Asian/Sydney)
- `app/utils/trade_utils.py` - Win/loss/breakeven detection
- `app/utils/streak_utils.py` - Streak calculation
- `app/utils/validation_utils.py` - Trade entry validation

## User Preferences
- Preferred communication style: Simple, everyday language
- Database: Exclusively SQLite for development

## Recent Changes (2026-01-08)
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
- Added `app/telegram/utils/auth.py` helper for state authentication
