import modules.import_from_form
import os.path

from modules.create_default_data import WorkWithDb

from urllib.parse import unquote
from wsgiref.simple_server import make_server
from modules.get_all_users import GetUsers



def web_app(environment, response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    response(status, headers)

    '''При нажатие на отправку формы мы начинаем обрабатывать GET запрос'''
    if environment['PATH_INFO'] == '/insert_data/':
        result_string = environment['QUERY_STRING']
        result_string = unquote(result_string)
        print(result_string)
        second_name = result_string.split('&')[0].split('=')[1]
        first_name = result_string.split('&')[1].split('=')[1]
        patronymic = result_string.split('&')[2].split('=')[1]
        region = result_string.split('&')[3].split('=')[1].replace('+', ' ')
        city = result_string.split('&')[4].split('=')[1]
        telephone = result_string.split('&')[5].split('=')[1]
        email = result_string.split('&')[6].split('=')[1]
        ClassImport = modules.import_from_form.InsertFromForm(
            [second_name, first_name, patronymic, region, city, telephone, email])
        ClassImport.db_name = 'modules/mydatabase.db'
        ClassImport.InsertData()
        return [b'<strong>Data export</strong>']
    # Если пользователь обратился по пути /users/ то выводим ему из БД html код со всеми пользователями
    elif environment['PATH_INFO'] == '/users/' or environment['PATH_INFO'] == '/users':
        HtmlGen = GetUsers()
        HtmlGen.db_name = 'modules/mydatabase.db'
        html = HtmlGen.GetUsers()
        return [html.encode()]
    else:
        return [b'<strong>Hello World I just created my first WSGI</strong>']


if __name__ == '__main__':
    # Выполняем проверку на наличие базы данных. Если база отсутвует, то создаем её
    if os.path.exists("modules/mydatabase.db") == True:
        MyClass = WorkWithDb()
        MyClass.db_name = "modules/mydatabase.db"
        MyClass.create_new_db()

    _port = 8000
    with make_server('', _port, web_app) as server:
        print("Serving on port 8000...\nVisit http://127.0.0.1:8000\n To kill the server enter 'control + C'")
        server.serve_forever()
