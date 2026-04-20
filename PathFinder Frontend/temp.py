from flask import Flask, render_template, request
import os
import mysql.connector

# Ensure Flask finds HTML files in the same folder
base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=base_dir, static_folder=base_dir)
app.secret_key = 'pathfinder_secret_key'

def get_db_connection():
    return mysql.connector.connect(
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
    email = request.form.get('email')
    password = request.form.get('password')
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    
    if user:
        return f"""
        <div style="text-align:center; margin-top:50px; font-family:Arial;">
            <h1 style="color:green;">Success!</h1>
            <p>Welcome <b>{user['username']}</b> to PathFinder Dashboard.</p>
            <a href="/" style="text-decoration:none; color:blue;">Logout</a>
        </div>
        """
    return render_template('login.html', error="Invalid Credentials")

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT security_question FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        
        if user:
            return render_template('forgot_password_verify.html', question=user['security_question'], email=email)
        return "<h2>Email not found!</h2><a href='/forgot-password'>Try again</a>"
    
    return render_template('forgot_password.html')

@app.route('/verify-answer', methods=['POST'])
def verify_answer():
    email = request.form.get('email')
    answer = request.form.get('answer')
    new_password = request.form.get('new_password')
    
    db = get_db_connection()
    cursor = db.cursor()
    # Check if security answer is correct
    cursor.execute("SELECT * FROM users WHERE email=%s AND security_answer=%s", (email, answer))
    user_record = cursor.fetchone()
    
    if user_record:
        # Update to new password
        cursor.execute("UPDATE users SET password=%s WHERE email=%s", (new_password, email))
        db.commit()
        cursor.close()
        db.close()
        return "<h2>Password reset successful!</h2><a href='/'>Click here to Login</a>"
    
    cursor.close()
    db.close()
    return "<h2>Wrong answer!</h2><a href='/forgot-password'>Try again</a>"

if __name__ == '__main__':
    app.run(debug=True)