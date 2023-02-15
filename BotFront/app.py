from flask import Flask, render_template, url_for, request
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
import ast
from flask import jsonify
from func import *

# creates an application that is named after the name of the file
app = Flask(__name__, static_url_path="")
app.config['JSON_AS_ASCII'] = False


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
    data_push = withdrawUsers_db()
    print(data_push)
    return render_template('table.html')


@app.route('/admin_data', methods=['POST', 'GET'])
def get_tableBox():
    return render_template('tableBox.html')


# if running this module as a standalone program (cf. command in the Python Dockerfile)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
