from aiogram.fsm.state import State, StatesGroup

class AccountStates(StatesGroup):
    """
    Rule 1: Defines the 'Known State' for the Account/Vault lifecycle.
    """
    waiting_for_name = State()  # The bot is waiting for the user to type a Vault name
