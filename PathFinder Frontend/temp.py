from flask import Flask, render_template, request, jsonify
import os
import mysql.connector

# --- Path Configuration ---
# This ensures Flask looks into 'PathFinder Frontend' for HTML, CSS, and JS
base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(os.path.dirname(base_dir), 'PathFinder Frontend')

app = Flask(__name__, 
            template_folder=frontend_dir, 
            static_folder=frontend_dir,
            static_url_path='') # static_url_path='' helps serve files from the root of frontend_dir

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
        # Passes the dynamic username to main.html
        return render_template('main.html', username=user['username'])
    
    return render_template('login.html', error="Invalid Credentials")

@app.route('/create-post', methods=['POST'])
def create_post():
    content = request.form.get('post_content')
    username = request.form.get('username')
    
    if not content:
        return jsonify({"status": "error", "message": "Content is empty"}), 400
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Identify the user ID from the username provided by the frontend
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_result = cursor.fetchone()
        
        if user_result:
            user_id = user_result[0]
            # Insert new post into database
            cursor.execute("INSERT INTO posts (user_id, content) VALUES (%s, %s)", (user_id, content))
            db.commit()
            cursor.close()
            db.close()
            return jsonify({"status": "success"})
            
        return jsonify({"status": "error", "message": "User not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get-posts', methods=['GET'])
def get_posts():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        # Fetch posts with usernames using a JOIN
        query = """
            SELECT users.username, posts.content, posts.created_at 
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

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)