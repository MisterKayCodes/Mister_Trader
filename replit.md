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
- **Handlers**: Structured handlers for Accounts, Trades, Media, Psychology, and Activity.
- **Persistence**: Uses `SQLStorage` (`fsm_storage.db`) for session data.
- **Authentication**: Requires `/signup` and `/login` with a numeric PIN.

### Frontend Architecture (React)
- **Framework**: Vite + React + Tailwind CSS.

## User Preferences
- Preferred communication style: Simple, everyday language.
- Database: Exclusively SQLite for development.
