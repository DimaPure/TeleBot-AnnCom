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
        val4 = jsonData['time']
        val5 = jsonData['compan']
        val6 = jsonData['crm']
        val7 = jsonData['cardd']
        print(val1, val2, val3, val4, val5, val6, val7)

        try:
            connection = psycopg2.connect(database='BOT',
                                          user='postgres',
                                          password='*******',
                                          host='localhost',
                                          port='5432')
            print('База подключена')
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            cursor.execute(
                f'''INSERT INTO FORM_SITE (name, email, phone, time, compan, crm, card) 
                       VALUES ('{val1}', '{val2}', '{val3}','{val4}', '{val5}', '{val6}','{val7}') on conflict (email) do nothing'''
            )
            print("Данные должны были записаться")
        except (Exception, Error) as error:
            print('Ошибка при работе с PostgreSQL', error)
        finally:
            if connection == True:
                cursor.close()
                connection.close()


# Выгрузка юзеров
def withdrawUsers_db():
    try:
        connection = psycopg2.connect(database='BOT',
                                      user='postgres',
                                      password='CHISTOHIN025134',
                                      host='localhost',
                                      port='5432')
        print('База подключена')

        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from users"

        cursor.execute(postgreSQL_select_Query)
        table_users = cursor.fetchall()

        dict_list = []
        for row in table_users:
            dict_list.append({
                "user_id": row[0],
                "name": row[1],
                "user_name": row[2]
            })
        return dict_list

    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection == True:
            cursor.close()
            connection.close()


# Выгрузка данных с сайта
def withdrawDataSite_db():
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
                "phone": row[2],
                "time": row[3],
                "company": row[4],
                "crm": row[5],
                "card": row[6]
            })
        return dict_list

    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection == True:
            cursor.close()
            connection.close()


# Выгрузка данных из Бота
def withdrawDataBot_db():
    try:
        connection = psycopg2.connect(database='BOT',
                                      user='postgres',
                                      password='CHISTOHIN025134',
                                      host='localhost',
                                      port='5432')
        print('База подключена')

        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from form_bot"

        cursor.execute(postgreSQL_select_Query)
        table_users = cursor.fetchall()

        dict_list = []
        for row in table_users:
            dict_list.append({
                "company": row[0],
                "phone": row[1],
                "email": row[2],
                "name": row[3],
                "time": row[4]
            })
        return dict_list

    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection == True:
            cursor.close()
            connection.close()