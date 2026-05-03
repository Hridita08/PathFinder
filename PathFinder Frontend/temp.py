from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
import os

# --- Path Configuration ---
base_dir = os.path.dirname(os.path.abspath(__file__))
# Frontend folder configuration
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
        password="1234",  # Apnar database password
        database="pathfinder_db"
    )

# --- Routes ---

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('main.html', username=session.get('username'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            cursor.close()
            db.close()
            return render_template('main.html', username=user['username'])
        
        cursor.close()
        db.close()
        return render_template('login.html', error="Invalid Credentials")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Post Feature ---

@app.route('/create-post', methods=['POST'])
def create_post():
    content = request.form.get('post_content')
    username = request.form.get('username')
    
    if not content or not username:
        return jsonify({"status": "error", "message": "Content or username missing"}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]
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
        cursor.execute("""
            SELECT posts.id, users.username, posts.content, posts.created_at 
            FROM posts 
            JOIN users ON posts.user_id = users.id 
            ORDER BY posts.created_at DESC
        """)
        posts = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(posts)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Comment Feature ---

@app.route('/add-comment', methods=['POST'])
def add_comment():
    post_id = request.form.get('post_id')
    username = request.form.get('username')
    comment_text = request.form.get('comment_text')
    
    if not comment_text or not post_id or not username:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO comments (post_id, username, content) VALUES (%s, %s, %s)", 
                       (post_id, username, comment_text))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get-comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT username, content FROM comments WHERE post_id = %s ORDER BY id ASC", (post_id,))
        comments = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(comments)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Share & Save Features ---

@app.route('/share-post', methods=['POST'])
def share_post():
    data = request.get_json()
    post_id = data.get('post_id')
    # Optional: Update share count in database if column exists
    return jsonify({"status": "success", "message": "Post shared"})

@app.route('/save-post', methods=['POST'])
def save_post():
    post_id = request.form.get('post_id')
    username = request.form.get('username')
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # Query to save post link to user profile (assuming 'saved_posts' table exists)
        # Table structure: id, username, post_id
        cursor.execute("INSERT INTO saved_posts (username, post_id) VALUES (%s, %s)", (username, post_id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)