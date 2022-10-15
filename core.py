import sqlite3


class Db_Driver_Sqlite3:
    def __init__(self, db_name='misses_database.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name):
        create_table = f'CREATE TABLE IF NOT EXISTS {table_name}(userid INT PRIMARY KEY, name TEXT, miss INT);'
        self.connection.cursor().execute(create_table)
        self.connection.commit()

    def add_miss(self, table_name, ins_tuple):
        self.cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?);', ins_tuple)
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

