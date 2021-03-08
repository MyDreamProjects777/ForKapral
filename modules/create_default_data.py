import sqlite3

class WorkWithDb(object):
    '''
    С помощью данного класса мы создаем базу данных и заполняем ей стандартными данными
    '''
    def __init__(self):
        # Задаем имя базы данных
        self.db_name = "mydatabase.db"
    def create_new_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            # Создание таблицы users
            cursor.execute("""CREATE TABLE users(
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            second_name str,
                            first_name str,
                            patronymic str,
                            region_id int,
                            city_id int,
                            phone str,
                            email str)
                           """)
            # Заполнение таблицы users
            more_users = [('Иванов', 'Иван', 'Иванович', '1', '3', '+79999999999', 'ivanov@rambler.ru'),
                          ('Александров', 'Александр', 'Александрович', '2', '7', '+788888888888', 'alexandr@rambler.ru')]
            cursor.executemany("INSERT INTO users(second_name, first_name, patronymic, region_id, city_id, phone, email) VALUES(?, ?, ?, ?, ?, ?, ?);", more_users)
        except sqlite3.OperationalError as err:
            print(err)

        try:
            # Создание таблицы regions
            cursor.execute("""CREATE TABLE regions(
                            id INTEGER, 
                            region_name str)
                           """)
            # Заполнение таблицы regions
            more_regions = [('0', 'Краснодарский Край'),
                            ('1', 'Ростовская область'),
                            ('2', 'Ставропольский Край'), ]
            cursor.executemany("INSERT INTO regions(id, region_name) VALUES(?,?);", more_regions)
        except sqlite3.OperationalError as err:
            print(err)
        try:
            # Создание таблицы cities
            cursor.execute("""CREATE TABLE cities(
                            id INTEGER,
                            region_id int,
                            city_name str)
                           """)
            # Заполнение таблицы cities
            more_cities = [('0', '0', 'Краснодар'),
                           ('1', '0', 'Кропоткин'),
                           ('2', '0', 'Славянск'),
                           ('3', '1', 'Ростов'),
                           ('4', '1', 'Шахты'),
                           ('5', '1', 'Батайск'),
                           ('6', '2', 'Ставрополь'),
                           ('7', '2', 'Пятигорск'),
                           ('8', '2', 'Кисловодск'), ]
            cursor.executemany("INSERT INTO cities(id,region_id, city_name) VALUES(?, ?, ?);", more_cities)
        except sqlite3.OperationalError as err:
            print(err)
        conn.commit()
        conn.close()
    def sql_select(self, sql):
        # Функция которая по переданному sql запросу выведет результат обращения к БД
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(sql)
        all_results = cursor.fetchall()
        conn.close()
        return all_results

if __name__ == '__main__':
    MyClass = WorkWithDb()
    MyClass.create_new_db()
    print(MyClass.sql_select("SELECT * FROM users;"))
    print(MyClass.sql_select("SELECT id FROM regions WHERE region_name='Краснодарский Край';"))
