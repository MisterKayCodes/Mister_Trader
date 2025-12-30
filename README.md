
# MisterTrader

**MisterTrader** is a trading journal backend with Telegram bot and React frontend.

## Setup

1. Create a Python virtual environment:

```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
````

2. Install dependencies:

```bash
pip install fastapi uvicorn
```

3. Run the server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. Visit `http://localhost:8000/health` to check health.

## Environment Variables

Copy `.env.example` to `.env` and fill in your Telegram Bot token and other configs.

```

---



```

mister_trader/
├── .gitignore
├── .env.example
└── README.md

```

---

