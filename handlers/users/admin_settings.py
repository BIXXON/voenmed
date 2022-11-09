# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities

from filters import IsAdmin
from keyboards.default import get_settings_func, all_back_to_main_default, check_user_out_func
from loader import dp
from states import StorageSettings
from utils.db_api.sqlite import *
from utils.other_func import send_all_admin, clear_firstname


# Обработка кнопки "Изменить Faq"
@dp.message_handler(IsAdmin(), text="ℹ Изменить отзывы 🖍", state="*")
async def change_faq(message: types.Message, state: FSMContext):
    await state.finish()
    get_faq = get_settingsx()
    await message.answer(f"<b>ℹ Текущий текст отзывов:</b>\n{get_faq[1]}", parse_mode='HTML')
    await message.answer("<b>🖍 Введите новый текст для отзывов</b>\n"
                         "❕ Вы можете использовать заготовленный синтаксис и HTML разметку:\n"
                         "▶ <code>{username}</code>  - логин пользоваля\n"
                         "▶ <code>{user_id}</code>   - айди пользовател\n"
                         "▶ <code>{firstname}</code> - имя пользователя", parse_mode='HTML')
    await StorageSettings.here_faq.set()


# Обработка кнопки "Изменить контакты"
@dp.message_handler(IsAdmin(), text="📕 Изменить контакты 🖍", state="*")
async def change_contact(message: types.Message, state: FSMContext):
    await state.finish()
    get_contact = get_settingsx()
    await message.answer(f"<b>📕 Текущие контакты:</b>\n{get_contact[0]}", parse_mode='HTML')
    await message.answer("🖍 Отправьте ID пользователя.\n"
                         "❕ Вводимый ID должен быть пользователем бота.", parse_mode='HTML')
    await StorageSettings.here_contact.set()


# Выключение покупок
@dp.message_handler(IsAdmin(), text="🔴 Выключить покупки", state="*")
async def turn_off_buy(message: types.Message, state: FSMContext):
    await state.finish()
    update_settingsx(status_buy="False")
    await message.answer("<b>🔴 Покупки в боте были выключены.</b>",
                         reply_markup=get_settings_func(), parse_mode='HTML')
    await send_all_admin(
        f"👤 Администратор <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
        "🔴 Выключил покупки в боте.", not_me=message.from_user.id, parse_mode='HTML')


# Включение покупок
@dp.message_handler(IsAdmin(), text="🟢 Включить покупки", state="*")
async def turn_on_buy(message: types.Message, state: FSMContext):
    await state.finish()
    update_settingsx(status_buy="True")
    await message.answer("<b>🟢 Покупки в боте были включены.</b>",
                         reply_markup=get_settings_func(), parse_mode='HTML')
    await send_all_admin(
        f"👤 Администратор <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
        "🟢 Включил покупки в боте.", not_me=message.from_user.id, parse_mode='HTML')


# Обработка кнопки "Отправить бота на тех. работы"
@dp.message_handler(IsAdmin(), text="🔴 Отправить на тех. работы", state="*")
async def send_bot_to_work(message: types.Message, state: FSMContext):
    await state.finish()
    update_settingsx(status="False")
    await message.answer("<b>🔴 Бот был отправлен на технические работы.</b>",
                         reply_markup=get_settings_func(), parse_mode='HTML')
    await send_all_admin(
        f"👤 Администратор <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
        "🔴 Отправил бота на технические работы.", not_me=message.from_user.id, parse_mode='HTML')


# Обработка кнопки "Вывести бота из тех. работ"
@dp.message_handler(IsAdmin(), text="🟢 Вывести из тех. работ", state="*")
async def return_bot_from_work(message: types.Message, state: FSMContext):
    await state.finish()
    update_settingsx(status="True")
    await message.answer("<b>🟢 Бот был выведен из технических работ.</b>",
                         reply_markup=get_settings_func(), parse_mode='HTML')
    await send_all_admin(
        f"👤 Администратор <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
        "🟢 Вывел бота из технических работ.", not_me=message.from_user.id)


# Принятие нового текста для faq
@dp.message_handler(IsAdmin(), state=StorageSettings.here_faq)
async def get_text_for_change_faq(message: types.Message, state: FSMContext):
    send_msg = message.text
    msg = message.text
    if "{username}" in msg:
        msg = msg.replace("{username}", f"<b>{message.from_user.username}</b>")
    if "{user_id}" in msg:
        msg = msg.replace("{user_id}", f"<b>{message.from_user.id}</b>")
    if "{firstname}" in msg:
        msg = msg.replace("{firstname}", f"<b>{clear_firstname(message.from_user.first_name)}</b>")
    try:
        await state.finish()
        await message.answer(f"ℹ Текст отзывов был обновлён ✅ Пример:\n{msg}",
                             reply_markup=get_settings_func(), parse_mode='HTML')
        update_settingsx(faq=send_msg)
    except CantParseEntities:
        await StorageSettings.here_faq.set()
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "🖍 Введите новый текст для отзывов", parse_mode='HTML')


# Принятие нового айди для контактов
@dp.message_handler(IsAdmin(), state=StorageSettings.here_contact)
async def get_id_for_change_contact(message: types.Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        get_status_user = get_userx(user_id=msg)
        if get_status_user is None:
            await StorageSettings.here_contact.set()
            await message.answer("<b>❌ Пользователь не был найден.</b>\n🖍 Отправьте ID пользователя.", parse_mode='HTML')
        else:
            await state.finish()
            msg = f"tg://user?id={msg}"
            update_settingsx(contact=msg)
            await message.answer(f"📕 Контакты были успешно обновлены ✅",
                                 reply_markup=get_settings_func())
    else:
        await StorageSettings.here_contact.set()
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "🖍 Отправьте ID пользователя.", parse_mode='HTML')


@dp.message_handler(IsAdmin(), text="📦Товар при выводе", state="*")
async def here_input_sber_min(message: types.Message, state: FSMContext):
    await state.finish()
    await StorageSettings.here_tovar.set()
    tovar = get_settingsp("tovar")
    await message.answer(f"""<b>Введите новый товар при выводе</b>
Текущий товар при выводе: <code>{tovar}</code>""",
                         reply_markup=all_back_to_main_default, parse_mode='HTML')

@dp.message_handler(IsAdmin(), state=StorageSettings.here_tovar)
async def here_input_sber_min(message: types.Message, state: FSMContext):
    new_tovar = message.text
    await state.finish()
    update_settingsx(tovar=new_tovar)
    await message.answer("Товар при выводе изменена",
                             reply_markup=get_settings_func(), parse_mode='HTML')

@dp.message_handler(IsAdmin(), text="🔁Изменить комиссию", state="*")
async def here_input_sber_min(message: types.Message, state: FSMContext):
    await state.finish()
    await StorageSettings.here_com.set()
    com = get_settingsp("com")
    await message.answer(f"""<b>Введите комиссию при выводе</b>
Текущая комиссия при выводе: <code>{com}</code>""",
                         reply_markup=all_back_to_main_default, parse_mode='HTML')

@dp.message_handler(IsAdmin(), state=StorageSettings.here_com)
async def here_input_sber_min(message: types.Message, state: FSMContext):
    try:
        com = int(message.text)
        update_settingsx(com=com)
        await message.answer("Комиссия при выводе изменена",
                                 reply_markup=get_settings_func(), parse_mode='HTML')
        await state.finish()
    except:
        await message.answer("Неверно введена комиссия", parse_mode='HTML')

@dp.message_handler(IsAdmin(), text="💹Изменить курс", state="*")
async def here_input_sber_min(message: types.Message, state: FSMContext):
    await state.finish()
    await StorageSettings.here_curs.set()
    curs = get_settingsp("curs")
    await message.answer(f"""<b>Введите курс</b>
Текущий курс: <code>{curs}</code>""",
                         reply_markup=all_back_to_main_default, parse_mode='HTML')

@dp.message_handler(IsAdmin(), state=StorageSettings.here_curs)
async def here_input_sber_min(message: types.Message, state: FSMContext):
    try:
        curs = float(message.text.replace(" ", "").replace(",", "."))
        update_settingsx(curs=curs)
        await message.answer("Курс изменён",
                                 reply_markup=get_settings_func(), parse_mode='HTML')
        await state.finish()
    except:
        await message.answer(f"""<b>Неверно введён курс курс</b>
Текущий курс: <code>{curs}</code>""", parse_mode='HTML')


@dp.message_handler(IsAdmin(), text="Изменить канал", state="*")
async def payments_systems(message: types.Message, state: FSMContext):
    await state.finish()
    canal = get_settingsp("canal")
    await message.answer(f"""Введите id канала без @ и tg.com/
текущий канал: {canal}""", reply_markup=all_back_to_main_default)
    await StorageSettings.here_canal.set()

@dp.message_handler(state=StorageSettings.here_canal)
async def here_canal(message: types.Message, state: FSMContext):
    msg = message.text.replace("@", "")
    update_settingsx(canal=msg)
    await message.answer(f"""Канал изменён
текущий канал: {msg}""", reply_markup=check_user_out_func(message.from_user.id), parse_mode='HTML')
    await state.finish()