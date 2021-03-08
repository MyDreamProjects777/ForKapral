import io
import sqlite3
import sys

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

class ImportFromPdf:
    def __init__(self):
        self.pdf_path = 'РЕЗЮМЕ.pdf'
        self.db_name = 'mydatabase.db'
    def extract_text_from_pdf(self):
        '''
        Функция-обработчик. С помощью неё получаем в виде текста данные для дальнейшего импорта в БД

        :return: текст из pdf
        '''
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(self.pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()

        # close open handles
        converter.close()
        fake_file_handle.close()

        if text:
            return text

    def DataForImport(self, data):
        # Формируем список разделителей для формирования данных
        _splits = ['Ф.И.О:', 'Дата рождения:', 'Национальность:', 'Регион:', 'Город:', 'Семейное положение:', 'Контактный телефон:', 'E-mail:', 'Знание языков:', 'Знание ПК:', 'Личные качества:', 'Желаемая должность:']
        _data = data
        for _split in _splits:
            _data = _data.replace(_split, '***')
        # Создаем универсальный разделитель ***
        begin_data = _data.split('***')
        # Разделяем данные по разделителю
        second_name = begin_data[1].split(' ')[1]
        first_name = begin_data[1].split(' ')[2]
        patronymic = begin_data[1].split(' ')[3]
        region = begin_data[4].strip().replace('край', 'Край')
        city = begin_data[5].strip()
        phone = begin_data[7].replace('+', '').strip()
        email = begin_data[8].strip()
        insert_data = [second_name, first_name, patronymic, region, city, phone, email]
        '''
        Примерный результат который должен получиться
        ['Орлов', 'Павел', 'Александрович', 'Краснодарский Край', 'Краснодар', '+76666666666', 'alexandr@rambler.ru']
        '''
        # ачинаем импорт в БД
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Ищем в базе данных id указанного пользователем города
        sql_city = "SELECT id FROM cities WHERE city_name='{}';".format(insert_data[4])
        cursor.execute(sql_city)
        citi_id = cursor.fetchone()[0]
        # Если указанного пользователем города в базе данных нет, то функция завершает свою работу
        if citi_id == None:
            print('Город не найден в БД. Импорта не будет')
            return False
        else:
            insert_data[4] = citi_id
        # Ищем в базе данных id указанного пользователем региона
        sql_region = "SELECT id FROM regions WHERE region_name='{}';".format(insert_data[3])
        cursor.execute(sql_region)
        region_id = cursor.fetchone()[0]
        # Если указанного пользователем региона в базе данных нет, то функция завершает свою работу
        if region_id == None:
            print('Регион не найден в БД. Импорта не будет')
            return False
        else:
            insert_data[3] = region_id

        # Пытаемся выполнить импорт в базу данных
        try:
            cursor.execute("INSERT INTO users(second_name, first_name, patronymic, region_id, city_id, phone, email) VALUES(?, ?, ?, ?, ?, ?, ?);", insert_data)
        except sqlite3.OperationalError as err:
            print(err)

        conn.commit()
        conn.close()

if __name__ == '__main__':
    MyClass = ImportFromPdf()
    data = MyClass.extract_text_from_pdf()
    MyClass.DataForImport(data)