# Mister Trader

A comprehensive trading journal and management system with a FastAPI backend, React frontend, and a Telegram bot interface.

## 🚀 Features

- **Trading Journal:** Log, track, and manage your trades across multiple vaults (accounts).
- **Telegram Bot:** Full-featured bot for logging trades, recording voice notes, and checking psychology stats on the go.
- **Psychology Tracking:** Monitor your emotional state and plan adherence to improve discipline.
- **Media Management:** Attach screenshots and voice notes to your trades for better post-trade analysis.
- **Modern Tech Stack:** FastAPI, SQLAlchemy, Alembic, Aiogram, React (Vite + Tailwind CSS).

## 🛠️ Project Structure

- `app/`: FastAPI backend application.
  - `api/v1/`: REST API endpoints.
  - `telegram/`: Telegram bot logic and handlers.
  - `models/`: SQLAlchemy database models.
  - `services/`: Business logic services.
- `react/`: Frontend application (Vite + React + Tailwind).
- `media/`: Storage for images and voice notes.
- `mister_trader.db`: Main SQLite database.

## ⚙️ Setup & Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   cd react && npm install
   ```

2. **Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token
   DATABASE_URL=sqlite:///./mister_trader.db
   SECRET_KEY=your_secret_key
   BACKEND_API_URL=http://0.0.0.0:8000
   ```

3. **Run the Backend:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

4. **Run the Telegram Bot:**
   ```bash
   python -m app.telegram.bot
   ```

5. **Run the Frontend:**
   ```bash
   cd react && npm run dev
   ```

## 🤖 Telegram Bot Commands

- `/start` - Initialize the bot and see the main menu.
- `/signup` - Register a new account.
- `/login` - Log in to your existing account.

## 📝 License

MIT License
