import logging
import sqlite3


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


class Db_Driver:
    """Класс работы с базой данных"""

    def __init__(self, db_name='misses_database.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)

    """Добавление пользователя в таблицу юзеров и создание отдельной таблицы под группу пользователя"""
    def create_new_table(self, userid, table_name):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {table_name}(userid AUTO_INCREMENT, name TEXT, miss INT, date TEXT);')
            self.connection.commit()
            cursor.execute('INSERT INTO chat_id VALUES (?, ?);', (userid, table_name))
            self.connection.commit()

    """Добавление пропуска в таблицу пользователя, входной tuple"""
    def add_miss(self, table_name, insert):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                if len(insert) == 1:
                    cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?, ?);', insert[0])
                    self.connection.commit()
                elif len(insert) > 1:
                    cursor.executemany(f'INSERT INTO {table_name} VALUES (?, ?, ?, ?);', insert)
                    self.connection.commit()
        except IndexError as error:
            logger.error(error, f'Driver - Ошибка добавления: {error}')

    """Возвращает список всех пропусков из определённой таблицы"""
    def show_all_miss(self, table_name):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name};')
        self.connection.commit()
        misses = cursor.fetchall()
        return misses

    """Добавляет пропуск с существущему уже в таблице"""
    def update_miss(self, table_name, userid, adding_miss, date):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE {} SET miss=miss+{}, date="{}" WHERE userid={}'.format(table_name,
                                                                                          adding_miss,
                                                                                          date,
                                                                                          userid))
            self.connection.commit()

    """Возвращает список 'Уникальный номер - имя' из таблицы группы"""
    def show_id(self, table_name):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT name, userid FROM {table_name}')
        self.connection.commit()
        ids = cursor.fetchall()
        return ids

    """Возвращает название группы, ищя в таблице пользователей соответствующий ID"""
    def check_login(self, chat_id):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT group_name FROM chat_id WHERE user_id={chat_id}')
        self.connection.commit()
        group = cursor.fetchall()
        return group

    """Обнуляет все пропуски в группе"""
    def clear_miss(self, table_name, date):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE {} SET miss=0, date="{}"'.format(table_name, date))
        self.connection.commit()
        logger.info(f'Driver - Обнуление группы: {table_name}')

    """Удаляет запись одного студента(уник.номер, имя, кол-во пропусков) в таблице группы"""
    def delete_one_miss(self, table_name, userid):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM {table_name} WHERE userid={userid}')
        self.connection.commit()
        logger.info(f'Driver - Удаление записи о студенте: {table_name} ID:{userid}')

    """Обнуление пропусков одного студента"""
    def clear_one_miss(self, table_name, stud_id, date):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE {} SET miss=0, date="{}" WHERE userid={}'.format(table_name, date, stud_id))
        self.connection.commit()
        logger.info(f'Driver - Обнуление пропусков студента: {table_name} {stud_id}')

    """Очистка всей БД"""
    def clear_all_db(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM sqlite_master where type="table"')
            table = cursor.fetchall()
            result = []
            for i in table[::-1]:
                if 'chat_id' in i:
                    pass
                else:
                    result.append(i)
            for i in result:
                cursor.execute(f'DELETE FROM {i[0]}')
        logger.warning('Driver - Очистка всех таблиц')

    """Удаление всех таблиц, кроме таблицы chat_id"""
    def delete_all_tables(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM sqlite_master where type="table"')
            table = cursor.fetchall()
            result = []
            for i in table[::-1]:
                if 'chat_id' in i:
                    pass
                else:
                    result.append(i)
            for i in result:
                cursor.execute(f'DROP FROM {i[0]}')
        logger.warning('Driver - Удаление всех таблиц')

    """Удаление одной определённой таблицы"""
    def delete_one_table(self, table):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f'DROP TABLE {table}')
            logger.warning(f'Driver - Удаление таблицы {table}')

    """Возвращает список всех таблиц в БД"""
    def get_all_tbl_names(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM sqlite_master where type="table"')
            tables = cursor.fetchall()
            return tables
