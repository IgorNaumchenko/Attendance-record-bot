import sqlite3
import string


class Db_Driver_Sqlite3:
    def __init__(self, db_name='misses_database.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_new_table(self, userid):
        need = string.ascii_lowercase
        output = [need[int(i)+1] for i in list(str(userid))]
        table_name = ''.join(output)
        create_table = f'CREATE TABLE IF NOT EXISTS {table_name}(userid AUTO_INCREMENT, name TEXT, miss INT);'
        self.connection.cursor().execute(create_table)
        self.connection.commit()
        self.connection.cursor().execute('INSERT INTO chat_id VALUES (?, ?);', (userid, table_name))
        self.connection.commit()

    def create_table(self, table_name):
        create_table = f'CREATE TABLE IF NOT EXISTS {table_name}(userid AUTO_INCREMENT, name TEXT, miss INT);'
        self.connection.cursor().execute(create_table)
        self.connection.commit()

    def add_miss(self, table_name, insert):
        if len(insert) == 1:
            f_text = tuple([i for j in insert for i in j])
            self.cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?);', f_text)
            self.connection.commit()
        if len(insert) > 1:
            self.cursor.executemany(f'INSERT INTO {table_name} VALUES (?, ?, ?);', insert)
            self.connection.commit()

    def show_misses(self, table_name):
        self.cursor.execute(f'SELECT * FROM {table_name};')
        self.connection.commit()
        misses = self.cursor.fetchall()
        return misses

    def update_miss(self, table_name, userid, adding_miss):
        self.cursor.execute(f'UPDATE {table_name} SET miss=miss+{adding_miss} WHERE userid={userid}')
        self.connection.commit()

    def show_id(self, table_name):
        self.cursor.execute(f'SELECT name, userid FROM {table_name}')
        self.connection.commit()
        id_list = self.cursor.fetchall()
        return id_list

    def check_login(self, chai_id):
        self.cursor.execute(f'SELECT group_name FROM chat_id WHERE user_id={chai_id}')
        self.connection.commit()
        group = self.cursor.fetchall()
        return group

    def clear_miss(self, table_name):
        self.cursor.execute(f'UPDATE {table_name} SET miss=0')
        self.connection.commit()
