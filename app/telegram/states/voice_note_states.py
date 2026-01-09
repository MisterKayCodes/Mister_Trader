from aiogram.fsm.state import State, StatesGroup

class VoiceNoteStates(StatesGroup):
    """
    Rule 1: Defines states for attaching voice notes to trades.
    """
    waiting_for_trade_selection = State() # Selecting which trade to record for
    waiting_for_voice = State()           # Waiting for the actual audio/voice message
