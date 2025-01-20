from aiogram.fsm.state import State, StatesGroup

class Holat(StatesGroup):
    get_firstname = State()
    get_lastname = State()
    check_data = State()