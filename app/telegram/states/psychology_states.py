from aiogram.fsm.state import State, StatesGroup

class PsychologyStates(StatesGroup):
    waiting_for_trade_selection = State()
    waiting_for_discipline = State()
    waiting_for_confidence = State()
    waiting_for_plan_check = State()
    waiting_for_notes = State()
