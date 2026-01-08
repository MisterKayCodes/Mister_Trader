# Mister Trader

## Overview
Mister Trader is a comprehensive trading journal and management system built with FastAPI, React (Vite + Tailwind CSS), and a Telegram bot interface.

## System Architecture

### Backend Architecture (FastAPI)
- **Primary Database**: `mister_trader.db` (SQLite).
- **ORM**: SQLAlchemy with Alembic for migrations.
- **Communication**: REST API for frontend and Telegram bot interaction.
- **Recent Change (2026-01-08)**: 
    - Updated `BACKEND_API_URL` to use Replit's dev domain.
    - Added root route `@app.get("/")` for health monitoring.
    - Switched database engine to use SQLite exclusively for the development environment.

### Telegram Bot Architecture (Aiogram)
- **Handlers**: Structured handlers for Accounts, Trades, Media, Psychology, and Activity.
- **Persistence**: Uses `SQLStorage` (via `aiogram_sqlite_storage`) for FSM state persistence.
- **Communication**: Communicates with the backend via the public `BACKEND_API_URL`.

### Frontend Architecture (React)
- **Framework**: Vite + React.
- **Styling**: Tailwind CSS.

## User Preferences
- Preferred communication style: Simple, everyday language.
