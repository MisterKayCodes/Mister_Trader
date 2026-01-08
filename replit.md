# Mister Trader

## Overview
Mister Trader is a comprehensive trading journal and management system built with FastAPI, React (Vite + Tailwind CSS), and a Telegram bot interface.

## System Architecture

### Backend Architecture (FastAPI)
- **Primary Database**: `mister_trader.db` (SQLite).
- **ORM**: SQLAlchemy with Alembic for migrations.
- **Communication**: REST API for frontend and Telegram bot interaction.
- **Critical Configuration**: 
    - `BACKEND_API_URL` uses Replit's dev domain for stable bot-to-server communication.
    - Database engine is hard-coded to SQLite in `app/core/database.py` to avoid accidental Postgres connection attempts from Replit system secrets.
    - Root route `@app.get("/")` provided for health monitoring.

### Telegram Bot Architecture (Aiogram)
- **Handlers** (all follow `*_handlers.py` naming convention):
    - `auth_handlers.py` - /start, /signup, /login commands
    - `account_handlers.py` - Vault/Account CRUD operations
    - `trade_handlers.py` - Trade logging, closing, modifying
    - `voice_handlers.py` - Voice note recording and playback
    - `psychology_handlers.py` - Trading discipline/psychology logging
    - `media_handlers.py` - Trade screenshot/chart uploads
    - `activity_handlers.py` - Daily activity tracking
    - `menu_handlers.py` - Global navigation handlers
- **States** (FSM state groups for multi-step flows):
    - `account_states.py`, `trade_states.py`, `voice_note_states.py`
    - `psychology_states.py`, `media_states.py`, `activity_states.py`
- **Persistence**: Uses `SQLStorage` (`fsm_storage.db`) for session data.
- **Authentication**: Requires `/signup` and `/login` with a numeric PIN. Session persists across bot restarts.

### Frontend Architecture (React)
- **Framework**: Vite + React + Tailwind CSS.

## User Preferences
- Preferred communication style: Simple, everyday language.
- Database: Exclusively SQLite for development.

## Recent Changes (2026-01-08)
- Refactored psychology, media, and activity handlers to comprehensive versions
- All handlers now follow `*_handlers.py` naming convention
- Added proper FSM states for all multi-step flows
- Updated keyboards to match new callback_data patterns
- FSM storage persists login sessions across bot restarts
