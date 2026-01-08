# Mister Trader

## Overview

Mister Trader is a comprehensive trading journal and management system designed for traders to log, track, and analyze their trades. The platform consists of three main components:

1. **FastAPI Backend** - REST API handling all business logic, authentication, and data persistence
2. **React Frontend** - Web interface built with Vite and Tailwind CSS
3. **Telegram Bot** - Mobile-friendly interface using Aiogram for on-the-go trade logging and management

Key capabilities include multi-account (vault) management, trade journaling with entry/exit tracking, psychology tracking for discipline monitoring, media attachments (screenshots), and voice note recordings for trade analysis.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture (FastAPI)

**Layered Structure:**
- `app/api/v1/` - REST endpoints organized by resource (users, accounts, trades, etc.)
- `app/services/` - Business logic layer, decoupled from HTTP handling
- `app/models/` - SQLAlchemy ORM models defining database schema
- `app/schemas/` - Pydantic models for request/response validation
- `app/core/` - Shared utilities (config, database, security, storage)

**Authentication Pattern:**
- PIN-based authentication tied to Telegram user IDs
- JWT tokens for session management with 24-hour expiry
- Security guard pattern via `get_current_user` dependency that validates tokens and enforces ownership on all protected routes
- All data queries filter by `user_id` to enforce strict data isolation

**Key Design Decisions:**
- User ID is never accepted from request bodies - always extracted from JWT token
- All resources (accounts, trades, media) have non-nullable `user_id` foreign keys
- Service layer handles business rules; API layer handles HTTP concerns only

### Telegram Bot Architecture (Aiogram 3.x)

**Structure:**
- `app/telegram/handlers/` - Message and callback handlers organized by feature
- `app/telegram/states/` - FSM (Finite State Machine) state definitions for multi-step flows
- `app/telegram/keyboards/` - Reply and inline keyboard definitions

**State Management:**
- Uses `aiogram-sqlite-storage` for persistent FSM state across bot restarts
- Access tokens stored in FSM data for authenticated API calls
- Active account context maintained in user session

**Communication:**
- Bot communicates with backend via HTTP using `httpx` async client
- All API calls include JWT Bearer token from user's session state

### Database Design

**Technology:** SQLAlchemy ORM with Alembic migrations

**Core Tables:**
- `users` - Telegram identity and hashed PIN
- `accounts` - Trading vaults/accounts (max 6 per user)
- `trades` - Trade entries with symbol, side, quantity, prices, state
- `trade_psychology` - Discipline and confidence tracking per trade
- `trade_media` - Screenshot attachments
- `trade_voice_notes` - Audio recordings
- `daily_activity` - Activity logging

**Relationships:**
- All tables cascade delete from parent user
- Strict foreign key enforcement with ownership validation

### File Storage

**Physical Storage:**
- Files saved to `media/` directory with subdirectories: `images/`, `voice/`, `documents/`
- UUID-based filenames prevent collisions
- `app/core/storage.py` handles file operations with path traversal protection

**Database Linking:**
- File paths stored as relative strings in database
- Static file serving via FastAPI's `StaticFiles` mount at `/media`

## External Dependencies

### Database
- **SQLAlchemy 2.0+** - ORM for database operations
- **Alembic** - Database migrations with batch mode for SQLite compatibility
- **SQLite** (default) or **PostgreSQL** - Primary data store (configurable via `DATABASE_URL`)
- **psycopg2-binary** - PostgreSQL driver (included for production deployment)

### Authentication & Security
- **python-jose** - JWT token encoding/decoding
- **passlib + bcrypt** - Password/PIN hashing

### Telegram Integration
- **Aiogram 3.x** - Async Telegram bot framework
- **aiogram-sqlite-storage** - Persistent FSM storage for bot sessions

### HTTP & API
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **httpx** - Async HTTP client for bot-to-backend communication
- **python-multipart** - File upload handling

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling

### Environment Variables Required
```
TELEGRAM_BOT_TOKEN - Bot token from @BotFather
DATABASE_URL - Database connection string
SECRET_KEY - JWT signing secret (required, no default)
BACKEND_API_URL - Backend URL for Telegram bot API calls
```