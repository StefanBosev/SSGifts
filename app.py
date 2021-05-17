import os
from flask import Flask, send_from_directory, render_template, redirect, url_for, request, jsonify
from flask_socketio import SocketIO
from flask_restful import Api, Resource, reqparse
from src.user import User
from functools import wraps
import json

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='static/html/')
api = Api(app)
socket = SocketIO(app)

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper


@app.route("/")
def homepage():
    return render_template('index.html')

@app.route('/events', methods=['GET', 'POST'])
@require_login
def events():
    if request.method == 'GET':
        return render_template('events.html')
    return render_template('failed_login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        user = User.find_by_email(email)

        if not user or not user.verify_password(password):
            return jsonify({'token': None})

        token = user.generate_token()
        return jsonify({'token': token.decode('ascii')})
        # return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['First name'],
            request.form['Last name'],
            User.hash_password(request.form['Password']),
            request.form['Age'],
            request.form['Gender'],
            request.form['Email'],
            request.form['Address']
        )
        
        User(*values).create()
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
