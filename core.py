import string
from SQLite3_Db_driver import *


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

    def add_miss(self, table_name, insert):
        self.Db_driver.add_miss(table_name=table_name, insert=insert)

    def show_misses(self, table_name):
        miss_list = self.Db_driver.show_all_miss(table_name=table_name)
        return miss_list

    def update_miss(self, table_name, userid, adding_miss):
        self.Db_driver.update_miss(table_name=table_name, userid=userid, adding_miss=adding_miss)

    def show_id(self, table_name):
        id_list = self.Db_driver.show_id(table_name=table_name)
        return id_list

    def check_login(self, chat_id):
        group = self.Db_driver.check_login(chat_id=chat_id)
        return group

    def clear_miss(self, table_name):
        self.Db_driver.clear_miss(table_name=table_name)

    def clear_one_mis(self, table_name, userid):
        self.Db_driver.clear_one_miss(table_name=table_name, userid=userid)
