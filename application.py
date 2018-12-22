import os

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template('index.html')

#Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

#Register
@app.route("/register", methods=['GET','POST'])
def register():
    return render_template('register.html')
