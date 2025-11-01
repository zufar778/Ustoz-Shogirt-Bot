from aiogram.fsm.state import State, StatesGroup

class Step(StatesGroup):
    activity = State()
    language = State()
    send = State()