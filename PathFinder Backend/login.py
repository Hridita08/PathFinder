from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="pathfinder_db"
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    input_user = request.form.get('email')
    input_password = request.form.get('password')
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (input_user, input_password))
    user = cursor.fetchone()

    if user:
        return f"Success! Welcome {input_user} to PathFinder Dashboard."
    else:
        return "Invalid Credentials! Try again."

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run(debug=True)