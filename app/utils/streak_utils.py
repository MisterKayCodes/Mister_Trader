from typing import List, Tuple


def calculate_streak(outcomes: List[str]) -> Tuple[int, str]:
    if not outcomes:
        return 0, None
    
    current_type = None
    current_count = 0
    
    for outcome in reversed(outcomes):
        if outcome not in ("WIN", "LOSS"):
            continue
        
        if current_type is None:
            current_type = outcome
            current_count = 1
        elif outcome == current_type:
            current_count += 1
        else:
            break
    
    return current_count, current_type


def calculate_best_streaks(outcomes: List[str]) -> Tuple[int, int]:
    best_win = 0
    best_loss = 0
    current_win = 0
    current_loss = 0
    
    for outcome in outcomes:
        if outcome == "WIN":
            current_win += 1
            current_loss = 0
            best_win = max(best_win, current_win)
        elif outcome == "LOSS":
            current_loss += 1
            current_win = 0
            best_loss = max(best_loss, current_loss)
        else:
            current_win = 0
            current_loss = 0
    
    return best_win, best_loss


def format_streak_display(count: int, streak_type: str) -> str:
    if count == 0 or streak_type is None:
        return "No active streak"
    
    emoji = "🔥" if streak_type == "WIN" else "❄️"
    label = "winning" if streak_type == "WIN" else "losing"
    
    return f"{emoji} {count} trade {label} streak"
