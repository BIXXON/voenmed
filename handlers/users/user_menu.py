# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from keyboards.default import check_user_out_func, all_back_to_main_default
from keyboards.default.menu import *
from keyboards.inline import *
from keyboards.inline.inline_page import *
from loader import dp, bot
from utils import send_all_admin, clear_firstname, get_dates
from states.state_users import *
from states.state_payment import *
from utils.other_func import clear_firstname, get_dates
import traceback
#from utils.db_api.sqlite import 


# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


# Обработка кнопки "Профиль"
@dp.message_handler(text="Бесплатная консультация", state="*")
async def show_profile(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Подайте заявку либо свяжитесь с нами в телеграме\n\nВ созвоне вы сможете обсудить все детали поэтому в приоритете оставлять заявку на звонок", reply_markup=open_profile_inl, parse_mode='HTML')


# Обработка кнопки "Поддержка"
@dp.message_handler(text="Частые вопросы", state="*")
async def show_contact(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    pd_kb = InlineKeyboardMarkup(row_width=2)
    pd_kb.add(InlineKeyboardButton(text="Что мы делаем?", callback_data="pd_kb:1"),InlineKeyboardButton(text="Какие гарантии?", callback_data="pd_kb:2"))
    pd_kb.add(InlineKeyboardButton(text="Официальны ли действия?", callback_data="pd_kb:3"),InlineKeyboardButton(text="Возможна ли рассрочка?", callback_data="pd_kb:4"))
    pd_kb.add(InlineKeyboardButton(text="Есть ли бесплатная консультация?", callback_data="pd_kb:5"))
    pd_kb.add(InlineKeyboardButton(text="А если не выявят диагноз?", callback_data="pd_kb:6"))
    await message.answer("""<b>Миссия МКЦ "ВОЕНМЕД"</b> - провести как можно большму количеству призывников качественное медицинское обследование для уточнения наличия или отсутсствия заболеваний, не сопоставимых со службой в Российской армии

<b>🔟 лет</b> - На страже призывников с 2012 г.
<b>2️⃣0️⃣0️⃣0️⃣ заболеваний</b> - Именно столько заболеваний существует в "Расписании болезней", дающих право на освобождение от службы в армии
<b>3️⃣0️⃣0️⃣➕</b> - Мы провели уже более 300 экспертиз по определению судов рзличных инстанций
""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')


@dp.callback_query_handler(text_startswith="return")
async def show_referral(call: CallbackQuery, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    pd_kb = InlineKeyboardMarkup(row_width=2)
    pd_kb.add(InlineKeyboardButton(text="Что мы делаем?", callback_data="pd_kb:1"),InlineKeyboardButton(text="Какие гарантии?", callback_data="pd_kb:2"))
    pd_kb.add(InlineKeyboardButton(text="Официальны ли действия?", callback_data="pd_kb:3"),InlineKeyboardButton(text="Возможна ли рассрочка?", callback_data="pd_kb:4"))
    pd_kb.add(InlineKeyboardButton(text="Есть ли бесплатная консультация?", callback_data="pd_kb:5"))
    pd_kb.add(InlineKeyboardButton(text="А если не выявят диагноз?", callback_data="pd_kb:6"))
    await call.message.edit_text("""<b>Миссия МКЦ "ВОЕНМЕД"</b> - провести как можно большму количеству призывников качественное медицинское обследование для уточнения наличия или отсутсствия заболеваний, не сопоставимых со службой в Российской армии

<b>🔟 лет</b> - На страже призывников с 2012 г.
<b>2️⃣0️⃣0️⃣0️⃣ заболеваний</b> - Именно столько заболеваний существует в "Расписании болезней", дающих право на освобождение от службы в армии
<b>3️⃣0️⃣0️⃣➕</b> - Мы провели уже более 300 экспертиз по определению судов рзличных инстанций
""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

@dp.callback_query_handler(text_startswith="get_zayvka", state="*")
async def show_referral(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await StorageUsers.here_name.set()
    async with state.proxy() as data:
        data["here_yslyga"] = call.data.split(":")[1]
    await call.message.delete()
    await bot.send_message(call.from_user.id, "➖➖➖➖➖➖➖➖➖➖➖")
    await bot.send_message(call.from_user.id, "Отправьте свои ФИО", reply_markup=all_back_to_main_default)


@dp.message_handler(state=StorageUsers.here_name)
async def get_promo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["here_name"] = message.text
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    await StorageUsers.here_phone.set()
    button_phone = types.KeyboardButton(text="Отправить телефон тг",
                                            request_contact=True)
    keyboard.add(button_phone)
    keyboard.row("⬅ На главную")
    await bot.send_message(message.chat.id, 'Отправте номер телефон',
                         reply_markup=keyboard)

@dp.message_handler(content_types=['contact'], state=StorageUsers.here_phone)
async def contact(message: types.Message, state: FSMContext):
    if message.contact is not None:
        await bot.send_message(message.from_user.id, 'Вы успешно отправили свой номер', reply_markup=all_back_to_main_default)
        phonenumber = str(message.contact.phone_number)
        user_id = str(message.contact.user_id)
        async with state.proxy() as data:
            data["here_phone"] = phonenumber
        here_status_kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        here_status_kb.add(InlineKeyboardButton(text="Я призывник", callback_data="get_status:призывник"))
        here_status_kb.add(InlineKeyboardButton(text="Я не призывник", callback_data="get_status:не призывник"))
        here_status_kb.add(InlineKeyboardButton(text="Пропустить", callback_data="get_status:неизвестно"))
        await bot.send_message(message.chat.id, 'Выберите ваш статус, это поможет нам подобрать для вас индивидуальный подход',
                         reply_markup=here_status_kb)

@dp.message_handler(state=StorageUsers.here_phone)
async def get_promo(message: types.Message, state: FSMContext):
    try:
        if int(message.text.replace("+", "").replace(" ", "").replace("-", "").replace(")", "").replace("(", "")) >= 10000000000:
            await bot.send_message(message.from_user.id, 'Вы успешно отправили свой номер', reply_markup=all_back_to_main_default)
            async with state.proxy() as data:
                data["here_phone"] = message.text
            here_status_kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
            here_status_kb.add(InlineKeyboardButton(text="Я призывник", callback_data="get_status:призывник"))
            here_status_kb.add(InlineKeyboardButton(text="Я не призывник", callback_data="get_status:не призывник"))
            here_status_kb.add(InlineKeyboardButton(text="Пропустить", callback_data="get_status:неизвестно"))
            await bot.send_message(message.chat.id, 'Выберите ваш статус, это поможет нам подобрать для вас индивидуальный подход',
                                 reply_markup=here_status_kb)
        else:
            await bot.send_message(message.chat.id, 'Вы неверно ввели номер телефона\n\nОтправте номер телефон')
    except:
        await bot.send_message(message.chat.id, 'Вы неверно ввели номер телефона\n\nОтправте номер телефон')


@dp.callback_query_handler(text_startswith="get_status", state="*")
async def pd_kb(call: CallbackQuery, state: FSMContext):
    status = call.data.split(":")[1]
    get_input = get_userx(user_id=call.from_user.id)
    async with state.proxy() as data:
        here_phone = data["here_phone"]
        here_name = data["here_name"]
        here_yslyga = data["here_yslyga"]
    await call.message.delete()
    delete_kb = InlineKeyboardMarkup(row_width=1)
    delete_kb.add(InlineKeyboardButton(text="Удалить", callback_data=f"delete:{call.from_user.id}"))
    await bot.send_message(call.from_user.id, 'Ваша заявка принята\nОжидайте звонка',
                         reply_markup=check_user_out_func(call.from_user.id))
    await send_all_admin(f"""<code>{here_yslyga}</code>
<a href='tg://user?id={get_input[1]}'>{get_input[3]}</a> (<code>{get_input[1]}</code>)

ФИО: <code>{here_name}</code>
Телефон: <code>{here_phone}</code>
Статус: <code>{status}</code>""", markup=delete_kb)
    await state.finish()

@dp.callback_query_handler(text_startswith="pd_kb", state="*")
async def pd_kb(call: CallbackQuery, state: FSMContext):
    await state.finish()
    id_v = int(call.data.split(":")[1])
    get_settings = get_settingsx()
    pd_rt = InlineKeyboardMarkup()
    pd_rt.add(InlineKeyboardButton(text="Назад", callback_data="return"))
    if id_v == 1:
        await call.message.edit_text("""Мы выполняем независимую военно-врачебную экспертизу и медицинское обследование на годность к военной службе для всех граждан РФ на основании медицинской лицензии, выданной Министерством Здравоохранения""", reply_markup=pd_rt, disable_web_page_preview=True, parse_mode='HTML')
    if id_v == 2:
        await call.message.edit_text("""У нас работают военные врачи в отставке с опытом работы в военкомате и проведения военно-врачебной комиссии от 6 лет, которые разработали собственную уникальную методику обследования, которая позволяет эффективно выявлять невидимые заболевания там, где их не может найти врач из обычной клиники""", reply_markup=pd_rt, disable_web_page_preview=True, parse_mode='HTML')
    if id_v == 3:
        await call.message.edit_text("""Мы не подкупаем должностных лиц, не производим подделки и 'не рисуем' диагнозов. Обращаясь к другим лицам или сомнительным компаниям, человек рискует обзавестись очень сертезными проблемами. Мы же работаем официально, поэтому вы с нами в безопасности.""", reply_markup=pd_rt, disable_web_page_preview=True, parse_mode='HTML')
    if id_v == 4:
        await call.message.edit_text("""Есть возможность получения внутренней рассрочки платежа, оплата которых производится через банк, что является гарантом нашей законности и надежности""", reply_markup=pd_rt, disable_web_page_preview=True, parse_mode='HTML')
    if id_v == 5:
        await call.message.edit_text("""Есть первичная бесплатная консультация для клиентов.""", reply_markup=pd_rt, disable_web_page_preview=True, parse_mode='HTML')
    if id_v == 6:
        await call.message.edit_text("""Если мы не выявим диагноз, который даёт вам право на получение военного билета, мы вернём вам часть оплаченной суммы""", reply_markup=pd_rt, disable_web_page_preview=True, parse_mode='HTML')


@dp.message_handler(text="Ошибки призывников", state="*")
async def show_contact(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    pd_kb = InlineKeyboardMarkup(row_width=3)
    pd_kb.add(InlineKeyboardButton(text="Последствия", callback_data="pos_kb:1"),InlineKeyboardButton(text="Далее➡️", callback_data="sled_kb:2"))
    await message.answer("""<b>ОШИБКА №1:</b> попытаться купить военный билет или дать взятку. 
Мошенничество - это получение военного билета в обход закона. Дача взятки должностному лицу преследуется по ст. 291 УК РФ и наказывается лишением свободы.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')


@dp.callback_query_handler(text_startswith="sled_kb", state="*")
async def pd_kb(call: CallbackQuery, state: FSMContext): 
    index = int(call.data.split(":")[1])
    pd_kb = InlineKeyboardMarkup(row_width=3)
    if index == 1:
        pd_kb.add(InlineKeyboardButton(text="Последствия", callback_data="pos_kb:1"),
            InlineKeyboardButton(text="Далее➡️", callback_data="sled_kb:2"))
        await call.message.edit_text("""<b>ОШИБКА №1:</b> попытаться купить военный билет или дать взятку. 

Мошенничество - это получение военного билета в обход закона. Дача взятки должностному лицу преследуется по ст. 291 УК РФ и наказывается лишением свободы.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 2:
        pd_kb.add(InlineKeyboardButton(text="⬅️Назад", callback_data="sled_kb:1"),
            InlineKeyboardButton(text="Последствия", callback_data="pos_kb:2"),
            InlineKeyboardButton(text="Далее➡️", callback_data="sled_kb:3"))
        await call.message.edit_text("""<b>ОШИБКА №2:</b> самостоятельно поставить диагноз.

Призывники сами пытаются определить свою категорию годности к военной службе, но очень часто ошибаются и рискуют отправиться в армию. Кроме того, некоторые заболевания может определить только опытный врач, который часто сталкивается с ним во время службы.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 3:
        pd_kb.add(InlineKeyboardButton(text="⬅️Назад", callback_data="sled_kb:2"),
            InlineKeyboardButton(text="Далее➡️", callback_data="sled_kb:4"))
        await call.message.edit_text("""<b>ОШИБКА №3:</b> слушать советчиков из интернета.

В СМИ, на форумах, в социальных сетях и на консультациях-профессионалов-призывника просто заваливают теорией и зачастую ошибочной, устаревшей. У каждого призывника своя ситуация и только практики с большим опытом работы могут дать действительно правильный совет.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 4:
        pd_kb.add(InlineKeyboardButton(text="⬅️Назад", callback_data="sled_kb:3"),
            InlineKeyboardButton(text="Далее➡️", callback_data="sled_kb:5"))
        await call.message.edit_text("""<b>ОШИБКА №4:</b> молчать на медкомиссии. 
Часто призывники боятся рассказать и предоставить на призывной комиссии свои диагнозы и по жаловаться на свое здоровье. Бояться этого не стоит, иначе вас признают здоровым и отправят слу жить несмотря на то, что у вас есть ряд заболеваний, который освобождает от призыва""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 5:
        pd_kb.add(InlineKeyboardButton(text="⬅️Назад", callback_data="sled_kb:4"),
            InlineKeyboardButton(text="Последствия", callback_data="pos_kb:5"))
        await call.message.edit_text("""<b>ОШИБКА №5:</b> сбежать из военкомата. 
Если молодого человека признали годным, а основание для отсрочки отсутствует, то призывнику вручается повестка на инструктаж и отправку. Многие призывники умудряются сбежать из военко мата. В этом случае призывник попадает под уголовную ответственность по ст. 328 УК РФ.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')


@dp.callback_query_handler(text_startswith="pos_kb", state="*")
async def pd_kb(call: CallbackQuery, state: FSMContext): 
    index = int(call.data.split(":")[1])
    pd_kb = InlineKeyboardMarkup(row_width=3)
    if index == 1:
        pd_kb.add(InlineKeyboardButton(text="Назад", callback_data="sled_kb:1"))
        await call.message.edit_text("""УК РФ Статья 291. Дача взятки.

Наказывается штрафом в размере до пятисот тысяч рублей, или в размере заработной платы или иного дохода осужденного за период до одного года, или в размере от пятикратной до тридцати кратной суммы взятки, либо исправительными работами на срок до двух лет с лишением права зани мать определенные должности или заниматься определенной деятельностью на срок до трех лет или без такового, либо принудительными работами на срок до трех лет, либо лишением свободы на срок до двух лет со штрафом в размере от пятикратной до десятикратной суммы взятки или без такового.""", reply_markup=pd_kb)

    if index == 2:
        pd_kb.add(InlineKeyboardButton(text="Назад", callback_data="sled_kb:2"))
        await call.message.edit_text("""УК РФ Статья 327. Подделка, изготовление или сбыт поддельных документов, государствен ных наград, штампов, печатей, бланков.

Наказывается ограничением свободы на срок до двух лет, либо принудительными работами на срок до двух лет, либо арестом на срок до шести месяцев, либо лишением свободы на срок до двух лет. """, reply_markup=pd_kb)

    if index == 5:
        pd_kb.add(InlineKeyboardButton(text="Назад", callback_data="sled_kb:5"))
        await call.message.edit_text(""" УК РФ Статья 328. Уклонение от прохождения военной и альтернативной гражданской службы. 

Наказывается штрафом в размере до двухсот тысяч рублей или в размере заработной платы или иного дохода осужденного за период до восемнадцати месяцев, либо принудительными работами на срок до двух лет, либо арестом на срок до шести месяцев, либо лишением свободы на срок до двух лет.""", reply_markup=pd_kb)


@dp.message_handler(text="Этапы обследования", state="*")
async def show_contact(message: types.Message, state: FSMContext):
    await state.finish()
    pd_kb = InlineKeyboardMarkup(row_width=2)
    pd_kb.add(InlineKeyboardButton(text=f"Шаг 2➡️", callback_data="sled_etap:2"))
    await message.answer("""<b>Шаг 1.</b> Первичная консультация призывников и их родителей по вопросам медицинского обследования на годность к военной службе происходит бесплатно. Выясняем ситуацию на настоящий момент с Военкоматом, рассказываем о этапах работы, обсуждаем фоки и стоимость услуг, отвечаем на все вопросы. При необходимости выдаем экземпляр договора на дом для ознакомления, чтобы призывник мог спокойно его изучить и принять «взвешенное» решение.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

@dp.callback_query_handler(text_startswith="sled_etap", state="*")
async def pd_kb(call: CallbackQuery, state: FSMContext): 
    index = int(call.data.split(":")[1])
    pd_kb = InlineKeyboardMarkup(row_width=3)
    if index == 1:
        pd_kb.add(InlineKeyboardButton(text=f"Шаг 2➡️", callback_data="sled_etap:2"))
        await call.message.edit_text("""<b>Шаг 1.</b> Первичная консультация призывников и их родителей по вопросам медицинского обследования на годность к военной службе происходит бесплатно. Выясняем ситуацию на настоящий момент с Военкоматом, рассказываем о этапах работы, обсуждаем фоки и стоимость услуг, отвечаем на все вопросы. При необходимости выдаем экземпляр договора на дом для ознакомления, чтобы призывник мог спокойно его изучить и принять «взвешенное» решение.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 2:
        pd_kb.add(InlineKeyboardButton(text=f"⬅️Шаг 1", callback_data="sled_etap:1"),InlineKeyboardButton(text=f"Шаг 3➡️", callback_data="sled_etap:3"))
        await call.message.edit_text("""<b>Шаг 2.</b>  Заключаем официальный договор, оплата договора проходит через банк.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 3:
        pd_kb.add(InlineKeyboardButton(text=f"⬅️Шаг 2", callback_data="sled_etap:2"),InlineKeyboardButton(text=f"Шаг 4➡️", callback_data="sled_etap:4"))
        await call.message.edit_text("""<b>Шаг 3.</b> Консультация врача-эксперта и знакомство с медицинской сестрой, которая будет сопровождать на протяжении всего обследования до уточнения наличия или отсутствия заболевания, дающего право на освобождение от службы в армии или отсрочки от призыва.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 4:
        pd_kb.add(InlineKeyboardButton(text=f"⬅️Шаг 3", callback_data="sled_etap:3"),InlineKeyboardButton(text=f"Шаг 5➡️", callback_data="sled_etap:5"))
        await call.message.edit_text("""<b>Шаг 4.</b> Врач-эксперт готовит индивидуальную программу независимого медицинского обследования с учетом предоставленных призывником медицинских документов и фактического физического состояния призывника.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 5:
        pd_kb.add(InlineKeyboardButton(text=f"⬅️Шаг 4", callback_data="sled_etap:4"),InlineKeyboardButton(text=f"Шаг 6➡️", callback_data="sled_etap:6"))
        await call.message.edit_text("""<b>Шаг 5.</b> Призывник проходит необходимое обследование до выявления диагноза по методике, позволяющей доказать соответствие диагноза требованием Военкомата.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 6:
        pd_kb.add(InlineKeyboardButton(text=f"⬅️Шаг 5", callback_data="sled_etap:5"),InlineKeyboardButton(text=f"Шаг 7➡️", callback_data="sled_etap:7"))
        await call.message.edit_text("""<b>Шаг 6.</b>  Врач-эксперт сопоставляет существующие заболевания на соответствие с Расписанием болезней (Приложение к Постановлению Правительства РФ от 4 июля 2013 гN 565 ред от 24.12.2021 г. Об утверждении Положения о военно-врачебной экспертизе), дающих право на освобождение призывника от службы в армии""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 7:
        pd_kb.add(InlineKeyboardButton(text=f"⬅️Шаг 6", callback_data="sled_etap:6"),InlineKeyboardButton(text=f"Шаг 8➡️", callback_data="sled_etap:8"))
        await call.message.edit_text("""<b>Шаг 7.</b> Призывник приходит в военкомат с документами и подтвержденным диагнозом. Мы полностью курируем этот процесс, при необходимости проводим независимую военно-врачебную экспертизу.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')

    if index == 8:
        pd_kb.add(InlineKeyboardButton(text=f"⬅️Шаг 7", callback_data="sled_etap:7"))
        await call.message.edit_text("""<b>Шаг 8.</b>  Призывник признается негодным к службе и получает военный билет в своем военкомате с указанием категории годности.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')    

@dp.message_handler(text="Услуги", state="*")
async def show_contact(message: types.Message, state: FSMContext):
    await state.finish()
    pd_kb = InlineKeyboardMarkup(row_width=1)
    pd_kb.add(InlineKeyboardButton(text=f"ОСНОВНОЙ", callback_data="osn_yslyga"))
    pd_kb.add(InlineKeyboardButton(text=f"НЕЗАВИСИМАЯ ВОЕННО-ВРАЧЕБНАЯ ЭКСПЕРТИЗА", callback_data="eksp_yslyga"))
    await message.answer("""Есть 2 тарифа:
Тариф <code>ОСНОВНОЙ</code>: Эта услуга для тех, кто хочет найти законные основания для получения военного билета
Стоимость услуги:  <code>62.000</code> руб.

<code>НЕЗАВИСИМАЯ ВОЕННО_ВРАЧЕБНАЯ ЭКСПЕРТИЗА</code>: Эта услуга для тех, кто не соглаен с заключением государственной военной комиссии.
Стоимость услуги:  <code>55.000</code> руб.

Доп. пакет <code>Медицина</code> к тарифу <code>ОСНОВНОЙ</code>: Этот тариф для тех кто не хочет стоять в очередях в поликлиниках, а хочет обследоваться у тех врачей, которые знают, как и что искать, а также не задают "ненужных" вопросов.
Стоимость услуги:  <code>25.000</code> руб.""", reply_markup=pd_kb, disable_web_page_preview=True, parse_mode='HTML')
   

@dp.callback_query_handler(text_startswith="osn_yslyga", state="*")
async def osn_yslyga(call: CallbackQuery, state: FSMContext): 
    open_profil = InlineKeyboardMarkup(row_width=1)
    input_kb = InlineKeyboardButton(text="Оформить заявку", callback_data="get_zayvka:Заявка на ОСНОВНОЙ тариф")#
    inputm_kb = InlineKeyboardButton(text="Связаться в тг", url="t.me/lis9_9")
    open_profil.add(input_kb, inputm_kb)
    await call.message.edit_text("""<b>Что входит в договор:</b>
☑️ Индивидуальные консультации врача.
☑️ Анализ медицинских документов и составление индивидуального плана обследования. Пошаговая инструкция.
☑️ Мед. сестра на связи 5 дней в неделю (с 9:00 до 18:00).

<b>Что не входит в договор:</b>
❌ Медицинские обследования (они оплачиваются отдельно в мед. учереждениях).

<b>Период: 3 месяца</b> | <b>Предусмотрена рассрочка и возврат оплаты</b>""", reply_markup=open_profil, parse_mode="HTML")

@dp.callback_query_handler(text_startswith="eksp_yslyga", state="*")
async def eksp_yslyga(call: CallbackQuery, state: FSMContext): 
    open_profil = InlineKeyboardMarkup(row_width=1)
    input_kb = InlineKeyboardButton(text="Оформить заявку", callback_data="НЕЗАВИСИМАЯ ВОЕННО-ВРАЧЕБНАЯ ЭКСПЕРТИЗА")#
    inputm_kb = InlineKeyboardButton(text="Связаться в тг", url="t.me/lis9_9")
    open_profil.add(input_kb, inputm_kb)
    await call.message.edit_text("""<b>Что входит в договор:</b>
☑️ Ознакомление с составом экспертов.
☑️ Первичное экспертное консультирование специалиста по военно-врачебной экспертизе с составлением плана обследования.
☑️ Мед. обследование, а также проведение необходимых лабораторных и диагностических иследований.
☑️ Экспертное консультирование вречей по результатам проведённых специальных исследований.
☑️ Заключительное экспертное онсультирование специалиста  по военно-врачебной экспертизе по итогам проведения независимой военно-врачебной экспертиизы.

<b>Период: 30 дней</b> | <b>не предусмотрена рассрочка и возврат оплаты</b>""", reply_markup=open_profil, parse_mode="HTML")


@dp.message_handler(text="Связаться в тг", state="*")
async def show_contact(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Для связи напишите менеджеру - <a href='tg://user?id=5256061002'>Иван</a>", parse_mode="HTML")