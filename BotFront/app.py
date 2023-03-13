from flask import Flask, render_template, redirect
from func import *
from flask import Flask, request, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

# security
auth = HTTPBasicAuth()

dataAdmin = withdrawDataAdmin_db()
userdb = dataAdmin[1]
hashDB = dataAdmin[0]

USERS = {userdb: hashDB}


@auth.verify_password
def verify_password(username, password):
    if username in USERS:
        return check_password_hash(USERS.get(username), password)
        return False


# creates an application that is named after the name of the file
app = Flask(__name__, static_url_path="")
app.config['JSON_AS_ASCII'] = False
# bootstrap = Bootstrap(app)


@app.route('/', methods=['POST', 'GET'])
def get_index():
    push_bd()
    return render_template('index.html')


@app.route('/hotOffer', methods=['POST', 'GET'])
def get_Hot():
    push_bd()
    return render_template('hotOffer.html')


@app.route('/aboutCompany', methods=['POST', 'GET'])
def get_about():
    push_bd()
    return render_template('aboutCompany.html')


@app.route('/botN', methods=['POST', 'GET'])
def get_bot():
    push_bd()
    return render_template('botN.html')


@app.route('/users', methods=['POST', 'GET'])
@auth.login_required
def get_users():
    data_push = withdrawUsers_db()
    return render_template('table.html', jsonStrUsers=data_push)


@app.route('/data', methods=['POST', 'GET'])
@auth.login_required
def get_data():
    data_push1 = withdrawDataSite_db()
    data_push2 = withdrawDataBot_db()
    return render_template('tableBox.html',
                           jsonStrSite=data_push1,
                           jsonStrBot=data_push2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=False)
