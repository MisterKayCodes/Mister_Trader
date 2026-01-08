from aiogram.fsm.state import State, StatesGroup

class MediaStates(StatesGroup):
    waiting_for_trade_selection = State()
    waiting_for_media_type = State()
    waiting_for_file = State()
