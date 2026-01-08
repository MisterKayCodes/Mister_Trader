from aiogram.fsm.state import State, StatesGroup

class ActivityStates(StatesGroup):
    waiting_for_activity_type = State()
    waiting_for_date = State()
    waiting_for_filter_date = State()
