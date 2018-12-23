import os
import requests

#Flask
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

#Socket.io
from flask_socketio import SocketIO, emit

#Database and Sessions
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_se ssion(sessionmaker(bind=engine))


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
