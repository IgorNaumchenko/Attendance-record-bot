from core import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


TOKEN = ''
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    login = InlineKeyboardButton('Вход', callback_data='login')
    all_misses = InlineKeyboardButton('Все пропуски', callback_data='all_misses')
    add_new_miss = InlineKeyboardButton('Добавить пропуски', callback_data='add_new_miss')
    keyboard.add(login, all_misses, add_new_miss)

    await bot.send_message(message.chat.id, 'Приветик\nВыбери функцию\nЕсли Ты не зарегистрирован, зарегайся',
                           reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'login')
async def login(call: types.callback_query):
    userid = call.message.chat.id
    try:
        group_name = Db_Driver_Sqlite3().check_login(userid)
        await bot.send_message(call.message.chat.id, f'Вы уже зарегистрированы\nУникальный номер вашей группы "{group_name[0][0]}"')
    except:
        await bot.send_message(call.message.chat.id, 'Усп\nЧто-то пошло не так')
    # await bot.send_message(call.message.chat.id, f'{userid}')


executor.start_polling(dp)
