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


@app.route('/login_admin', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # получили логин и пароль ввода пользователя
        username = request.form['username']
        password = request.form['password']
        tableSel = request.form['tableS']

        dataAdmin = withdrawDataAdmin_db()
        userdb = dataAdmin[1]
        hashDB = dataAdmin[0]

        if check_password(hashDB, password) and username == userdb:
            if tableSel == "Пользователи, зашедшие в бота":
                data_push = withdrawUsers_db()
                return render_template('table.html', jsonStrUsers=data_push)
            else:
                data_push1 = withdrawDataSite_db()
                data_push2 = withdrawDataBot_db()
                return render_template('tableBox.html',
                                    jsonStrSite=data_push1,
                                    jsonStrBot=data_push2)
        else:
            error = "Попробуйте ещё раз, не все данные верны"
            return render_template('login.html', error=error)


    return render_template('login.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=False)
