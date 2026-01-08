# Mister Trader

A comprehensive trading journal and management system with FastAPI backend, React frontend, and Telegram bot interface.

## Features

- **Trade Logging** - Log trades via Telegram bot with automatic session detection
- **Performance Analytics** - Win rate, P&L, session comparison, strategy effectiveness
- **Session Tracking** - Automatic detection of London, NY, Asian, Sydney sessions
- **Strategy Management** - Define and track multiple trading strategies
- **Trading Plans** - Create daily trading plans with bias, watchlist, mental state
- **Streak Tracking** - Current and best win/loss streaks
- **Time Analysis** - Best performing hours and sessions
- **CSV Export** - Export all trade data for external analysis
- **React Dashboard** - Modern web interface for data visualization
- **Psychology Tracking** - Monitor emotional state and plan adherence
- **Media Management** - Attach screenshots and voice notes to trades

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Telegram Bot Token

### 1. Set Environment Variables
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

### 2. Start Backend
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

### 3. Start Telegram Bot
```bash
python -m app.telegram.bot
```

### 4. Start React Frontend (Optional)
```bash
cd react
npm install
npm run dev
```

## Telegram Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/signup` | Create account with PIN |
| `/login` | Authenticate session |
| `/stats` | View trading statistics |
| `/export` | Download trades as CSV |
| `/strategy` | Manage trading strategies |
| `/plan` | Create/view trading plans |

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Bot**: Aiogram 3.x with FSM
- **Frontend**: React, Vite, Tailwind CSS
- **Database**: SQLite (mister_trader.db)

## Project Structure

```
├── app/
│   ├── api/v1/          # REST endpoints
│   ├── core/            # Config, database
│   ├── models/          # SQLAlchemy models
│   ├── services/        # Business logic
│   ├── telegram/        # Bot handlers
│   └── utils/           # Utilities
├── react/               # React frontend
├── alembic/             # Migrations
└── media/               # Uploads
```

## API Documentation

Visit `/docs` when the backend is running for interactive API documentation.

## Documentation

See [INSTRUCTIONS.md](./INSTRUCTIONS.md) for detailed project documentation including:
- Complete architecture overview
- Handler and service documentation
- Debugging guide
- Deployment instructions

## License

MIT
