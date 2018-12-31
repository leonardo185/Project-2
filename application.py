import os
import requests

#Flask
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

#Flask Wrappers
from functools import wraps

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
db = scoped_session(sessionmaker(bind=engine))


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first.")
            return render_template('login.html')
    return wrap


#Index
@app.route("/")
def index():
    return render_template('index.html')

#Chat
@app.route("/chat")
@login_required
def chat():
    return render_template('chat.html')

#Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    #Clear all existing sessions.
    session.clear()

    if request.method == 'POST':
        Email = request.form.get('email')
        Password = request.form.get('password')
            
        rows = db.execute("SELECT * FROM users WHERE email=:Email", {"Email":Email}).fetchone()
        print(type(rows))

        if rows == None:
            return render_template('login.html', error = "Invalid Username or Password")
        elif len(rows) != 1 and Password != rows[3]:
            return render_template('login.html', error = "Invalid Username or Password")

        session['logged_in'] = True
        session['user_id'] = rows[0]
        session['user_name'] = rows[1]
        print(session['user_id'])
        return redirect(url_for("chat"))

    return render_template('login.html')

#logout
@app.route("/logout")
@login_required
def logout():
    session.clear()
    return render_template('index.html')

#Register
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        Username = request.form.get('username')
        Email = request.form.get('email')
        Password = request.form.get('password')
        Password_again = request.form.get('password_again')

        db.execute("INSERT INTO users (username, email, password) VALUES (:Username, :Email, :Password)", {"Username": Username, "Email":Email, "Password": Password})
        db.commit()

        flash("You are now register in.")
        return render_template("index.html")
    return render_template("register.html")
