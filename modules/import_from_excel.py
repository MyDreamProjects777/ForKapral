import sqlite3
import xlrd

class export_data_to_excel:
    '''
        Работа класса состоит из двух этапов:
        1) Формирование списка данных для импорта в БД(Функция read_xls)
        2) Импорт данных на основании сформированной переменной self.all_data_from_excel с помощью функции sql_insert

    '''
    def __init__(self, xls_file):
        # Указываем имя рабочей БД
        self.db_name = 'mydatabase.db'
        self.xls_file = xls_file
        self.all_data_from_excel = []
    def sql_insert(self):
        # Функция, которая импортирует переданные из excel файла данные
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.executemany(
            """INSERT INTO users(second_name, first_name, patronymic, region_id, city_id, phone, email)
                VALUES(?, ?, ?, ?, ?, ?, ?);""", self.all_data_from_excel)
        conn.commit()
        conn.close()

    def read_xls(self):
        '''
        Парсим xls файл для получения данных.
        Если указанный пользователем город отсутвует в базе то импорт будет прерван
        '''
        rb = xlrd.open_workbook(self.xls_file, formatting_info=True)
        sheet = rb.sheet_by_index(0)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            if row != ['Фамилия', 'Имя', 'Отчество', 'Регион', 'Город', 'Телефон', 'Электронный адрес']:
                sql_citi = "SELECT id FROM cities WHERE city_name='{}';".format(row[4])
                cursor.execute(sql_citi)
                citi_id = cursor.fetchone()[0]
                if citi_id == None:
                    print('Город не найден в БД. Импорта не будет')
                    continue
                else:
                    row[4] = citi_id

                sql_region = "SELECT id FROM regions WHERE region_name='{}';".format(row[3])
                cursor.execute(sql_region)
                region_id = cursor.fetchone()[0]
                if region_id  == None:
                    print('Регион не найден в БД. Импорта не будет')
                    continue
                else:
                    row[3] = region_id
                # Все данные вносим в глобаную переменную класса для обработки функцией sql_insert
                self.all_data_from_excel.append(row)

        conn.close()

if __name__ == '__main__':
    MyClass = export_data_to_excel('results/example.xls')
    MyClass.read_xls()
    MyClass.sql_insert()

