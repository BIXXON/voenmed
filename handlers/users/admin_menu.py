# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from filters import IsAdmin
from keyboards.default import get_settings_func, payment_default, get_functions_func, items_default, admins, all_back_to_main_default
from keyboards.inline import choice_way_input_payment_func, promo_key, get_u
from loader import dp, bot
from states.state_items import StoragePosition
from utils import get_dates
from utils.db_api.sqlite import *


# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


# Обработка кнопки "Платежные системы"
@dp.message_handler(IsAdmin(), text="🔑 Платежные системы", state="*")
async def payments_systems(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🔑 Настройка платежных системы.", reply_markup=payment_default(), parse_mode='HTML')
    await message.answer("🥝 Выберите способ пополнения 💵\n"
                         "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                         "🔸 <a href='https://vk.cc/bYjKGM'><b>По форме</b></a> - <code>Готовая форма оплаты QIWI</code>\n"
                         "🔸 <a href='https://vk.cc/bYjKEy'><b>По номеру</b></a> - <code>Перевод средств по номеру телефона</code>\n"
                         "🔸 <a href='https://vk.cc/bYjKJk'><b>По никнейму</b></a> - "
                         "<code>Перевод средств по никнейму (пользователям придётся вручную вводить комментарий)</code>",
                         reply_markup=choice_way_input_payment_func(), parse_mode='HTML')


# Обработка кнопки "Настройки бота"
@dp.message_handler(IsAdmin(), text="⚙ Настройки", state="*")
async def settings_bot(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("⚙ Основные настройки бота.", reply_markup=get_settings_func(), parse_mode='HTML')


# Обработка кнопки "Общие функции"
@dp.message_handler(IsAdmin(), text="🔆 Общие функции", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🔆 Выберите нужную функцию.", reply_markup=get_functions_func(message.from_user.id), parse_mode='HTML')


# Обработка кнопки "Общие функции"
@dp.message_handler(IsAdmin(), text="📰 Информация о боте", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    about_bot, lenn = get_about_bot(0)
    key_about = get_u(0, lenn)
    try:
        await message.answer(about_bot, reply_markup = get_u, parse_mode='HTML')
    except:
        await message.answer(about_bot, parse_mode='HTML')

@dp.callback_query_handler(text_startswith="next_about", state="*")
async def next_about(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    await state.finish()
    about_bot = get_about_bot(0)
    key_about = get_u(0)
    try:
        await call.message.edit_text(about_bot, reply_markup = get_u, parse_mode='HTML')
    except:
        await call.message.edit_text(about_bot, parse_mode='HTML')


# Обработка кнопки "Управление товарами"
@dp.message_handler(IsAdmin(), text="🎁 Управление товарами 🖍", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🎁 Редактирование товаров, разделов и категорий 📜",
                         reply_markup=items_default, parse_mode='HTML')


# Получение БД
@dp.message_handler(IsAdmin(), text="/getbd", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    for admin in admins:
        with open("data/botBD.sqlite", "rb") as doc:
            await bot.send_document(admin,
                                    doc,
                                    caption=f"<b>📦 BACKUP</b>\n"
                                            f"<code>🕜 {get_dates()}</code>", parse_mode='HTML')


def get_about_bot(remover):
    show_profit_all, show_profit_day, show_refill, show_buy_day, show_money_in_bot, show = 0, 0, 0, 0, 0, 0
    get_settings = get_settingsx()
    all_purchases = get_all_purchasesx()
    all_users = get_all_usersx()
    all_refill = get_all_refillx()
    show_users = get_all_usersx()
    show_users.reverse()
    lenn = len(show_users)
    top_don = ""
    for i in range(remover,remover+20):
        try:
            top_don += f"{i+1}. <a href='tg://user?id={show_users[i][1]}'>{show_users[i][3]}</a> - {show_users[i][8]} G\n"
        except:
            break
    show_categories = get_all_categoriesx_creat()
    show_positions = get_all_positionsx()
    show_items = get_all_itemsx()
    for purchase in all_purchases:
        show_profit_all += int(purchase[6])
        if int(get_settings[4]) - int(purchase[14]) < 86400:
            show_profit_day += int(purchase[6])
    for user in all_users:
        show_money_in_bot += int(user[4])
    for refill in all_refill:
        show_refill += int(refill[5])
        if int(get_settings[5]) - int(refill[9]) < 86400:
            show_buy_day += int(refill[5])
    message = f"""<b>📰 ВСЯ ИНФОРАМЦИЯ О БОТЕ</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>🔶 Пользователи: 🔶</b>
👤 Пользователей: <code>{len(show_users)}</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
🥝 Пополнено: <code>{show_refill}руб</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>🔶 Топ донатеров: 🔶</b>
{top_don}
"""
    return message, lenn


# Получение списка всех товаров
@dp.message_handler(IsAdmin(), text="/getitems", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_itemsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>🎁 Все товары</b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             "<code>📍 айди товара - данные товара</code>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n", parse_mode='HTML')
        for item in get_items:
            save_items.append(f"<code>📍 {item[1]} - {item[2]}</code>")
        if len_items >= 20:
            count_split = round(len_items / 20)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message, parse_mode='HTML')
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message, parse_mode='HTML')
    else:
        await message.answer("<b>🎁 Товары отсутствуют</b>", parse_mode='HTML')


# Получение списка всех позиций
@dp.message_handler(IsAdmin(), text="/getposition", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_positionsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>📁 Все позиции</b>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n", parse_mode='HTML')
        for item in get_items:
            save_items.append(f"<code>{item[2]}</code>")
        if len_items >= 35:
            count_split = round(len_items / 35)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message, parse_mode='HTML')
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message, parse_mode='HTML')
    else:
        await message.answer("<b>📁 Позиции отсутствуют</b>", parse_mode='HTML')


# Получение подробного списка всех товаров
@dp.message_handler(IsAdmin(), text="/getinfoitems", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_itemsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>🎁 Все товары и их позиции</b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n", parse_mode='HTML')
        for item in get_items:
            get_position = get_positionx("*", position_id=item[3])
            save_items.append(f"<code>{get_position[2]} - {item[2]}</code>")
        if len_items >= 20:
            count_split = round(len_items / 20)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message, parse_mode='HTML')
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message, parse_mode='HTML')
    else:
        await message.answer("<b>🎁 Товары отсутствуют</b>", parse_mode='HTML')

@dp.callback_query_handler(IsAdmin(), text_startswith="delete", state="*")
async def pd_kb(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Заявка удалена <code>{call.data.split(':')[1]}</code>", parse_mode="HTML")
