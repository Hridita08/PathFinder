from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# ডাটাবেজ কানেকশন
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
    # HTML ফর্ম থেকে আসা ডেটা
    email_input = request.form.get('email')
    password_input = request.form.get('password')
    
    cursor = db.cursor()
    
    # তোমার ডাটাবেজে কলামের নাম 'username', তাই এখানে 'username' ব্যবহার করা হয়েছে
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (email_input, password_input))
    
    user = cursor.fetchone()

    if user:
        return f"Login successful! Welcome {email_input}"
    else:
        # ভুল পাসওয়ার্ড বা ইমেইল দিলে এই মেসেজ দেখাবে
        return "Invalid email or password. Please try again."

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run(debug=True)