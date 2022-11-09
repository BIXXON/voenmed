# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Кнопки при поиске профиля через админ-меню
open_profile_inl = InlineKeyboardMarkup(row_width=1)
input_kb = InlineKeyboardButton(text="Оставить заявку на бесплатную консультацию", callback_data="get_zayvka:Бесплатная консультация")#
inputm_kb = InlineKeyboardButton(text="Связаться в тг", url="t.me/lis9_9")
open_profile_inl.add(input_kb, inputm_kb)


