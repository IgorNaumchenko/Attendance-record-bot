import sqlite3


class Db_Driver:
    """Класс работы с базой данных"""
    def __init__(self, db_name='misses_database.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)

    """Добавление пользователя в таблицу юзеров и создание отдельной таблицы под группу пользователя"""
    def create_new_table(self, userid, table_name):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name}(userid AUTO_INCREMENT, name TEXT, miss INT);')
            self.connection.commit()
            cursor.execute('INSERT INTO chat_id VALUES (?, ?);', (userid, table_name))
            self.connection.commit()

    """Добавление пропуска в таблицу пользователя, входной tuple"""
    def add_miss(self, table_name, insert):
        with self.connection as conn:
            cursor = conn.cursor()
            if len(insert) == 1:
                miss_tup = tuple([i for j in insert for i in j])
                cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?);', miss_tup)
            elif len(insert) > 1:
                cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?);', insert)
            self.connection.commit()

    """Возвращает список всех пропусков из определённой таблицы"""
    def show_all_miss(self, table_name):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name};')
        self.connection.commit()
        misses = cursor.fetchall()
        return misses

    """Добавляет пропуск с существущему уже в таблице"""
    def update_miss(self, table_name, userid, adding_miss):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE {table_name} SET miss=miss+{adding_miss} WHERE userid={userid}')
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
    def clear_miss(self, table_name):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE {table_name} SET miss=0')
        self.connection.commit()

    """Удаляет запись одного студента(уник.номер, имя, кол-во пропусков) в таблице группы"""
    def clear_one_miss(self, table_name, userid):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM {table_name} WHERE userid={userid}')
        self.connection.commit()
