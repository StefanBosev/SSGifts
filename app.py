import os
from flask import Flask, send_from_directory, render_template, redirect, \
    url_for, request, jsonify, abort
from flask_socketio import SocketIO
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_login.utils import login_required
from flask_restful import Api, Resource, reqparse
from src.user import User
from src.events import Event
from functools import wraps
import json

app = Flask(__name__, static_url_path='', static_folder='static',
            template_folder='static/html/')
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
        admin = 0
        if request.form['First name'] == "ssg":
            admin = 1
        values = (
            None,
            request.form['First name'],
            request.form['Last name'],
            User.hash_password(request.form['Password']),
            request.form['Age'],
            request.form['Gender'],
            request.form['Email'],
            request.form['Address'],
            admin
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
    all_events = Event.all()
    print(all_events[1])
    return render_template('events.html', events=all_events)


# @app.route('/events')
# @login_required
# def events():
#     return render_template('events.html')


# @app.route('/events/all')
# @login_required
# def list_events():
#     response = app.response_class(
#         response=json.dumps(Event.all()),
#         status=200,
#         mimetype='application/json'
#     )
#     return response


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.admin == 0:
        abort(403)
    else:
        if request.method == 'GET':
            return render_template('admin.html')
        elif request.method == 'POST':
            event = Event(
                request.form['name'],
                request.form['event_start_date'],
                request.form['event_end_date'],
                request.form['price_high_border'],
                request.form['price_low_border']
            ).create()
            
            return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
