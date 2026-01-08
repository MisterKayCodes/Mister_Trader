from datetime import datetime, time
from typing import Optional


TRADING_SESSIONS = {
    "SYDNEY": {
        "start": time(21, 0),
        "end": time(6, 0),
        "overlap_next_day": True
    },
    "ASIAN": {
        "start": time(0, 0),
        "end": time(9, 0),
        "overlap_next_day": False
    },
    "LONDON": {
        "start": time(7, 0),
        "end": time(16, 0),
        "overlap_next_day": False
    },
    "NEWYORK": {
        "start": time(12, 0),
        "end": time(21, 0),
        "overlap_next_day": False
    }
}


def detect_trading_session(utc_timestamp: datetime) -> Optional[str]:
    if utc_timestamp is None:
        return None
    
    trade_time = utc_timestamp.time()
    
    if time(7, 0) <= trade_time < time(12, 0):
        return "LONDON"
    elif time(12, 0) <= trade_time < time(17, 0):
        return "LONDON_NY"
    elif time(17, 0) <= trade_time < time(21, 0):
        return "NEWYORK"
    elif time(21, 0) <= trade_time or trade_time < time(0, 0):
        return "SYDNEY"
    elif time(0, 0) <= trade_time < time(7, 0):
        return "ASIAN"
    
    return "OFF_HOURS"


def get_session_display_name(session: str) -> str:
    names = {
        "LONDON": "London",
        "LONDON_NY": "London/NY Overlap",
        "NEWYORK": "New York",
        "SYDNEY": "Sydney",
        "ASIAN": "Asian",
        "OFF_HOURS": "Off Hours"
    }
    return names.get(session, session)


def get_hour_bucket(utc_timestamp: datetime) -> int:
    if utc_timestamp is None:
        return -1
    return utc_timestamp.hour


def format_session_stats(session_data: dict) -> str:
    lines = []
    for session, stats in session_data.items():
        total = stats.get("wins", 0) + stats.get("losses", 0)
        if total > 0:
            win_rate = (stats["wins"] / total) * 100
            lines.append(f"{get_session_display_name(session)}: {win_rate:.1f}% ({stats['wins']}W / {stats['losses']}L)")
    return "\n".join(lines) if lines else "No session data yet"
