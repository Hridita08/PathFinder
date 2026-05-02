from flask import Flask, render_template, request, jsonify
import os
import mysql.connector

# --- Path Configuration ---
base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(os.path.dirname(base_dir), 'PathFinder Frontend')

app = Flask(__name__, 
            template_folder=frontend_dir, 
            static_folder=frontend_dir,
            static_url_path='')

app.secret_key = 'pathfinder_secret_key'

# --- Database Connection ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="pathfinder_db"
    )

# --- Routes ---

@app.route('/')
def home():
    return render_template('login.html')

# ---------------- LOGIN ----------------
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
        return render_template('main.html', username=user['username'])
    
    return render_template('login.html', error="Invalid Credentials")

# ---------------- FORGOT PASSWORD ----------------

# Step 1: Email input
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
            return render_template('forgot_password_verify.html',
                                   question=user['security_question'],
                                   email=email)
        else:
            return render_template('forgot_password.html', error="Email not found!")

    return render_template('forgot_password.html')


# Step 2: Verify answer + reset password
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
        message = "Password reset successful!"
    else:
        message = "Wrong answer!"

    cursor.close()
    db.close()

    return message

# ---------------- CREATE POST ----------------
@app.route('/create-post', methods=['POST'])
def create_post():
    content = request.form.get('post_content')
    username = request.form.get('username')
    
    if not content:
        return jsonify({"status": "error", "message": "Content is empty"}), 400
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_result = cursor.fetchone()
        
        if user_result:
            user_id = user_result[0]
            cursor.execute("INSERT INTO posts (user_id, content) VALUES (%s, %s)", (user_id, content))
            db.commit()
            cursor.close()
            db.close()
            return jsonify({"status": "success"})
            
        return jsonify({"status": "error", "message": "User not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- GET POSTS ----------------
@app.route('/get-posts', methods=['GET'])
def get_posts():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT posts.id, users.username, posts.content, posts.created_at 
            FROM posts 
            JOIN users ON posts.user_id = users.id 
            ORDER BY posts.created_at DESC
        """
        cursor.execute(query)
        all_posts = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(all_posts)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- SAVE POST ----------------
@app.route('/save-post', methods=['POST'])
def save_post():
    post_id = request.form.get('post_id')
    username = request.form.get('username')
    
    if not post_id or not username:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM saved_posts WHERE username=%s AND post_id=%s", (username, post_id))
        existing = cursor.fetchone()
        
        if existing:
            cursor.close()
            db.close()
            return jsonify({"status": "info", "message": "Already saved!"})

        cursor.execute("INSERT INTO saved_posts (username, post_id) VALUES (%s, %s)", (username, post_id))
        db.commit()
        
        cursor.close()
        db.close()
        return jsonify({"status": "success", "message": "Saved!"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)