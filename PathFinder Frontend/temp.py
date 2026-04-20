from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

# Initialize Flask app
# os.path ensures Flask looks in the exact folder where temp.py is saved
current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=current_dir)
app.secret_key = 'pathfinder_secret_key'

# Function to establish connection with MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="pathfinder_db"
    )

# Route: Home Page (Renders Login Page)
@app.route('/')
def home():
    return render_template('login.html')

# Route: Login Logic
@app.route('/login', methods=['POST'])
def login():
    # Fetch data from the login form
    input_email = request.form.get('email')
    input_password = request.form.get('password')
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Query to verify user credentials from the database
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (input_email, input_password))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user:
        # Success response with basic styling
        return f"""
        <div style="text-align:center; margin-top:50px; font-family:Arial;">
            <h1 style="color:green;">Success!</h1>
            <p>Welcome <b>{user['username']}</b> to PathFinder Dashboard.</p>
            <a href="/" style="text-decoration:none; color:blue;">Logout</a>
        </div>
        """
    else:
        # Reload login page with error message if authentication fails
        return render_template('login.html', error="Invalid Credentials! Please try again.")

# Route: Forgot Password (Step 1)
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
        else:
            return "<h2>Email not found!</h2><a href='/forgot-password'>Try again</a>"
            
    return render_template('forgot_password.html')

# Route: Verify Answer and Reset Password (Step 2)
@app.route('/verify-answer', methods=['POST'])
def verify_answer():
    email = request.form.get('email')
    answer = request.form.get('answer')
    new_password = request.form.get('new_password')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE email=%s AND security_answer=%s", (email, answer))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET password=%s WHERE email=%s", (new_password, email))
        db.commit()
        cursor.close()
        db.close()
        return "<h2>Password reset successful!</h2><a href='/'>Click here to Login</a>"
    else:
        cursor.close()
        db.close()
        return "<h2>Wrong answer!</h2><a href='/forgot-password'>Try again</a>"

# Run the Flask Application
if __name__ == '__main__':
    app.run(debug=True)