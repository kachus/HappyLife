from aiogram.filters.state import State, StatesGroup


class FSMQMainProcess(StatesGroup):
    first = State()
    second = State()
    third = State()
    fourth = State()
