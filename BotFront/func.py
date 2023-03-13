from flask import request
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# database='for_bots',
# user='wisdom',
# password='vZSi#6j?X$',
# host='localhost',
# port='5432'

# database='BOT',
#                                   user='postgres',
#                                   password='CHISTOHIN025134',
#                                   host='localhost',
#                                   port='5432'


def ConDB():
    connection = psycopg2.connect(database='for_bots',
                                  user='wisdom',
                                  password='vZSi#6j?X$',
                                  host='localhost',
                                  port='5432')
    return connection


# Отправка данных в бд
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
            connection = ConDB()
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
        connection = ConDB()
        print('База подключена')

        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from users"

        cursor.execute(postgreSQL_select_Query)
        table_users = cursor.fetchall()

        dict_list = []
        for row in table_users:
            dict_list.append({
                "user_id": str(row[0]),
                "name": str(row[1]),
                "user_name": str(row[2]),
                "time": str(row[3])
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
        connection = ConDB()
        print('База подключена')

        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from form_site"

        cursor.execute(postgreSQL_select_Query)
        table_users = cursor.fetchall()

        dict_list = []
        for row in table_users:
            dict_list.append({
                "name": str(row[0]),
                "email": str(row[1]),
                "phone": str(row[2]),
                "time": str(row[3]),
                "company": str(row[4]),
                "crm": str(row[5]),
                "card": str(row[6])
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
        connection = ConDB()
        print('База подключена')

        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from form_bot"

        cursor.execute(postgreSQL_select_Query)
        table_users = cursor.fetchall()

        dict_list = []
        for row in table_users:
            dict_list.append({
                "company": str(row[0]),
                "phone": str(row[1]),
                "email": str(row[3]),
                "name": str(row[2]),
                "time": str(row[4]),
                "username": str(row[5])
            })
        return dict_list

    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection == True:
            cursor.close()
            connection.close()


def withdrawDataAdmin_db():
    try:
        connection = ConDB()
        print('База подключена')

        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from safe"

        cursor.execute(postgreSQL_select_Query)
        table_users = cursor.fetchall()

        dataAd = []
        for row in table_users:
            dataAd.append(str(row[0]))
            dataAd.append(str(row[1]))
        return dataAd

    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection == True:
            cursor.close()
            connection.close()
