# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from data.config import admins


def check_user_out_func(user_id):
    menu_default = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_default.row("Бесплатная консультация")
    menu_default.row("Услуги", "Связаться в тг")
    menu_default.row("Частые вопросы", "Ошибки призывников")
    menu_default.row("Этапы обследования")
    if str(user_id) in admins:
        menu_default.row("📰 Информация о боте")
        menu_default.row("Изменить канал")
        menu_default.row("⚙ Настройки", "🔆 Общие функции")
    return menu_default


all_back_to_main_default = ReplyKeyboardMarkup(resize_keyboard=True)
all_back_to_main_default.row("⬅ На главную")

