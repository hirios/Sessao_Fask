import os
import secrets
import pickle
from datetime import datetime, timedelta
from flask import Flask, session, redirect, escape, request


HEX = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = HEX #os.environ.get(HEX, default=None)


@app.route('/')
def index():
    if 'username' in session:
        ociosidade = pickle.loads(session["temporizador"])
        if ociosidade < datetime.now():
            return redirect('/logout')

        return f'Logged in as {session["username"]}'

    return 'Você não está logado!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ociosidade = pickle.dumps(datetime.now() + timedelta(minutes=5))
        session['username'] = request.form['username']
        session['temporizador'] = ociosidade
        return redirect('/')

    return '''
        <form method="post">
        <p><input type=text name=username>
        <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    #webbrowser.open(f'http://localhost:{PORT}')
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)