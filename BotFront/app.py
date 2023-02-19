from flask import Flask, render_template, redirect
from func import *
from flask import Flask, request, render_template

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


@app.route('/admin_data', methods=['POST', 'GET'])
def login_ad():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        dataAdmin = withdrawDataAdmin_db()
        userdb = dataAdmin[1]
        hashDB = dataAdmin[0]

        if check_password(hashDB, password) and username == userdb:
            data_push1 = withdrawDataSite_db()
            data_push2 = withdrawDataBot_db()
            data_push3 = withdrawUsers_db()
            return render_template('tableBox.html',
                                   jsonStr1=data_push1,
                                   jsonStr2=data_push2,
                                   jsonStr3=data_push3)
        else:
            error = "Попробуйте ещё раз, не все данные верны"
            return render_template('login.html', error=error)

    return render_template('login.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=False)
