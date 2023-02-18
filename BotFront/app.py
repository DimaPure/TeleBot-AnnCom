from flask import Flask, render_template
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


# Переход на админскую страничку
@app.route('/admin_users', methods=['POST', 'GET'])
def get_table():
    data_push = withdrawUsers_db()
    jsonHash = withdrawKey_db()
    return render_template('table.html', jsonStr=data_push, jsonHash=jsonHash)


@app.route('/admin_data', methods=['POST', 'GET'])
def get_tableBox():
    data_push = withdrawDataSite_db()
    data_push2 = withdrawDataBot_db()
    jsonHash = withdrawKey_db()
    return render_template('tableBox.html',
                           jsonStr2=data_push,
                           jsonStr3=data_push2,
                           jsonHash=jsonHash)


# if running this module as a standalone program (cf. command in the Python Dockerfile)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=False)
