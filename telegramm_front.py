from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import pshares
from core import *
from settings import TOKEN

TOKEN = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    login = InlineKeyboardButton('Вход', callback_data='login')
    all_misses = InlineKeyboardButton('Все пропуски', callback_data='all_misses')
    show_miss_id = InlineKeyboardButton('Показать ID', callback_data='show_id')
    commands_mean = InlineKeyboardButton('Команды бота', callback_data='show_comm_mean')
    get_id = InlineKeyboardButton('Мой ID', callback_data='get_ID')
    keyboard.add(login, all_misses, show_miss_id, commands_mean, get_id)
    await bot.send_message(message.chat.id, pshares.start, reply_markup=keyboard)


@dp.callback_query_handler(lambda a: a.data == 'login')
async def login(call: types.callback_query):
    userid = call.message.chat.id
    try:
        group_name = Db_Driver_Sqlite3().check_login(userid)
        await bot.send_message(call.message.chat.id,
                               f'Вы уже зарегистрированы\nУникальный номер вашей группы "{group_name[0][0]}"')
    except:
        Db_Driver_Sqlite3().create_new_table(userid=userid)
        group_name = Db_Driver_Sqlite3().check_login(userid)
        await bot.send_message(call.message.chat.id,
                               f'Бот вас зарегистрировал. Уникальное имя вашей группы: {group_name[0][0]}')


@dp.callback_query_handler(lambda a: a.data == 'all_misses')
async def all_group_misses(call: types.callback_query):
    group_name = Db_Driver_Sqlite3().check_login(call.message.chat.id)[0][0]
    miss = Db_Driver_Sqlite3().show_misses(group_name)
    new = ''.join([f'{i[0]}.{i[1]} - {i[2]}\n' for i in miss])
    await bot.send_message(call.message.chat.id, f'{new}')


@dp.callback_query_handler(lambda a: a.data == 'show_id')
async def show_id(call: types.callback_query):
    group_name = Db_Driver_Sqlite3().check_login(call.message.chat.id)
    miss = Db_Driver_Sqlite3().show_misses(group_name[0][0])
    send = ''.join([f'{i[0]} - {i[1]}\n' for i in miss])
    await bot.send_message(call.message.chat.id, send)


@dp.message_handler(commands=['clear_miss'])
async def clear(message: types.Message):
    group_name = Db_Driver_Sqlite3().check_login(message.chat.id)
    Db_Driver_Sqlite3().clear_miss(group_name[0][0])


@dp.callback_query_handler(lambda a: a.data == 'show_comm_mean')
async def show_comm_mean(call: types.callback_query):
    await bot.send_message(call.message.chat.id, pshares.comm_mean)


@dp.callback_query_handler(lambda a: a.data == 'get_ID')
async def get_id(call: types.callback_query):
    await bot.send_message(call.message.chat.id, f'{call.message.chat.id}')


@dp.message_handler(commands=['new'])
async def add_group(message: types.Message):
    get_text = [tuple(i.split('-')) for i in message.text.split('\n')]
    group = Db_Driver_Sqlite3().check_login(message.chat.id)[0][0]
    Db_Driver_Sqlite3().add_miss(table_name=group, insert=get_text[1:])


@dp.message_handler()
async def add_miss(message: types.Message):
    get_text = [tuple(i.split('-')) for i in message.text.split('\n')]
    group = Db_Driver_Sqlite3().check_login(message.chat.id)[0][0]
    for i in get_text:
        Db_Driver_Sqlite3().update_miss(table_name=group, userid=i[0], adding_miss=i[2])


executor.start_polling(dp)
