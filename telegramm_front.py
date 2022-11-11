from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import text_messages
from core import Core
from settings import TOKEN

TOKEN = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
core = Core()


# """ Команда старт """
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    log_in = InlineKeyboardButton('Вход', callback_data='login')
    all_misses = InlineKeyboardButton('Все пропуски', callback_data='all_misses')
    show_miss_id = InlineKeyboardButton('Показать ID', callback_data='show_id')
    commands_mean = InlineKeyboardButton('Команды бота', callback_data='show_comm_mean')
    get_tg_id = InlineKeyboardButton('Мой ID', callback_data='get_ID')
    keyboard.add(log_in, all_misses, show_miss_id, commands_mean, get_tg_id)
    await bot.send_message(message.chat.id, text_messages.start, reply_markup=keyboard)


# """ Кнопка Вход """
@dp.callback_query_handler(lambda a: a.data == 'login')
async def login(call: types.callback_query):
    userid = call.message.chat.id
    try:
        group_name = core.check_login(userid)
        await bot.send_message(call.message.chat.id,
                               f'Вы уже зарегистрированы\nУникальный номер вашей группы "{group_name[0][0]}"')
    except:
        core.create_new_table(userid=userid)
        group_name = core.check_login(userid)
        await bot.send_message(call.message.chat.id,
                               f'Бот вас зарегистрировал. Уникальное имя вашей группы: {group_name[0][0]}')


# """ Кнопка всех пропусков """
@dp.callback_query_handler(lambda a: a.data == 'all_misses')
async def all_group_misses(call: types.callback_query):
    group_name = core.check_login(call.message.chat.id)[0][0]
    miss = core.show_misses(group_name)
    new = ''.join([f'{i[0]}.{i[1]} - {i[2]}\n' for i in miss])
    await bot.send_message(call.message.chat.id, f'{new}')


# """ Кнопка Показать ID """
@dp.callback_query_handler(lambda a: a.data == 'show_id')
async def show_id(call: types.callback_query):
    group_name = core.check_login(call.message.chat.id)
    miss = core.show_misses(group_name[0][0])
    send = ''.join([f'{i[0]} - {i[1]}\n' for i in miss])
    await bot.send_message(call.message.chat.id, send)


# """ Команда обнуления всех пропусков """
@dp.message_handler(commands=['clear_miss'])
async def clear(message: types.Message):
    group_name = core.check_login(message.chat.id)
    core.clear_miss(group_name[0][0])


# """ Кнопка показа команд бота """
@dp.callback_query_handler(lambda a: a.data == 'show_comm_mean')
async def show_comm_mean(call: types.callback_query):
    await bot.send_message(call.message.chat.id, text_messages.comm_mean)


# """Кнопка вывода ID в Telegram"""
@dp.callback_query_handler(lambda a: a.data == 'get_ID')
async def get_id(call: types.callback_query):
    await bot.send_message(call.message.chat.id, f'{call.message.chat.id}')


# """ Команда добавления новых людей в группу """
@dp.message_handler(commands=['new'])
async def add_group(message: types.Message):
    get_text = [tuple(i.split('-')) for i in message.text.split('\n')]
    group = core.check_login(message.chat.id)[0][0]
    core.add_miss(table_name=group, insert=get_text[1:])


# """ Прием сообщений с пропусками """
@dp.message_handler()
async def add_miss(message: types.Message):
    get_text = [tuple(i.split('-')) for i in message.text.split('\n')]
    group = core.check_login(message.chat.id)[0][0]
    for i in get_text:
        core.update_miss(table_name=group, userid=i[0], adding_miss=i[2])


executor.start_polling(dp)
