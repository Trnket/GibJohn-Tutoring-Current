from flask import Flask, request, render_template,redirect,session
from flask_session import Session
import hashlib
import string
import sqlite3

acceptedChars =[ x for x in string.punctuation+string.ascii_letters+string.digits]

app = Flask(__name__)

#This section of code is used to create a session so being logged in is trackable accross pages
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem" 
Session(app) 

#This section of code is used to call the index page
@app.route('/')
def index():
    return render_template('index.html', student = session.get("username"), teacher = session.get("username"))

#This section of code is used to call the about us page
@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html' , student = session.get("username"), teacher = session.get("username"))



@app.route("/courses", methods=["POST", "GET"])
def courses():
    return render_template("courses.html", student = session.get("username"), teacher = session.get("username"))



#This section calls the login in selection menu
@app.route("/signup", methods=["POST", "GET"])
def signup():
    return render_template('signup.html', student = session.get("username"), teacher = session.get("username"))


#This section of code is used to call the student sign up page
@app.route("/student_signup", methods=['POST', 'GET'])
def student_signup():
    if request.method == 'POST':
        password = request.form.get('password')
        email = request.form.get('email')
        username = request.form.get('username')
        ConfirmPass = request.form.get('ConfirmPass')
        
        
        #This section of code is used to confirm the password meets the requirements
        if len(password) <= 7 :
            return render_template("error.html", error="Password must be at least 8 characters long")
        if password != ConfirmPass:
            return render_template("error.html", error="Confirm password must match password")
        for z in password:
            if z not in acceptedChars:
                return render_template("error.html", error="Password must contain at least one special character")
        #This code hashes the password making it more secure
        hashed = hashlib.sha512(password.encode()).hexdigest()

        #This section of code connects to the database and adds in the details on a new record
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO LoginDetails (Student, Password, Email)
            VALUES (?, ?, ?)
            ''', (username, hashed, email))
        conn.commit()
        conn.close()

        #This section of code makes the user stay signed in
        session["username"] = request.form.get("username")
        return render_template("index.html", student = session.get("username"))
    return render_template("student_signup.html", student = session.get("username"), teacher = session.get("username"))



#This section of code is used to call the teacher sign up page
@app.route("/teacher_signup", methods=['POST', 'GET'])
def teacher_signup():
    if request.method == 'POST':
        password = request.form.get('password')
        email = request.form.get('email')
        username = request.form.get('username')
        ConfirmPass = request.form.get('ConfirmPass')
        
        
        #This section of code is used to confirm the password meets the requirements
        if len(password) <= 7 :
            return render_template("error.html", error="Password must be at least 8 characters long")
        if password != ConfirmPass:
            return render_template("error.html", error="Confirm password must match password")
        for z in password:
            if z not in acceptedChars:
                return render_template("error.html", error="Password must contain at least one special character")
        #This code hashes the password making it more secure
        hashed = hashlib.sha512(password.encode()).hexdigest()

        #This section of code connects to the database and adds in the details on a new record
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO TeacherDetails (Teacher, Password, Email)
            VALUES (?, ?, ?)
            ''', (username, hashed, email))
        conn.commit()
        conn.close()

        #This section of code makes the user stay signed in
        session["username"] = request.form.get("username")
        return render_template("index.html", teacher = session.get("username"))
    return render_template("teacher_signup.html", student = session.get("username"), teacher = session.get("username"))









#This section calls the login in selection menu
@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template('login.html', student = session.get("username"), teacher = session.get("username"))

#This section of code calls the login student page
@app.route("/student_login", methods=["POST", "GET"])
def student_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        hashed = hashlib.sha512(password.encode()).hexdigest()

        #This section of code connects and searches the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        logCheck = c.execute('''SELECT * FROM LoginDetails WHERE
                              Student = ? AND Password = ?''',(username, hashed)).fetchone()
        if logCheck is None:
            return render_template("error.html", error="Invalid username or password")
        conn.close()

        #This section makes the user stay signed in
        session["username"] = request.form.get("username")
        return render_template("index.html", student = session.get("username"))
    return render_template("student_login.html", student = session.get("username"), teacher = session.get("username"))






#This section of code calls the login teacher page
@app.route("/teacher_login", methods=["POST", "GET"])
def teacher_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        hashed = hashlib.sha512(password.encode()).hexdigest()

        #This section of code connects and searches the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        logCheck = c.execute('''SELECT * FROM TeacherDetails WHERE
                              Teacher = ? AND Password = ?''',(username, hashed)).fetchone()
        if logCheck is None:
            return render_template("error.html", error="Invalid username or password")
        conn.close()

        #This section makes the user stay signed in
        session["username"] = request.form.get("username")
        return render_template("index.html", Teacher = session.get("username"))
    return render_template("teacher_login.html", student = session.get("username"), teacher = session.get("username"))










#This section of code calls the login admin page
@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        hashed = hashlib.sha512(password.encode()).hexdigest()

        #This section of code connects and searches the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        logCheck = c.execute('''SELECT * FROM AdminDetails WHERE
                              Admin = ? AND Password = ?''',(username, hashed)).fetchone()
        if logCheck is None:
            return render_template("error.html", error="Invalid username or password")
        conn.close()

        #This section makes the user stay signed in
        session["username"] = request.form.get("username")
        return render_template("index.html", Admin = session.get("username"))
    return render_template("admin_login.html" , student = session.get("username"), teacher = session.get("username"))






@app.route('/booking', methods=['POST', 'GET'])
def booking():
    if request.method == "POST":
        student_name = request.form['student_name']
        subject = request.form['subject']
        teacher_name = request.form['teacher_name']
        date = request.form['date']
        time = request.form['time']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Bookings (student_name, subject, teacher_name, date, time) VALUES (?, ?, ?, ?, ?)', (student_name, subject, teacher_name, date, time))
        conn.commit()
        cursor.close()
        conn.close()

        return render_template("index.html", Admin = session.get("username"), student = session.get("username"), teacher = session.get("username"))
    return render_template("booking.html", Admin = session.get("username"), student = session.get("username"), teacher = session.get("username"))






#This section of code calls the bookings page
@app.route("/bookings")
def bookings():
    #This section of code makes it so the page can check to see if the user is signed in
    return render_template("bookings.html", student = session.get("username"), teacher = session.get("username"))

#This section logsout the users when called
@app.route("/signout")
def signout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)