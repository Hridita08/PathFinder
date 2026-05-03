from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
import os

# --- Path Configuration ---
base_dir = os.path.dirname(os.path.abspath(__file__))
# Pathfinder Career Guidance System project-er frontend folder path
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
        password="1234",  # Apnar MySQL password
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
            return redirect(url_for('home'))
        
        cursor.close()
        db.close()
        return render_template('login.html', error="Invalid Credentials")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/create-post', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    content = request.form.get('post_content')
    user_id = session['user_id']
    
    if not content:
        return jsonify({"status": "error", "message": "Content is empty"}), 400
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO posts (user_id, content) VALUES (%s, %s)", (user_id, content))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get-posts', methods=['GET'])
def get_posts():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        # JOIN babohar kora hoyeche jeno username shoho post ashe
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

@app.route('/add-comment', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    post_id = request.form.get('post_id')
    content = request.form.get('comment_text')
    username = session.get('username')
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO comments (post_id, username, content) VALUES (%s, %s, %s)", 
                       (post_id, username, content))
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
        cursor.execute("SELECT id, username, content FROM comments WHERE post_id = %s ORDER BY id ASC", (post_id,))
        comments = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(comments)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/edit-comment', methods=['POST'])
def edit_comment():
    data = request.get_json()
    comment_id = data.get('id')
    new_content = data.get('content')
    
    if not comment_id or not new_content:
        return jsonify({"status": "error", "message": "Data missing"}), 400
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE comments SET content = %s WHERE id = %s", (new_content, comment_id))
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
    # Pathfinder Career Guidance System development mode
    app.run(debug=True)