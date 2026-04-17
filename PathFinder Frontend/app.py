from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#Project18#",
    database="Pathfinderdb"
)

cursor = db.cursor()

# 👉 LOGIN PAGE SHOW
@app.route('/')
def login_page():
    return render_template("login.html")


# 👉 REGISTER PAGE SHOW
@app.route('/register')
def register_page():
    return render_template("register.html")


# 👉 REGISTER FUNCTION (MAIN)
@app.route('/registerUser', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    cursor.execute(
        "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
        (name, email, password)
    )
    db.commit()

    return redirect("/")


# 👉 LOGIN FUNCTION
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cursor.fetchone()

    if user:
        return render_template("dashboard.html")
    else:
        return "Invalid Login ❌"


if __name__ == "__main__":
    app.run(debug=True)