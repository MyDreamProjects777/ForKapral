from fpdf import FPDF
import sqlite3

class PdfWriter:
    def __init__(self):
        self.output_file = 'results/users.pdf'
        self.db_name = 'mydatabase.db'
    def get_data(self):
        '''
        Забираем данные из базы, спреобразованием id
        Пример результата: ('Александров', 'Александр', 'Александрович', '2', '7', '+788888888888', 'alexandr@rambler.ru')

        :param data: database
        :return: ('Александров', 'Александр', 'Александрович', '2', '7', '+788888888888', 'alexandr@rambler.ru')
        '''
        _sql = """SELECT us.second_name, us.first_name, us.patronymic,reg.region_name, cit.city_name, us.phone, us.email 
                FROM users us
                LEFT JOIN regions reg ON us.region_id = reg.id
                LEFT JOIN cities cit ON us.city_id = cit.id;"""

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(_sql)
        all_results = cursor.fetchall()
        conn.close()
        return all_results

    def create_pdf(self, data):
        '''
        :param data: ('Александров', 'Александр', 'Александрович', '2', '7', '+788888888888', 'alexandr@rambler.ru')
        :return: filename.pdf
        '''
        pdf = FPDF()
        i = 1
        for item in data:
            pdf.add_page()
            pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
            pdf.set_font('DejaVu', '', 14)
            pdf.cell(200, 10, txt="РЕЗЮМЕ №{}".format(i), ln=1, align="C")
            pdf.cell(200, 10, txt="Фамилия: {}".format(item[0]), ln=1, align="L")
            pdf.cell(200, 10, txt="Имя: {}".format(item[1]), ln=1, align="L")
            pdf.cell(200, 10, txt="Отчество: {}".format(item[2]), ln=1, align="L")
            pdf.cell(200, 10, txt="Регион: {}".format(item[3]), ln=1, align="L")
            pdf.cell(200, 10, txt="Город: {}".format(item[4]), ln=1, align="L")
            pdf.cell(200, 10, txt="Телефон: {}".format(item[5]), ln=1, align="L")
            pdf.cell(200, 10, txt="Email: {}".format(item[6]), ln=1, align="L")
            i = i + 1
        pdf.output(self.output_file)

if __name__ == "__main__":
    MyClass = PdfWriter()
    data = MyClass.get_data()
    MyClass.create_pdf(data)