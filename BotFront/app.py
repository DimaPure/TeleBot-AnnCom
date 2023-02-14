from flask import Flask, render_template, url_for, request
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# creates an application that is named after the name of the file
app = Flask(__name__, static_url_path="")
app.config['JSON_AS_ASCII'] = False


def push_bd():
    if request.method == "POST":
        jsonData = request.get_json()
        val1 = jsonData['name_py']
        val2 = jsonData['email_py']
        val3 = jsonData['numph_py']
        print(val1, val2, val3)

        try:
            connection = psycopg2.connect(database='BOT',
                                          user='postgres',
                                          password='*******',
                                          host='localhost',
                                          port='5432')
            print('База подключена')
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            cursor.execute(f'''INSERT INTO FORM_SITE (name, email, phone) 
                       VALUES ('{val1}', '{val2}', '{val3}') on conflict (email) do nothing'''
                           )
            print("Данные должны были записаться")
        except (Exception, Error) as error:
            print('Ошибка при работе с PostgreSQL', error)
        finally:
            if connection == True:
                cursor.close()
                connection.close()


@app.route('/', methods=['POST', 'GET'])
def get_index():
    push_bd()
    return render_template('index.html')


@app.route('/hotOffer', methods=['POST', 'GET'])
def get_Hot():
    push_bd()
    return render_template('hotOffer.html')


@app.route('/admin_users', methods=['POST', 'GET'])
def get_table():
    return render_template('table.html')


@app.route('/admin_data', methods=['POST', 'GET'])
def get_tableBox():
    return render_template('tableBox.html')


# if running this module as a standalone program (cf. command in the Python Dockerfile)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=False)
