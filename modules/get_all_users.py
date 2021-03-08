import sqlite3
class GetUsers:
    def __init__(self):
            self.db_name = 'mydatabase.db'
    def GetUsers(self):
        '''
        С помощью данной функции мы формируем html код страницы со всеми пользвателя. Результат состоит из суммы
        трех переменных:
        1) html_code_begin - начальная неизменяемая часть
        2) html_code_middle - средняя часть. Наполняется в зависимости от таблицы БД
        3) html_code_end - закрывающий тэг таблицы
        :return:
        final_code - результирующая переменная, представляющая конечный код таблицы
        '''
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""SELECT us.second_name, us.first_name, us.patronymic,reg.region_name, cit.city_name, us.phone, 
                          us.email FROM users us
                          LEFT JOIN regions reg ON us.region_id = reg.id
                          LEFT JOIN cities cit ON us.city_id = cit.id;""")
        all_results = cursor.fetchall()
        conn.close()


        html_code_begin = '''
        <table border="1" cellpadding="5">
    
              <tr>
                    <th>Фамилия</th>
                    <th>Имя</th>
                    <th>Отчество</th>
                    <th>Регион</th>
                    <th>Город</th>
                    <th>Телефон</th>
                    <th>Электронный адрес</th>
              </tr>
      '''
        html_code_middle = ''
        for row in all_results:
            html_row = '''
                    <tr>
                        <th>{}</th>
                        <th>{}</th>
                        <th>{}</th>
                        <th>{}</th>
                        <th>{}</th>
                        <th>{}</th>
                        <th>{}</th>
                    </tr>
            '''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            html_code_middle = html_code_middle + html_row

        html_code_end = '''</table>'''
        final_code = html_code_begin + html_code_middle + html_code_end
        return final_code


if __name__ == '__main__':
    GetUsers()


