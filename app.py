from flask import Flask, request, render_template,redirect,session
from flask_session import Session
import hashlib
import string
import sqlite3

acceptedChars =[ x for x in string.punctuation+string.ascii_letters+string.digits]

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem" 
Session(app) 


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        password = request.form.get('password')
        email = request.form.get('email')
        username = request.form.get('username')
        ConfirmPass = request.form.get('ConfirmPass')
        if len(password) <= 7 or password != ConfirmPass:
            return render_template("error.html", error="Password must be at least 8 characters long")
        for z in password:
            if z not in acceptedChars:
                return render_template("error.html", error="Password must contain at least one special character")
        hashed = hashlib.sha512(password.encode()).hexdigest()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO LoginDetails (Username, Password, Email)
            VALUES (?, ?, ?)
            ''', (username, hashed, email))
        conn.commit()
        conn.close()
        session["username"] = request.form.get("username")
        return render_template("index.html", username = session.get("username"))
    return render_template("signup.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if len(password) <= 7:
            return render_template("error.html", error="Password must be at least 8 characters long")
        hashed = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM LoginDetails WHERE Username = ?", (username,hashed))
    return render_template("login.html")

@app.route("/bookings")
def bookings():
    return render_template("bookings.html", username = session.get("username"))
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)