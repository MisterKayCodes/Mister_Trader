from aiogram.fsm.state import State, StatesGroup

class AccountStates(StatesGroup):
    """
    Rule 1: Defines the 'Known State' for the Account/Vault lifecycle.
    """
    waiting_for_name = State()          # Waiting for user to type a new Vault name
    waiting_for_switch_selection = State()  # Waiting for user to click a vault to switch
    waiting_for_delete_selection = State()  # Waiting for user to click a vault to delete
