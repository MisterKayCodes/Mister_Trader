# Mister Trader

Mister Trader is a specialized tool designed to help traders keep a focused and meaningful record of their activity. It combines the convenience of a Telegram bot for quick data entry with a detailed web dashboard for deep analysis of performance and habits.

The project was built to solve the common problem of fragmented trading data. By allowing you to log trades and thoughts directly from your phone while providing a professional interface for review, it helps bridge the gap between execution and reflection.

## Core Capabilities

The system is built around three main parts that work together to give you a complete picture of your trading.

### Telegram Companion
The bot acts as your personal assistant. You can use it to open and close trades, record voice notes about your current mindset, and upload screenshots of your charts. It also handles basic administrative tasks like signing up or viewing your current statistics. 

One of the most useful features is the automatic session detection. When you log a trade, the system identifies if you were trading during London, New York, or Asian hours. This helps you figure out when you are most effective without manual tagging.

### Performance Analytics
Beyond simple win and loss tracking, the app analyzes your data to find patterns. It tracks your winning and losing streaks, compares your performance across different strategies, and identifies which days of the week or hours of the day generate your best results.

### Psychology Tracking
Successful trading is often about mindset. This project allows you to record your emotional state and discipline levels for every trade. You can log whether you followed your plan, how confident you felt, and what the market conditions were like. This data is then used to provide insights into how your psychology affects your bottom line.

### Media and Voice Notes
You can attach images and voice recordings to your trades. The voice notes are particularly helpful for capturing the fast moving thoughts you have during a live session. These recordings can be played back directly from the web dashboard during your weekend review.

## Architecture

The technical side of the project consists of a FastAPI backend using a Python based environment. It stores data in a simple and portable SQLite database. The frontend is built with React and provides a clean, modern interface for all your data.

## Getting Started

To get the project running locally, you will need Python and Node.js installed on your system. 

1. Setup your environment by creating a file for your Telegram bot token.
2. Start the backend api using the provided uvicorn command.
3. Launch the Telegram bot script to start receiving messages.
4. Run the React development server to access the web dashboard.

For more detailed technical information and a full list of commands, please refer to the instructions file included in the repository.
