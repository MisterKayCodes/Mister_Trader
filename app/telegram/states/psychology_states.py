from aiogram.fsm.state import State, StatesGroup

class PsychologyStates(StatesGroup):
    waiting_for_trade_selection = State()
    waiting_for_discipline = State()
    waiting_for_confidence = State()
    waiting_for_decision_quality = State()
    waiting_for_emotions = State()
    waiting_for_market_condition = State()
    waiting_for_volatility = State()
    waiting_for_plan_check = State()
    waiting_for_notes = State()
