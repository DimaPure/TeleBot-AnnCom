from flask import Flask, render_template, url_for, request
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
import ast


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


# Для ссылки admin_users
def withdrawUsers_db():
    try:
        connection = psycopg2.connect(database='BOT',
                                      user='postgres',
                                      password='CHISTOHIN025134',
                                      host='localhost',
                                      port='5432')
        print('База подключена')

        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from form_site"

        cursor.execute(postgreSQL_select_Query)
        table_users = cursor.fetchall()

        dict_list = []
        for row in table_users:
            dict_list.append({
                "name": row[0],
                "email": row[1],
                "phone": row[2]
            })
        return dict_list

    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection == True:
            cursor.close()
            connection.close()