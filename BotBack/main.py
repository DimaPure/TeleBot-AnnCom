import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger
from config import TOKEN

loop = asyncio.new_event_loop()
bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop, storage=MemoryStorage())


async def on_startup(_):
    logger.info("start pooling | {} - @{}",
                (me := await bot.get_me()).first_name, me.username)
    user_should_be_notified = 166122310
    await bot.send_message(user_should_be_notified, "Бот начал работу")


# async def on_shutdown(_):
#     user_should_be_notified = -1001842737455
#     await bot.send_message(user_should_be_notified, 'Бот выключен')


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)


