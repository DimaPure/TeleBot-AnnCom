from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup

# Главное меню
keyboard = InlineKeyboardMarkup()

button_menu = InlineKeyboardButton('-|Меню', callback_data='Menu')
button_inc = InlineKeyboardButton('📝|Канал', callback_data='btn_fq')
button_help = InlineKeyboardButton('🆘|Помощь', callback_data='btn_h')

bt_sec = ReplyKeyboardMarkup(resize_keyboard=True).row(
    button_menu, button_inc, button_help)

vturmu = ["📩 ПОДДЕРЖКА", "📩 Консультация", "📩 новый ПОСТ", "💬 НОВОЕ СООБЩЕНИЕ"]
