import sqlite3

class InsertFromForm():
    '''
    Данный класс принимаем в себя список значений. Например,
    ['Орлов', 'Павел', 'Александрович', 'Краснодарский Край', 'Краснодар', '+76666666666', 'alexandr@rambler.ru']
    и импортирует в базу данных.
    Импорт происходит только в том случае если указанный пользователем город имеет id  в базе данных.
    '''
    def __init__(self, param_list):
        self.db_name = "mydatabase.db"
        self.insert_data = param_list
    def InsertData(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Ищем в базе данных id указанного пользователем города
        sql_citi = "SELECT id FROM cities WHERE city_name='{}';".format(self.insert_data[4])
        cursor.execute(sql_citi)
        citi_id = cursor.fetchone()[0]
        # Если указанного пользователем города в базе данных нет, то функция завершает свою работу
        if citi_id == None:
            print('Город не найден в БД. Импорта не будет')
            return False
        else:
            self.insert_data[4] = citi_id
        # Ищем в базе данных id указанного пользователем региона
        sql_region = "SELECT id FROM regions WHERE region_name='{}';".format(self.insert_data[3])
        cursor.execute(sql_region)
        region_id = cursor.fetchone()[0]
        # Если указанного пользователем региона в базе данных нет, то функция завершает свою работу
        if region_id == None:
            print('Регион не найден в БД. Импорта не будет')
            return False
        else:
            self.insert_data[3] = region_id

        # Пытаемся выполнить импорт в базу данных
        try:
            cursor.execute("INSERT INTO users(second_name, first_name, patronymic, region_id, city_id, phone, email) VALUES(?, ?, ?, ?, ?, ?, ?);", self.insert_data)
        except sqlite3.OperationalError as err:
            print(err)

        conn.commit()
        conn.close()
    def sql_select(self, sql):
        # Функция sql селекта для проверки импорта в БД
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(sql)
        all_results = cursor.fetchall()
        conn.close()
        return all_results

if __name__ == '__main__':
    MyClass = InsertFromForm(['Орлов', 'Павел', 'Александрович', 'Краснодарский Край', 'Краснодар', '+76666666666', 'alexandr@rambler.ru'])
    MyClass.InsertData()
    print(MyClass.sql_select("SELECT * FROM users;"))
