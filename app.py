import os
from flask import Flask, send_from_directory, render_template, redirect, url_for, request, jsonify
from flask_socketio import SocketIO
from flask_login import LoginManager, login_user, logout_user
from flask_login.utils import login_required
from flask_restful import Api, Resource, reqparse
from src.user import User
from src.events import Event
from functools import wraps
import json

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='static/html/')
api = Api(app)
socket = SocketIO(app)
app.secret_key = "this is a development secret key"

login_manager = LoginManager(app)

@login_manager.user_loader
def user_loader(email):
    return User.find_by_email(email)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        user = User.find_by_email(email)

        if user and user.verify_password(password):
            login_user(user)
            return redirect('/')
            
        return render_template('login.html')


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
        
        user = User(*values).create()
        login_user(user)
        return redirect('/')
  
@app.route("/")
def homepage():
    return render_template('index.html')
  
@app.route('/events')
@login_required
def events():
    return render_template('events.html')
    

@app.route('/events/all')
@login_required
def list_events():
    response = app.response_class(
        response = json.dumps(Event.all()),
        status = 200,
        mimetype = 'application/json'
    )
    return response

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

    
if __name__ == '__main__':
    app.run(debug=True)
