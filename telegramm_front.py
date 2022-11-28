from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

import text_messages
from core import Core
from settings import TOKEN

TOKEN = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
core = Core()

"""Логирование"""
logging.basicConfig(level=logging.INFO,
                    filename='core_log.log',
                    filemode='a',
                    format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_form = logging.Formatter('%(asctime)s: %(message)')
log_handler = logging.StreamHandler()
logger.addHandler(log_handler)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    log_in = InlineKeyboardButton('Вход', callback_data='login')
    all_misses = InlineKeyboardButton('Все пропуски', callback_data='all_misses')
    show_miss_id = InlineKeyboardButton('Показать ID', callback_data='show_id')
    commands_mean = InlineKeyboardButton('Команды бота', callback_data='show_comm_mean')
    get_tg_id = InlineKeyboardButton('Мой ID', callback_data='get_ID')
    last_update_btn = InlineKeyboardButton('Посл.обновления', callback_data='last_update')
    keyboard.add(log_in, all_misses, show_miss_id, commands_mean, get_tg_id, last_update_btn)

    group_name = core.check_login(message.chat.id)[0][0]
    if group_name:
        """Команда старт для авторизованных со списком-напоминалкой команд"""
        await bot.send_message(message.chat.id, text_messages.start_auth, reply_markup=keyboard)
    else:
        """ Команда старт для неавторизованных """
        await bot.send_message(message.chat.id, text_messages.start, reply_markup=keyboard)


@dp.callback_query_handler(lambda a: a.data == 'login')
async def login(call: types.callback_query):
    """ Кнопка Вход """
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


@dp.callback_query_handler(lambda a: a.data == 'all_misses')
async def all_group_misses(call: types.callback_query):
    """ Кнопка всех пропусков """
    group_name = core.check_login(call.message.chat.id)[0][0]
    miss = core.show_misses(group_name)
    new = ''.join([f'{i[0]}.{i[1]} - {i[2]}\n' for i in miss])
    await bot.send_message(call.message.chat.id, f'{new}')


@dp.callback_query_handler(lambda a: a.data == 'show_id')
async def show_id(call: types.callback_query):
    """ Кнопка Показать ID """
    group_name = core.check_login(call.message.chat.id)
    miss = core.show_misses(group_name[0][0])
    send = ''.join([f'{i[0]} - {i[1]}\n' for i in miss])
    await bot.send_message(call.message.chat.id, send)


@dp.message_handler(commands=['clear_miss'])
async def clear(message: types.Message):
    """ Команда обнуления всех пропусков """
    group_name = core.check_login(message.chat.id)
    core.clear_miss(group_name[0][0])
    logger.warning(f'Bot - Обнуление группы|| {group_name[0][0]}')


@dp.callback_query_handler(lambda a: a.data == 'show_comm_mean')
async def show_comm_mean(call: types.callback_query):
    """ Кнопка показа команд бота """
    await bot.send_message(call.message.chat.id, text_messages.comm_mean)


@dp.callback_query_handler(lambda a: a.data == 'get_ID')
async def get_id(call: types.callback_query):
    """Кнопка вывода ID в Telegram"""
    await bot.send_message(call.message.chat.id, f'{call.message.chat.id}')


@dp.message_handler(commands=['new'])
async def add_group(message: types.Message):
    """ Команда добавления новых людей в группу """
    get_text = [tuple(i.split('-')) for i in message.text.split('\n')]
    group = core.check_login(message.chat.id)[0][0]
    core.add_miss(table_name=group, insert=get_text[1:])
    logger.info(f'Bot - Добавление студента|| {group} {get_text[1:]}')


@dp.message_handler(commands=['delete_one'])
async def clear_one(message: types.Message):
    """Удаление одного студента из БД"""
    group_name = core.check_login(message.chat.id)
    stud_id = message.text.split('/delete_one')[1].strip()
    core.delete_one_stud(table_name=group_name[0][0], userid=stud_id)
    logger.info(f'Bot - Удаление студента|| {group_name[0][0]} ID:{stud_id}')
    await bot.send_message(message.chat.id, f'Студент с ID: {stud_id} удалён')


@dp.message_handler(commands=['delete_one'])
async def clear_one_stud(message: types.Message):
    """Обнуление пропусков студента"""
    group_name = core.check_login(message.chat.id)
    stud_id = message.text
    core.clear_one_miss(table_name=group_name[0][0], stud_id=stud_id)
    logger.info(f'Bot - Обнуление пропусков студента|| {group_name[0][0]} ID:{stud_id}')
    await bot.send_message(message.chat.id, f'Пропуски студента с ID: {stud_id} обнулены')


@dp.message_handler(commands=['sort_from'])
async def sort_from(message: types.Message):
    """Возвращает список пропусков, добавленных после определённой даты"""
    need_date = ''.join(message.text.split('/sort_from')[1:])
    new_date = need_date.replace(' ', '', 10)
    group_name = core.check_login(message.chat.id)
    response = core.sort_from_date(table_name=group_name[0][0], need_date=new_date)
    if len(response) != 0:
        await bot.send_message(message.chat.id, ''.join([f'{i}\n' for i in response]))
    else:
        await bot.send_message(message.chat.id, f'Упс...\nПохоже после {need_date} пропуски не добавлялись')


@dp.message_handler(commands=['sort_before'])
async def sort_before(message: types.Message):
    """Возвращает список пропусков, добавленный после определённой даты"""
    need_date = ''.join(message.text.split('/sort_before')[1:])
    new_date = need_date.replace(' ', '', 10)
    group_name = core.check_login(message.chat.id)
    response = core.sort_before_date(table=group_name[0][0], need_date=new_date)
    if len(response) != 0:
        await bot.send_message(message.chat.id, ''.join([f'{i}\n' for i in response]))
    else:
        await bot.send_message(message.chat.id, f'Упс...\nПохоже до {need_date} пропуски не добавлялись')


@dp.message_handler(commands=['sort_btw'])
async def sort_btw(message: types.Message):
    """Возвращает список пропусков, добавленных в определённый период -> дата начала, дата конца"""
    text = message.text.split('/sort_btw')
    new_text = text[1].strip().split(' ')
    start_date, end_date = new_text[0], new_text[-1]
    group_name = core.check_login(message.chat.id)
    response = core.sort_btw(table=group_name[0][0], start_date=start_date, end_date=end_date)
    if len(response) != 0:
        await bot.send_message(message.chat.id, ''.join([f'{i}\n' for i in response]))
    else:
        await bot.send_message(message.chat.id,
                               f'Упс...\nПохоже в период между {start_date} и {end_date} пропуски не добавляли')


@dp.callback_query_handler(lambda a: a.data == 'last_update')
async def last_update(call: types.callback_query):
    """Возвращает даты последних добавленных пропусков"""
    group = core.check_login(call.message.chat.id)[0][0]
    response = core.last_update(group)
    logger.info(f'Bot - Просмотр последних обновлений')
    await bot.send_message(call.message.chat.id, ''.join([f'{i[0]}.{i[1]} - {i[2]} <- {i[3]}\n' for i in response]))


@dp.message_handler(commands=['clear_all_database'])
async def clear_all_db(message: types.Message):
    """Очищает базу данных полностью"""
    tables = core.clear_all_db()
    await bot.send_message(message.chat.id, f'Вся база данных успешно очищена')
    await bot.send_message(message.chat.id, ''.join([f'{i}\n' for i in tables]))


@dp.message_handler(commands=['delete_one_table'])
async def delete_one_table(message: types.Message):
    """Удаляет одну таблицу, после команды просто написать имя таблицы"""
    get_text = message.text.split('/delete_one_table')[1].replace(' ', '')
    core.delete_one_table(get_text)
    await bot.send_message(message.chat.id, f'Удалена одна таблица:{get_text}')


@dp.message_handler(commands=['show_tables'])
async def show_all_tables(message: types.Message):
    """Показывает все существующие таблицы, кроме chat_id"""
    tables = core.get_all_tbl_names()
    response = ''.join([f"{i[0]}\n" for i in tables])
    await bot.send_message(message.chat.id, f'Список всех таблиц\n{response}')


@dp.message_handler(commands=['clear_log_file'])
async def del_log_file(message: types.Message):
    """Очистка файла логов"""
    core.clear_log_file()
    await bot.send_message(message.chat.id, 'Файл логов удалён')


@dp.message_handler()
async def add_miss(message: types.Message):
    """ Прием сообщений с пропусками """
    get_text = [tuple(i.split('-')) for i in message.text.split('\n')]
    group = core.check_login(message.chat.id)[0][0]
    for i in get_text:
        core.update_miss(table_name=group, userid=i[0], adding_miss=i[2])
        logger.info(f'Bot - Добавление пропуска|| группа {group} ID:{i[0]} часов:{i[2]} ')


executor.start_polling(dp)
