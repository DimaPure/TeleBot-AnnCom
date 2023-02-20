import asyncio
import datetime
import time

from aiogram.utils.exceptions import MessageToDeleteNotFound
import aiogram.utils.markdown as md
import psycopg2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InputFile, ParseMode, \
    WebAppInfo, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.exceptions import CantInitiateConversation
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from text_bt import link
from keyboards import bt_sec

from config import CHANNEL_ID

from main import bot, dp

hotOffer = 'https://tgtest.sahome.ru/hotOffer'
index = "https://tgtest.sahome.ru/"


# ----------Возврат меню------------------
@dp.callback_query_handler(text=['Menu'])
async def main_menu(message: types.Message):
    kb1 = types.InlineKeyboardMarkup()
    kb1.insert(types.InlineKeyboardButton(text="Бесплатная консультация", callback_data="Konsult"))
    kb1.add(types.InlineKeyboardButton(text="О компании", callback_data="Company"))
    kb1.insert(types.InlineKeyboardButton(text="Собрать 🤖", callback_data="robot"))
    kb1.add(types.InlineKeyboardButton(text="🤖 в коробке", web_app=WebAppInfo(
        url=index)))
    kb1.insert(types.InlineKeyboardButton(text="🔥Предожение", web_app=WebAppInfo(
        url=hotOffer)))
    kb1.add(types.InlineKeyboardButton(text="Про бот N.", callback_data="bot_info"))
    kb1.insert(types.InlineKeyboardButton(text="Контакты", callback_data="contacts"))
    kb1.add(types.InlineKeyboardButton(text="Поделится", switch_inline_query='https://t.me/practicIST_bot'))
    await bot.send_photo(message.from_user.id, InputFile("pic/icon.jpg"), reply_markup=kb1, caption=f'''🤖 Автодайлер «Бот N.»
    Голосовой робот-помощник для бизнеса

    🔥передает голосовые сообщения, распознает ответы Человека, анализирует и умеет вести диалог
    🔥умный секретарь для входящих звонков

    ✓ оповещение об акциях
    ✓ приглашение на вебинар/мероприятие
    ✓ проведение опросов, анкетирование
    ✓ фильтрация базы номеров
    ✓ повышение лояльности клиентов
    ✓ лидогенерация и многое другое…
    _____
    {message.from_user.first_name}, выберите пункт меню 👇🏻''', )
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except (Exception, Error, AttributeError):
                print('Нужные сообщеньки стёрлись')


# ----------------- Консультация------------------------
def konsult():
    class FormKonsult(StatesGroup):
        klient_message = State()

    @dp.callback_query_handler(text="Konsult")
    async def answer_k(message: types.message, state: FSMContext):
        button_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
        cancelButton = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)
        await FormKonsult.klient_message.set()
        await bot.send_message(message.from_user.id, f'''
✉️<strong>{message.from_user.first_name}, отправьте текст своего сообщения</strong> 👇🏻''',
                               parse_mode=ParseMode.HTML, reply_markup=cancelButton)

    @dp.message_handler(state='*', commands='cancel')
    @dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
    async def cancel(message: types.message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return

        await state.finish()
        await bot.send_message(message.from_user.id, text='''🔥 Бот N — голосовой помощник от ANNCOM
    _____''', reply_markup=bt_sec)
     
        await main_menu(message)

    @dp.message_handler(state=FormKonsult.klient_message)
    async def text_user(callback: types.callback_query, state: FSMContext):
        async with state.proxy() as data:
            data['klient_message'] = callback.text

            await bot.send_message(CHANNEL_ID, md.text(md.text('<b>📩 Консультация</b>'),
                                                       md.text(''),
                                                       md.text(f'<b>TG user id: {callback.from_user.id} </b>'),
                                                       md.text(
                                                           f'<b>TG first name: {callback.from_user.first_name} </b>'),
                                                       md.text(f'<b>TG last name: {callback.from_user.last_name} </b>'),
                                                       md.text(f'<b>TG user name: @{callback.from_user.username} </b>'),
                                                       md.text(''),
                                                       md.text(f'🗓<b>дата:{datetime.date.today()} </b>'),
                                                       md.text(
                                                           f'⏰<b>время:{datetime.datetime.now().strftime("%H:%M:%S")} </b>'),
                                                       md.text(f'_____'),
                                                       md.text('👨', f"<b> {(data['klient_message'])}</b>"),
                                                       sep='\n'))
            await bot.send_message(CHANNEL_ID, f"@{callback.from_user.username}, {callback.from_user.id}")
        await state.finish()
        await bot.send_message(callback.from_user.id,
                               f"{callback.from_user.first_name}, <b> Вы успешно отпрвили личноее сообщение. <u>Ожидайте ответа</u>\n\nСпасибо!🤝</b>",
                               reply_markup=bt_sec)
        await asyncio.sleep(2)
        await bot.delete_message(callback.chat.id, callback.message_id-1)
        await main_menu(callback)


# ------------------------------------------------------------------------------------------------------------------------------------------


# --------------------Поддержка------------------------------
class FormSos(StatesGroup):
    message_bot = State()
    answer_admin = State()


@dp.message_handler(text=['🆘|Помощь'])
async def post(message: types.Message):
    button_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
    cancelButton = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)
    await FormSos.message_bot.set()
    await bot.send_message(message.from_user.id,
                           f'''{message.from_user.first_name}, какой у Вас вопрос❓
📝 Опишите максимально подробно возникшую проблему, чем подробнее Вы опишите возникшую проблему, тем быстрее и качественнее мы сможем помочь Вам 👇🏻
''', reply_markup=cancelButton)


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel(message: types.message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await bot.send_message(message.from_user.id, text='''🔥 Бот N — голосовой помощник от ANNCOM
_____''', reply_markup=bt_sec)

    await state.finish()
    await main_menu(message)
    try:    
            for delit in range(1,20):
                await bot.delete_message(message.chat.id, message.message_id-delit)
    except (Exception, Error, MessageToDeleteNotFound):
            print('Нужные сообщеньки стёрлись')


@dp.message_handler(state=FormSos.message_bot)
async def user_text(callback: types.callback_query, state: FSMContext):
    async with state.proxy() as data:
        data['klient_message'] = callback.text

        await bot.send_message(CHANNEL_ID,
                               md.text(md.text('📩 <strong>ПОДДЕРЖКА</strong>'),
                                       md.text(''),
                                       md.text(
                                           f'<b>TG user id: {callback.from_user.id}</b>'),
                                       md.text(
                                           f'<b>TG first name: {callback.from_user.first_name}</b>'),
                                       md.text(
                                           f'<b>TG last name: {callback.from_user.last_name}</b>'),
                                       md.text(
                                           f'<b>TG user name: @{callback.from_user.username}</b>'),
                                       md.text(''),
                                       md.text(
                                           f'⭐️<b>дата:{datetime.date.today()}</b>'),
                                       md.text(
                                           f'⭐️<b>время:{datetime.datetime.now().time()}</b>'),
                                       md.text(f'_____'),
                                       md.text(
                                           f"🆘\n<b>{data['klient_message']}</b>"),
                                       sep='\n'))
        await state.finish()
        await bot.send_message(CHANNEL_ID, f"@{callback.from_user.username}, {callback.from_user.id}")
        await asyncio.sleep(2)
        await bot.send_message(callback.from_user.id, "В скором времени с вами свяжутся.\n\nСпасибо!🤝",
                               reply_markup=bt_sec)
        await asyncio.sleep(1)
        await main_menu(callback)
        try:    
            for delit in range(1,3):
                await bot.delete_message(callback.chat.id, callback.message_id-delit)
        except (Exception, Error, MessageToDeleteNotFound):
            print('Нужные сообщеньки стёрлись')


# ---------------------------------------------------------------------------------------------------------
# --------------------Предложить------------------------------
def post():
    class FormPost(StatesGroup):
        klient_post = State()

    @dp.message_handler(text="📝|Предложить пост в канал")
    async def post_bt(callback: types.callback_query, state: FSMContext):
        await callback.answer('Кнопка не работает')
        await asyncio.sleep(3)
        await main_menu(callback)
        await FormPost.klient_post.set()
        await callback.answer(f'{callback.from_user.username}, введите сообщение, которое хотите предложить.')
        await callback.delete()
    #
    # @dp.message_handler(state=FormPost.klient_post, content_types=types.ContentTypes.TEXT)
    # async def post_kl(call: types.callback_query, state: FSMContext):
    #     async with state.proxy() as data:
    #         data['klient_post'] = call.text
    #         await bot.send_message(CHANNEL_ID, md.text(md.text(f'<b>📩 новый ПОСТ</b> '),
    #                                                    md.text(''),
    #                                                    md.text(f'TG user id: {call.from_user.id}'),
    #                                                    md.text(f'TG first name: {call.from_user.first_name}'),
    #                                                    md.text(f'TG user name: {call.from_user.username}'),
    #                                                    md.text(''),
    #                                                    md.text(f'⭐дата: {datetime.date.today()}'),
    #                                                    md.text(f'⭐время: {datetime.datetime.now().time()}'),
    #                                                    md.text(f'_____'),
    #                                                    md.text(f"<b>📝️ текст поста:</b>"),
    #                                                    md.text('👇🏻', data['klient_post']),
    #                                                    md.text(f''),
    #                                                    md.text(f'💾️ файл / фото / видео'),
    #                                                    md.text(f'_____'),
    #                                                    md.text(f''),
    #                                                    md.text(f'• постов в очереди: '),
    #                                                    md.text(f''),
    #                                                    md.text(f'<b>🤖️ меню начала действий:</b>'),
    #                                                    md.code(f'├ публикация поста'),
    #                                                    md.code(f'├ отмена публикации'),
    #                                                    md.code(f'└ настроить очередь'),
    #                                                    md.text(f''),
    #                                                    md.text(f'🤖️ информер подписчику: '),
    #                                                    md.text(f'мда... Ну и дичь'),
    #                                                    sep='\n'))
    #
    #     await state.finish()
    #     await bot.send_message(call.from_user.id, "Вы успешно предложили новость.\n\nСпасибо!🤝")
    #     time.sleep(2)
    #     await call.delete()
    #     await main_menu(call)


# ----------Form "Собрать"-----------------
def form_colect():
    class Form(StatesGroup):
        Company = State()
        Phone = State()
        ClientName = State()
        E_mail = State()
        RobotType = State()
        PhoneSize = State()
        telephonia = State()
        Confirm = State()

    @dp.callback_query_handler(text="robot")
    async def robot(message: types.Message, state: FSMContext):
        button_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
        cancelButton = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)
        await Form.Company.set()
        await bot.send_message(message.from_user.id, f'''{message.from_user.first_name}, отправьте свое техническое задание для робота и узнайте, чем он может быть Вам полезен!
_____
1️⃣ Название компании 👇🏻''', reply_markup=cancelButton, parse_mode='HTML')

    @dp.message_handler(state='*', commands='cancel')
    @dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
    async def cancel(message: types.message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return

        await bot.send_message(message.from_user.id, text='''🔥 Бот N — голосовой помощник от ANNCOM
_____''', reply_markup=bt_sec)

        await state.finish()
        await asyncio.sleep(1)
        await main_menu(message)

    @dp.message_handler(state=Form.Company)
    async def client_company(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['Company'] = message.text

        await Form.next()
        await bot.send_message(message.from_user.id, '2️⃣ Номер телефона 👇🏻')


    @dp.message_handler(state=Form.Phone)
    async def client_phone(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['Phone'] = message.text

        await Form.next()
        await bot.send_message(message.from_user.id, '3️⃣ Ваше Имя 👇🏻')

    @dp.message_handler(state=Form.ClientName)
    async def client_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['ClientName'] = message.text

        await Form.next()
        await bot.send_message(message.from_user.id, '4️⃣ Ваш E-mail 👇🏻')

    @dp.message_handler(state=Form.E_mail)
    async def client_email(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['E_mail'] = message.text

        kb_form = InlineKeyboardMarkup()
        kb_form.add(types.InlineKeyboardButton(text='Валидация/Фильтрация', callback_data='1'))
        kb_form.add(types.InlineKeyboardButton(text='Предиктивный набор', callback_data='2'))
        kb_form.add(types.InlineKeyboardButton(text='HLR запросы', callback_data='3'))
        kb_form.add(types.InlineKeyboardButton(text='Передача голоса', callback_data='4'))
        kb_form.add(types.InlineKeyboardButton(text='Диалог "робот-Человек"', callback_data='5'))
        kb_form.add(types.InlineKeyboardButton(text='Робот на входящую связь', callback_data='6'))

        await Form.next()
        await bot.send_message(message.from_user.id,
                               '''5️⃣ Какой тип робота вам нужен? Отправьте боту название 
    из списка ниже:

    ✓ Валидация / Фильтрация базы номеров
    ✓ Предиктивный набор (автодозвон)
    ✓ HLR запросы
    ✓ С передачей голосового сообщения
    ✓ Распознавание + ведение диалога «робот-Человек»
    ✓ Робот на входящую связь
    _____

    ⚠️ Нажмите кнопку или напишите текстом, какие типы 
     робота Вас интересуют 👇🏻''', reply_markup=kb_form)


    @dp.callback_query_handler(text_contains='', state=Form.RobotType)
    async def client_robot_type(callback_query: types.callback_query, state: FSMContext):
        mass = ''
        match callback_query.data:
            case '1':
                mass = 'Валидация/Фильтрация'
            case '2':
                mass = 'Предиктивный набор'
            case '3':
                mass = 'HLR запросы'
            case '4':
                mass = 'Передача голоса'
            case '5':
                mass = 'Диалог "робот-Человек"'
            case '6':
                mass = 'Робот на входящую связь'
            case _:
                mass = callback_query.text

        async with state.proxy() as data:
            data['RobotType'] = mass

        await Form.next()
        await bot.send_message(callback_query.from_user.id, '''6️⃣ Укажите количество номеров, 
      которые планируете загружать в обзвон в день 👇🏻''')

    @dp.message_handler(state=Form.PhoneSize)
    async def client_phone_size(message: types.message, state: FSMContext):
        async with state.proxy() as data:
            data['PhoneSize'] = message.text

        kb_phones = InlineKeyboardMarkup()
        kb_phones.add(types.InlineKeyboardButton(text="своя телефония", callback_data="1"))
        kb_phones.add(types.InlineKeyboardButton(text='телефония + робот', callback_data='2'))
        await Form.next()
        await bot.send_message(message.from_user.id, '''7️⃣ Для исходящих звонков и рассылки голосовых 
    сообщений к роботу нужно подключить провайдера 
    связи. Вы можете подключить своего провайдера – это 
    бесплатно! либо запросить тарифы на исходящие звонки 
    у нас. 
    Выберите, что подключаем: 👇🏻''', reply_markup=kb_phones)

    @dp.callback_query_handler(text_contains='', state=Form.telephonia)
    async def client_telephonia(callback: types.callback_query, state: FSMContext):
        global connection, cursor
        mass = ''
        match callback.data:
            case '1':
                mass = 'своя телефония'
            case '2':
                mass = 'телефония + робот'
            case _:
                mass = callback.text
        async with state.proxy() as data:
            data['telephonia'] = mass
            markup = types.ReplyKeyboardRemove()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Согласен", "Нет"]
        keyboard.add(*buttons)
        await Form.next()
        await bot.send_message(callback.from_user.id, f'''
Бот собирает информацию для обратной связи и попросит оставить свои данные.
Если Вы {link}, то нажмите кнопку "Согласен". 
В противном случае, нажмите "Нет."''', reply_markup=keyboard, disable_web_page_preview=True)




    @dp.message_handler(state=Form.Confirm)
    async def confirm(callback: types.callback_query, state: FSMContext):
        global connection, cursor
        mass = ''
        match callback.text:
            case '1':
                mass = "Согласен"
            case '2':
                mass = "Нет"
            case _:
                mass = callback.text
        async with state.proxy() as data:
            data['Confrim'] = mass

        if (mass == "Согласен"):
            await bot.send_message(CHANNEL_ID, md.text(md.text('<strong>🤖СБОРКА</strong>\n'),
                                                       md.text(f"<b>TG user id: {callback.from_user.id}</b>"),
                                                       md.text(
                                                           f"<b>TG first name: {callback.from_user.first_name}</b>"),
                                                       md.text(f"<b>TG last name: {callback.from_user.last_name}</b>"),
                                                       md.text(f"<b>TG username: {callback.from_user.username}</b>"),
                                                       md.text(f'🗓<b>дата:{datetime.date.today()} </b>'),
                                                       md.text(
                                                           f'⏰<b>время:{datetime.datetime.now().strftime("%H:%M:%S")} </b>'),
                                                       md.text('--------------'),
                                                       md.text(f"🔥 <strong>{data['Company']}</strong>"),
                                                       md.text(f"🔥 <strong>{data['Phone']}</strong>"),
                                                       md.text(f"🔥 <strong>{data['ClientName']}</strong>"),
                                                       md.text(f"🔥 <strong>{data['E_mail']}</strong>"),
                                                       md.text(f"🔥 <strong>{data['RobotType']}</strong>"),
                                                       md.text(f"🔥 <strong>{data['PhoneSize']}</strong>"),
                                                       md.text(f"🔥 <strong>{data['telephonia']}</strong>"),
                                                       sep='\n'), parse_mode=ParseMode.HTML)
            await state.finish()
            await bot.send_message(CHANNEL_ID, f"@{callback.from_user.username}, {callback.from_user.id}")
            await bot.send_message(callback.from_user.id, '<b>Спасибо! \n С вами свяжутся</b>🤝', reply_markup=bt_sec,
                                   parse_mode=ParseMode.HTML)
            await asyncio.sleep(2)
            await main_menu(callback)
            try:
                for delit in range(1,20):
                    await bot.delete_message(callback.chat.id, callback.message_id-delit)
            except (Exception, Error, MessageToDeleteNotFound):
                print('Нужные сообщеньки стёрлись')

            # try:
            # Дата
            #     now = datetime.datetime.now()
            #     timeN = now.strftime("%d/%m/%Y")

            #     connection = psycopg2.connect(  database='BOT',
                                    #   user='postgres',
                                    #   password='CHISTOHIN025134',
                                    #   host='localhost',
                                    #   port='5432')
            #     print('База подключена')
            #     connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            #     cursor = connection.cursor()
            #     cursor.execute(f'''INSERT INTO FORM_BOT (company, phone, name, e_mail, time, username) 
            #     VALUES ('{data['Company']}', {data['Phone']}, '{data['ClientName']}', '{data['E_mail']}','{timeN}','{callback.from_user.username}')''')
            # except (Exception, Error) as error:
            #     print('Ошибка при работе с PostgreSQL в форме', error)
            # finally:
            #     if connection:
            #         cursor.close()
            #         connection.close()
        else:
            await bot.send_message(callback.from_user.id, f'''К сожалению, дальнейшее взаимодействие с Ботом невозможно 
по причине вашего отказа от передачи своих данных.''', reply_markup=bt_sec)
            await state.finish()
            await asyncio.sleep(1)
            await main_menu(callback)
            try:
                for delit in range(1,20):
                    await bot.delete_message(callback.chat.id, callback.message_id-delit)
            except (Exception, Error, MessageToDeleteNotFound):
                print('Нужные сообщеньки стёрлись')


# ----------End Form "Собрать"-----------------


# ----------Form "новое сообщение"-----------------
def form_new_mess():
    class Forma(StatesGroup):
        Mes = State()

    @dp.callback_query_handler(text="mess_to_add")
    async def robot_voic(message: types.message, state: FSMContext):
        button_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
        cancelButton = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)
        await Forma.Mes.set()
        await bot.send_message(message.from_user.id, f'''<b>Уважаемый {message.from_user.first_name}, отправьте сообщение и с Вами свяжутся!</b>👇🏻
    ''', parse_mode=ParseMode.HTML, reply_markup=cancelButton)

    @dp.message_handler(state='*', commands='cancel')
    @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
    async def cancel(message: types.message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return

        await state.finish()
        await message.reply()

    @dp.message_handler(state=Forma.Mes)
    async def client_mess(message: types.message, state: FSMContext):
        async with state.proxy() as data:
            data['ClientMess'] = message.text
            await bot.send_message(CHANNEL_ID, md.text(md.text('<strong>💬 НОВОЕ СООБЩЕНИЕ</strong>'),
                                                       md.text(f"<b>TG user id: {message.from_user.id}</b>"),
                                                       md.text(
                                                           f"<b>TG first name: {message.from_user.first_name}</b>"),
                                                       md.text(
                                                           f"<b>TG last name: {message.from_user.last_name}</b>"),
                                                       md.text(f"<b>TG username: {message.from_user.username}</b>"),
                                                       md.text(f'🗓<b>дата:{datetime.date.today()} </b>'),
                                                       md.text(
                                                           f'⏰<b>время:{datetime.datetime.now().strftime("%H:%M:%S")} </b>'),
                                                       md.text('--------------'),
                                                       md.text(
                                                           f"Сообщение от клиента:\n <strong>{data['ClientMess']}</strong>"),
                                                       sep='\n'), parse_mode=ParseMode.HTML)
            await bot.send_message(CHANNEL_ID, f"@{message.from_user.username}, {message.from_user.id}")

            await state.finish()
            await bot.send_message(message.from_user.id, '<b>Спасибо! \n С вами свяжутся</b>🤝',
                                   parse_mode=ParseMode.HTML, reply_markup=bt_sec)
            await asyncio.sleep(3)
            await main_menu(message)

# ----------End Form------------
# 3