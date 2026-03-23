# Detailed Project Guide

This document provides a technical walkthrough of how Mister Trader is put together. It covers everything from the database structure to the logical flow of the Telegram bot and the web dashboard. 

If you just need a broad overview of what the app does, please start with the main readme file. This guide is intended for those who want to understand the underlying mechanics or contribute to the project.

## Quick Start

To get the system running on your local machine, follow these three steps.

### 1. Start the Backend API
Use this command to launch the FastAPI server. It handles all the data processing and storage.
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

### 2. Start the Telegram Bot
While the API is running, start the bot script in a separate terminal. This will allow you to interact with the system via Telegram.
```bash
python -m app.telegram.bot
```

### 3. Start the React Frontend
Finally, go into the react directory and run the development server to see your dashboard.
```bash
cd react && npm run dev
```

---

## Project Architecture

```
mister-trader/
├── app/                     # Backend (FastAPI + Python)
│   ├── api/v1/             # REST API endpoints
│   ├── core/               # Config, database, storage
│   ├── models/             # SQLAlchemy models
│   ├── services/           # Business logic layer
│   ├── telegram/           # Telegram bot
│   │   ├── handlers/       # Message/callback handlers
│   │   ├── states/         # FSM state groups
│   │   └── utils/          # Bot utilities
│   └── utils/              # Shared utilities
├── react/                   # Frontend (Vite + React + Tailwind)
│   └── src/
│       ├── components/     # Reusable UI components
│       ├── pages/          # Page components
│       ├── hooks/          # Custom React hooks
│       └── utils/          # API client, helpers
├── alembic/                 # Database migrations
└── media/                   # Uploaded files
```

---

## Backend API (FastAPI)

### Core Configuration (`app/core/`)
- `config.py` - Environment variables and settings
- `database.py` - SQLAlchemy engine and session management
- `storage.py` - File upload/delete utilities

### Database Models (`app/models/`)
| Model | Purpose |
|-------|---------|
| `User` | Telegram user authentication |
| `Account` | Trading accounts/vaults |
| `Trade` | Individual trades with outcomes |
| `Strategy` | Trading strategies |
| `TradingPlan` | Daily trading plans |
| `UserStats` | Aggregated statistics |
| `Activity` | Daily activity logs |
| `TradePsychology` | Psychology notes per trade |
| `TradeMedia` | Screenshots/charts |
| `VoiceNote` | Voice recordings |
| `Reminder` | Notification settings |

### API Endpoints (`app/api/v1/`)
| Endpoint | Description |
|----------|-------------|
| `/api/v1/analytics/*` | Statistics, session data, performance |
| `/api/v1/strategies/*` | Strategy CRUD |
| `/api/v1/plans/*` | Trading plan CRUD |
| `/api/v1/trades/*` | Trade management |
| `/api/v1/export/trades/csv` | CSV export |

### Services (`app/services/`)
Business logic is separated from API routes:
- `analytics_service.py` - Statistics calculations
- `strategy_service.py` - Strategy management
- `trading_plan_service.py` - Plan management
- `export_service.py` - CSV generation
- `reminder_service.py` - Notification settings

---

## Telegram Bot (Aiogram)

### Handler Files (`app/telegram/handlers/`)
Each handler file manages a specific feature:

| Handler | Commands/Features |
|---------|-------------------|
| `auth_handlers.py` | `/start`, `/signup`, `/login` |
| `trade_handlers.py` | Trade logging, closing |
| `stats_handlers.py` | `/stats` - Statistics dashboard |
| `export_handlers.py` | `/export` - CSV export |
| `strategy_handlers.py` | `/strategy` - Strategy CRUD |
| `plan_handlers.py` | `/plan` - Trading plan CRUD |
| `psychology_handlers.py` | Psychology logging |
| `media_handlers.py` | Screenshot uploads |
| `voice_handlers.py` | Voice notes |
| `activity_handlers.py` | Daily activity |
| `account_handlers.py` | Account management |
| `menu_handlers.py` | Navigation menus |

### FSM States (`app/telegram/states/`)
Multi-step flows use Finite State Machine states:
- `StrategyStates` - Creating new strategies
- `PlanStates` - Creating trading plans
- `TradeStates` - Trade entry flow

### Bot Authentication
1. User sends `/signup` to create account with PIN
2. User sends `/login` to authenticate
3. Session persists in `fsm_storage.db` (SQLite)

---

## React Frontend

### Component Structure
```
src/
├── components/
│   ├── Sidebar.jsx      # Navigation sidebar
│   └── StatCard.jsx     # Statistics display card
├── pages/
│   ├── Dashboard.jsx    # Main dashboard with stats
│   ├── Trades.jsx       # Trade journal table
│   ├── Strategies.jsx   # Strategy management
│   ├── Plans.jsx        # Trading plans
│   └── Settings.jsx     # Configuration
├── hooks/
│   └── useApi.js        # API fetching hooks
└── utils/
    └── api.js           # API client
```

### API Client (`src/utils/api.js`)
Centralized API calls with authentication:
```javascript
import { api } from './utils/api'

// Get stats
const stats = await api.getStats()

// Get strategies
const strategies = await api.getStrategiesList()

// Export trades
api.exportTrades()  // Opens CSV download
```

### Custom Hooks (`src/hooks/useApi.js`)
```javascript
import { useApi, useMutation } from './hooks/useApi'

// Fetch data
const { data, loading, error, refetch } = useApi(api.getStats)

// Mutations
const { mutate, loading } = useMutation(api.createStrategy)
```

### Tailwind CSS Styling
- Soft, eye-friendly color palette
- Custom utility classes in `index.css`
- Responsive grid layouts

---

## Utilities

### Session Detection (`app/utils/session_utils.py`)
Automatically detects trading session from timestamp:
- **London**: 07:00 - 16:00 UTC
- **New York**: 12:00 - 21:00 UTC
- **Asian**: 00:00 - 09:00 UTC
- **Sydney**: 21:00 - 06:00 UTC
- **London/NY Overlap**: 12:00 - 17:00 UTC

### Trade Outcome (`app/utils/trade_utils.py`)
Determines WIN/LOSS/BREAKEVEN:
- BUY trades: Win if exit > entry
- SELL trades: Win if exit < entry

### Streak Tracking (`app/utils/streak_utils.py`)
Calculates current and best streaks from trade history.

### Validation (`app/utils/validation_utils.py`)
Validates trade entries:
- Symbol format
- Price ranges
- Stop loss/take profit logic

---

## Database

### SQLite Files
- `mister_trader.db` - Main application database
- `fsm_storage.db` - Telegram bot session storage

### Running Migrations
```bash
# Generate new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Or sync directly
python -c "from app.core.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | Yes |
| `SECRET_KEY` | JWT signing key | Yes |
| `DATABASE_URL` | SQLite path (hardcoded) | No |

---

## Debugging

### Backend Issues
1. Check workflow logs: `FastAPI Backend`
2. API docs: http://localhost:5000/docs
3. Health check: GET `/health`

### Bot Issues
1. Check workflow logs: `Telegram Bot`
2. Verify `TELEGRAM_BOT_TOKEN` is set
3. Check FSM storage: `fsm_storage.db`

### Frontend Issues
1. Check browser console
2. Verify API proxy in `vite.config.js`
3. Check network requests in DevTools

### Common Fixes
- **Bot not responding**: Restart Telegram Bot workflow
- **API 500 errors**: Check database migrations
- **Frontend blank**: Ensure Tailwind is configured

---

## Deployment

### Production Build (React)
```bash
cd react && npm run build
```

### Recommended Setup
1. Backend on port 5000 (Uvicorn with Gunicorn)
2. React as static files or separate deployment
3. Telegram bot as background process

---

## Key Data Flows

### Trade Entry Flow (Telegram)
1. User taps "New Trade" button
2. Bot asks for symbol → side → quantity → entry price
3. Trade saved as "pending"
4. Session auto-detected from timestamp
5. User can close trade later with exit price
6. Outcome calculated, stats updated

### Statistics Calculation
1. User requests `/stats`
2. `analytics_service.recalculate_user_stats()` runs
3. Aggregates all closed trades
4. Updates `UserStats` table
5. Returns formatted response

### Session Performance
Trades are tagged with session based on open timestamp.
Stats show win rate per session for comparison.

---

## Adding New Features

### New Telegram Handler
1. Create `app/telegram/handlers/feature_handlers.py`
2. Define router and handlers
3. Import in `app/telegram/bot.py`
4. Add to `register_all_handlers()`

### New API Endpoint
1. Create `app/api/v1/feature.py`
2. Define FastAPI router
3. Import in `app/main.py`
4. Add `app.include_router()`

### New React Page
1. Create `react/src/pages/Feature.jsx`
2. Add to navigation in `Sidebar.jsx`
3. Add case in `App.jsx` switch

---

## Summary

Mister Trader is a full-stack trading journal with:
- **FastAPI** backend with REST API
- **Telegram bot** for mobile trade logging
- **React + Tailwind** dashboard
- **SQLite** database for simplicity
- **Analytics** for session, strategy, and time analysis
- **Export** to CSV for external analysis

The system prioritizes user experience through the Telegram interface while providing a web dashboard for deeper analysis.
