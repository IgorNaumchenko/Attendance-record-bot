from sqlite3_db_driver import *
from pathlib import Path
import datetime
import string
import logging


"""Логирование"""
logging.basicConfig(level=logging.INFO,
                    filename='core_log.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_form = logging.Formatter('%(asctime)s: %(message)')
log_handler = logging.StreamHandler()
logger.addHandler(log_handler)


class Core:
    def __init__(self, db_name='misses_database.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.Db_driver = Db_Driver()

    def create_new_table(self, userid):
        need = string.ascii_lowercase
        output = [need[int(i)+1] for i in list(str(userid))]
        table_name = ''.join(output)
        self.Db_driver.create_new_table(userid=userid, table_name=table_name)
        logger.info(f'Core - Создание таблицы: {userid}:{table_name}')

    def add_miss(self, table_name, insert):
        """Добавление нового студента, принимается в виде [('19', 'Полина', '0'), datatime]"""
        expl = datetime.datetime.today()
        date = f'{expl.year}-{expl.month}-{expl.day} {expl.hour}:{expl.minute}:{expl.second}'
        new_insert = [list(i) for i in insert]
        date_insert = [i.append(date) for i in new_insert]
        ins = tuple([tuple(i) for i in new_insert])
        self.Db_driver.add_miss(table_name=table_name, insert=ins)
        logger.info(f'Core - +++ Добавление студента: {table_name}: {ins}')

    def show_misses(self, table_name):
        """Показ всех пропусков в таблице table_name"""
        miss_list = self.Db_driver.show_all_miss(table_name=table_name)
        return miss_list

    def update_miss(self, table_name, userid, adding_miss):
        """Добавление пропуска в таблицу table_name студенту с userid в количестве add_miss"""
        expl = datetime.datetime.today()
        date = f'{expl.year}-{expl.month}-{expl.day} {expl.hour}:{expl.minute}:{expl.second}'
        self.Db_driver.update_miss(table_name=table_name,
                                   userid=userid,
                                   adding_miss=adding_miss,
                                   date=date)
        logger.info(f'Core - Обновление пропуска: {table_name}: {userid}, {adding_miss}  {date}')

    def show_id(self, table_name):
        """Показать ID студентов в группе table_name"""
        id_list = self.Db_driver.show_id(table_name=table_name)
        return id_list

    def check_login(self, chat_id):
        """Возвращает группу по ID в Telegram"""
        group = self.Db_driver.check_login(chat_id=chat_id)
        return group

    def clear_miss(self, table_name):
        """Обнуление пропусков всей группы table_name"""
        expl = datetime.datetime.today()
        date = f'{expl.year}-{expl.month}-{expl.day} {expl.hour}:{expl.minute}:{expl.second}'
        self.Db_driver.clear_miss(table_name=table_name, date=date)
        logger.warning(f'Core - Обнуление пропусков группы: {table_name}')

    def delete_one_stud(self, table_name, userid):
        """Удаление одного студента userid в таблице table_name"""
        self.Db_driver.delete_one_miss(table_name=table_name, userid=userid)
        logger.warning(f'Core - Удаление студента: {table_name} {userid}')

    def clear_one_miss(self, table_name, stud_id):
        """Обнуление пропусков одного студента stud_id в таблице table_name"""
        expl = datetime.datetime.today()
        date = f'{expl.year}-{expl.month}-{expl.day} {expl.hour}:{expl.minute}:{expl.second}'
        self.Db_driver.clear_one_miss(table_name=table_name, stud_id=stud_id, date=date)
        logger.warning(f'Core - Обнуление пропуска студента: {table_name}  {stud_id}  {date}')

    def sort_from_date(self, table_name, need_date: str):
        """Возвращает пропуски, добавленные в таблицу table_name после need_date """
        date = datetime.datetime.strptime(need_date.replace('.', '-', 2), '%d-%m-%Y')
        group = self.Db_driver.show_all_miss(table_name=table_name)
        return_list = []
        for stud in group:
            ask_date = stud[3]
            form_date = datetime.datetime.strptime(ask_date, '%Y-%m-%d %H:%M:%S')
            if (form_date.year >= date.year) and (form_date.month >= date.month) and (form_date.day >= date.day):
                return_list.append(f'{stud[0]}-{stud[1]}: {stud[2]} часа(-ов)')
        return return_list

    def sort_before_date(self, table, need_date: str):
        """Возвращает пропуски, добавленные в таблицу table_name перед need_date """
        date = datetime.datetime.strptime(need_date.replace('.', '-', 2), '%d-%m-%Y')
        group = self.Db_driver.show_all_miss(table_name=table)
        return_list = []
        for stud in group:
            ask_date = stud[3]
            print(ask_date)
            form_date = datetime.datetime.strptime(ask_date, '%Y-%m-%d %H:%M:%S')
            if (form_date.year <= date.year) and (form_date.month <= date.month) and (form_date.day <= date.day):
                return_list.append(f'{stud[0]}-{stud[1]}: {stud[2]} часа(-ов)')
        return return_list

    def sort_btw(self, table, start_date: str, end_date: str):
        """Возвращает пропуски, добавленные в таблицу table_name после start_date и до end_date """
        start_date = datetime.datetime.strptime(start_date.replace('.', '-', 2), '%d-%m-%Y')
        end_date = datetime.datetime.strptime(end_date.replace('.', '-', 2), '%d-%m-%Y')
        group = self.Db_driver.show_all_miss(table_name=table)
        return_list = []
        for stud in group:
            ask_date = stud[3]
            form_date = datetime.datetime.strptime(ask_date, '%Y-%m-%d %H:%M:%S')
            if (form_date.year >= start_date.year and form_date.month >= start_date.month and
                form_date.day >= start_date.day) and (form_date.year <= end_date.year
                                                      and form_date.month <= end_date.month
                                                      and form_date.day <= end_date.day):
                return_list.append(f'{stud[0]}-{stud[1]}: {stud[2]} часа(-ов)')
        return return_list

    def last_update(self, table):
        """Показывает последние обновления пропусков студентов в группе table"""
        logger.info(f'Core - Просмотр последних обновлений')
        return self.Db_driver.show_all_miss(table_name=table)

    def clear_all_db(self):
        """Очищает всех таблиц в БД"""
        tables = self.Db_driver.clear_all_db()
        logger.warning('Core - Очищение всей БД')
        return tables

    def delete_one_table(self, table):
        """Удаление таблицы table"""
        self.Db_driver.delete_one_table(table=table)
        logger.warning('Core - Удаление таблицы')

    def get_all_tbl_names(self):
        """Возвращает список таблиц в БД, кроме chat_id"""
        table_names = self.Db_driver.get_all_tbl_names()
        return table_names

    def clear_log_file(self):
        """Очищает файл логов"""
        path = Path().cwd().glob('**/*.log')
        for i in path:
            with open(i, mode='w'):
                pass
