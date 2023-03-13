import asyncio
import time
import datetime

import psycopg2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InputFile, WebAppInfo
from aiogram.utils import executor
from aiogram.utils.exceptions import CantInitiateConversation, MessageCantBeDeleted, MessageToDeleteNotFound
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import keyboards
from form import form_colect, form_new_mess, konsult, post
from keyboards import bt_sec
from main import bot, dp
from text_bt import comp, link, cont

hotOffer = 'https://tgtest.sahome.ru/hotOffer'
index = "https://tgtest.sahome.ru/"
botN = 'https://tgtest.sahome.ru/botN'
contacts = 'https://tgtest.sahome.ru/contacts'

# -------------------Приветствие-------------------------
@dp.message_handler(commands=['start'])
async def process_hi1_command(message: types.Message):
    # global connection, cursor
    await message.answer(f'''🤖 Автодайлер «Бот N.»
 Голосовой робот-помощник для бизнеса

 🔥передает голосовые сообщения, распознает ответы 
   Человека, анализирует и умеет вести диалог
   
 🔥умный секретарь для входящих звонков

 ✓ оповещение об акциях
 ✓ приглашение на вебинар/мероприятие
 ✓ проведение опросов, анкетирование
 ✓ фильтрация базы номеров
 ✓ повышение лояльности клиентов
 ✓ лидогенерация и многое другое…
 _____
    {message.from_user.first_name}, выберите пункт меню 👇🏻''', reply_markup=bt_sec)

    try:
        now = datetime.datetime.now()
        timeN = now.strftime("%d/%m/%Y")
        connection = psycopg2.connect(database='for_bots',
                                        user='wisdom',
                                        password='vZSi#6j?X$',
                                        host='localhost',
                                        port='5432')
        print('База подключена')
        cursor = connection.cursor()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # print(cursor.execute(f'select from users where user_id = {message.from_user.id}'))
        # if cursor.execute(f'select from users where user_id = {message.from_user.id}') == None:
        cursor.execute(f'''insert into USERS (user_id, name, username, time)
                            values ('{message.from_user.id}', '{message.from_user.first_name}', '{message.from_user.username}','{timeN}')
                              on conflict (user_id) do nothing''')
    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)

    finally:
        if connection:
            cursor.close()
            connection.close()


#  ----------------- 📝|Канал -----------------------------------------------
@dp.message_handler(text=['📝|Канал'])
async def canal(message: types.Message):
    kb_canal = types.InlineKeyboardMarkup()
    kb_canal.insert(types.InlineKeyboardButton(text="|КАНАЛ", url='https://t.me/botN_ai'))
    kb_canal.add(types.InlineKeyboardButton(text="|Главное меню", callback_data="Menu"))
    await bot.send_photo(message.from_user.id, InputFile('pic/Mini_icon.jpg'), reply_markup=kb_canal,
                         caption=f'''{message.from_user.first_name}, здесь вы можете перейти в канал и чат нашего проекта 👇''', )
    await bot.delete_message(message.chat.id, message.message_id)

#  -------------------------------------------------

# Help------------------------------------------------
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Выберите пункт меню!")
    await bot.delete_message(message.chat.id, message.message_id)


# Menu------------------------------------------------
@dp.message_handler(text=['-|Меню'])
async def main_menu(message: types.Message):
    kb1 = types.InlineKeyboardMarkup()
    kb1.insert(types.InlineKeyboardButton(text="Бесплатная консультация", callback_data="Konsult"))
    kb1.add(types.InlineKeyboardButton(text="О компании", callback_data="Company"))
    # kb1.insert(types.InlineKeyboardButton(text="Собрать 🤖", callback_data="robot"))
    kb1.add(types.InlineKeyboardButton(text="🤖 в коробке", web_app=WebAppInfo(url=index)))
    kb1.insert(types.InlineKeyboardButton(text="🔥Предожение", web_app=WebAppInfo(url=hotOffer)))
    kb1.add(types.InlineKeyboardButton(text="Про Бот N.", web_app=WebAppInfo(url=botN)))
    kb1.insert(types.InlineKeyboardButton(text="Контакты",callback_data="contacts"))
    kb1.add(types.InlineKeyboardButton(text="Поделится", switch_inline_query='https://t.me/practicIST_bot'))
    await bot.send_photo(message.from_user.id, InputFile("pic/icon.jpg"), reply_markup=kb1, caption=f''' {message.from_user.first_name}, выберите пункт меню 👇🏻''', )
    await bot.delete_message(message.chat.id, message.message_id)


# ----------- Form Консультация ------------
konsult()
# ------------------------------------------
post()

# ---------- Form "Собрать"-----------------
form_colect()
# -------------------------------------------

# ----------Form "Новое сообщение"----------
form_new_mess()


# ------------------------------------------


# Наполнение внутренних кнопок главного меню----------------------------------------------------------------------------------------------
@dp.callback_query_handler(text_contains='', state='*')
async def qr_message(call: types.callback_query, state: FSMContext):
    await state.get_state()
    await state.finish()
    code = call.data
    match code:
        # О компании ----------------------------------------------------------------------------------------------------------------------------
        case "Company":
            kb_Company = InlineKeyboardMarkup()
            kb_Company.row(types.InlineKeyboardButton(text='✅|бесплатная консультация', callback_data='Konsult'))
            kb_Company.row(types.InlineKeyboardButton(text='🤖 в КОРОБКЕ', web_app=WebAppInfo(url=index)))
            # kb_Company.row(types.InlineKeyboardButton(text='Контакты', web_app=WebAppInfo(url=contacts)))
            kb_Company.row(types.InlineKeyboardButton(text='Главное меню', callback_data='Menu'))
            await bot.send_photo(call.from_user.id, InputFile('pic/Mini_icon.jpg'), reply_markup=kb_Company,
                                 caption=comp)
        #Контакты ------------------------------------------------------------------------------------------------------
        case "contacts":
            kb_contacts = InlineKeyboardMarkup()
            kb_contacts.insert(types.InlineKeyboardButton(text='📨|Написать соощение', callback_data='mess_to_add'))
            kb_contacts.row(types.InlineKeyboardButton(text='Главное меню', callback_data='Menu'))
            await bot.send_message(call.from_user.id, cont, disable_web_page_preview=True, reply_markup=kb_contacts)
        # Про бот N ----------------------------------------------------------------------------------------------------------------------
        # case "bot_info":
        #     kb_bot_info = InlineKeyboardMarkup()
        #     kb_bot_info.row(types.InlineKeyboardButton(text='❓ Какие задачи можно решить', callback_data='may_ex'))
        #     kb_bot_info.row(types.InlineKeyboardButton(text='| Главное меню', callback_data='Menu'))
        #     await bot.send_photo(call.from_user.id, InputFile('pic/Mini_icon.jpg'), reply_markup=kb_bot_info,
        #                          caption=bot_inf)
        # ❓ Какие задачи можно решить ---------------------------------------------------------------------------------------------------
        # case "may_ex":
        #     kb_may_ex = InlineKeyboardMarkup()
        #     kb_may_ex.row(types.InlineKeyboardButton(text='⬅| Вернуться назад', callback_data='bot_info'))
        #     kb_may_ex.row(types.InlineKeyboardButton(text='| Главное меню', callback_data='Menu'))
        #     await bot.send_photo(call.from_user.id, InputFile('pic/Mini_icon.jpg'), reply_markup=kb_may_ex, caption=ex)


@dp.message_handler()
async def admin_reply(message: types.Message):
    # me = await bot.get_me()
    # if not message.reply_to_message:
    #     return
    # if message.reply_to_message.from_user.id != me.id:
    #     return
    # if not message.text:
    #     await bot.send_message(message.chat.id, "Я обрабатываю только текст")
    #     return
    # if message.reply_to_message.text.split('\n')[0] not in keyboards.vturmu:
    #     return
    if not message.reply_to_message.text.__contains__(", "):
        return

    # Парсим id из сообщения
    uid = message.reply_to_message.text.split(", ")[1]
    try:
        await bot.send_message(uid, "<strong>⚠Ответ от администратора: </strong>" + message.text)
    except CantInitiateConversation:
        await bot.reply("Ошибка\n")



