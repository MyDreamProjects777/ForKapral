import sqlite3
import xlwt

class export_data_to_excel:
    def __init__(self):
        # Указываем путь к рабочей базе данных
        self.db_name = 'mydatabase.db'
    def sql_select(self, _sql):
        # Функция которая вернет все результаты из переданного select
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(_sql)
        all_results = cursor.fetchall()
        conn.close()
        return all_results


    def export_to_xls(self):
        # Запрос, который выводит данные из таблицы users с полным названием региона и города
        data = self.sql_select("""SELECT us.second_name, us.first_name, us.patronymic,reg.region_name, cit.city_name, us.phone, us.email FROM users us
                            LEFT JOIN regions reg ON us.region_id = reg.id
                            LEFT JOIN cities cit ON us.city_id = cit.id;""")
        # Задаем стили для конечного документа
        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 4
        font0.bold = True
        style0 = xlwt.XFStyle()
        style0.font = font0

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Кандидаты')

        # Создаем заголовки колонок в выходном excel документе
        ws.write(0, 0, 'Фамилия', style0)
        ws.write(0, 1, 'Имя', style0)
        ws.write(0, 2, 'Отчество', style0)
        ws.write(0, 3, 'Регион', style0)
        ws.write(0, 4, 'Город', style0)
        ws.write(0, 5, 'Телефон', style0)
        ws.write(0, 6, 'Электронный адрес', style0)
        # Записываем все данные из sql select в будущий excel файл
        i = 1
        for row in data:
            ws.write(i, 0, row[0])      # Фамилия
            ws.write(i, 1, row[1])      # Имя
            ws.write(i, 2, row[2])      # Отчество
            ws.write(i, 3, row[3])      # Регион
            ws.write(i, 4, row[4])      # Город
            ws.write(i, 5, str(row[5])) # Телефон
            ws.write(i, 6, row[6])      # Электронный адресс
            i = i + 1
        wb.save('results/example.xls')

if __name__ == '__main__':
    MyClass = export_data_to_excel()
    MyClass.export_to_xls()

