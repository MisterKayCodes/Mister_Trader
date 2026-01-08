from aiogram.fsm.state import State, StatesGroup

class TradeStates(StatesGroup):
    """
    Defines the multi-step form (FSM) for creating a trade.
    """
    waiting_for_symbol = State()
    waiting_for_side = State()        # BUY or SELL
    waiting_for_quantity = State()
    waiting_for_entry_price = State()
    
    waiting_for_trade_selection = State()
     
    waiting_for_exit_price = State()     
    waiting_for_modify_selection = State() 
    waiting_for_field_selection = State()   
    waiting_for_new_value = State() 
