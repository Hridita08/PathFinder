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

@app.route('/get-posts', methods=['GET'])
def get_posts():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        # share_count soho fetch korchi jate frontend-e koto bar share hoiche dekhano jay
        query = """
            SELECT posts.id, users.username, posts.content, posts.created_at, posts.share_count 
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

# --- NEW: Comment Route ---
@app.route('/add-comment', methods=['POST'])
def add_comment():
    data = request.json
    post_id = data.get('post_id')
    username = data.get('username')
    content = data.get('content')
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # User ID ber kora
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_res = cursor.fetchone()
        
        if user_res:
            user_id = user_res[0]
            cursor.execute("INSERT INTO comments (post_id, user_id, content) VALUES (%s, %s, %s)", 
                           (post_id, user_id, content))
            db.commit()
            cursor.close()
            db.close()
            return jsonify({"status": "success", "message": "Comment added!"})
            
        return jsonify({"status": "error", "message": "User not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- NEW: Share Route ---
@app.route('/share-post', methods=['POST'])
def share_post():
    data = request.json
    post_id = data.get('post_id')
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # Share count +1 kore update kora
        cursor.execute("UPDATE posts SET share_count = share_count + 1 WHERE id = %s", (post_id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"status": "success", "message": "Post shared!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)