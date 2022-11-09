# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup


class StorageUsers(StatesGroup):
    here_name = State()
    here_phone = State()
    here_yslyga = State()
