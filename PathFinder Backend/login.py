from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'pathfinder_secret_key'

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
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (input_user, input_password))
    user = cursor.fetchone()

    if user:
        return f"Success! Welcome {user['username']} to PathFinder Dashboard."
    else:
        return "Invalid Credentials! Try again."

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT security_question FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            return render_template('forgot_password_verify.html', question=user['security_question'], email=email)
        else:
            return "Email not found!"
            
    return render_template('forgot_password.html')

@app.route('/verify-answer', methods=['POST'])
def verify_answer():
    email = request.form.get('email')
    answer = request.form.get('answer')
    new_password = request.form.get('new_password')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND security_answer=%s", (email, answer))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET password=%s WHERE email=%s", (new_password, email))
        db.commit()
        return "Password reset successful! <a href='/'>Login now</a>"
    else:
        return "Wrong answer to the security question!"

if __name__ == '__main__':
    app.run(debug=True)