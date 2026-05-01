
from flask import Flask
from flask_mysqldb import MySQL
from flask import request, jsonify, session
import random

# Flask app
app = Flask(__name__)

from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.secret_key = 'pathfinder_secret_key'  

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '#Project18#'
app.config['MYSQL_DB'] = 'pathfinder'

mysql = MySQL(app)

# Home route
@app.route('/')
def home():
    return "Connected successfully!"

# Users API
@app.route('/users')
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    return str(data)

    #password login update er kaj

   
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, password FROM users WHERE email=%s AND name=%s", (email, name))
    user = cur.fetchone()

    if user is None:
        return jsonify({"status": "fail", "message": "User not found!"})

    if user[1] != password:
        return jsonify({"status": "fail", "message": "Wrong password!"})

    return jsonify({"status": "success", "user_id": user[0]})

 #password check
    
@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data['email']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET password=%s WHERE email=%s", (password, email))
    mysql.connection.commit()

    if cur.rowcount > 0:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail", "message": "Email not found"})

# profile GET
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    
    row = cur.fetchone()

    if row:
        columns = [col[0] for col in cur.description]
        user = dict(zip(columns, row))
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


# profile UPDATE  ✔️ (separate function)
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json

    name = data.get('name')
    role = data.get('role')
    interests = data.get('interests')
    education = data.get('education')
    expertise = data.get('expertise')
    experience = data.get('experience')
    bio = data.get('bio')
    profile_pic = data.get('profile_pic')

    cur = mysql.connection.cursor()

    student_id = data.get('student_id')

    query = """
    UPDATE users SET 
        name=%s,
        student_id=%s,
        role=%s,
        interests=%s,
        education=%s,
        expertise=%s,
        experience=%s,
        bio=%s,
        profile_pic=%s
    WHERE id=%s
    """

    cur.execute(query, (
        name, student_id , role , interests, education,
        expertise, experience, bio, profile_pic,
        user_id
    ))

    mysql.connection.commit()

    return jsonify({"message": "Profile updated successfully"})
    
# OTP generation and verification

otp_storage = {}
def generate_otp():
    return str(random.randint(1000, 9999))

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data['email']

    otp = generate_otp()
    otp_storage[email] = otp

    print(f"OTP for {email}: {otp}")  # এখন email না পাঠিয়ে console এ দেখাবে

    return jsonify({"message": "OTP sent"})
@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    email = data['email']
    otp = data['otp']

    if otp_storage.get(email) == otp:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})
    

    
    # ১. Message পাঠানো (Post এর Message button)

@app.route('/api/messages/send', methods=['POST'])
def send_message():
    data = request.json
    sender_id = data.get('sender_id')   # frontend থেকে পাঠাবেন
    receiver_id = data.get('receiver_id')
    content = data.get('content')

    if not sender_id:
        return jsonify({'error': 'Login করুন'}), 401

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO messages (sender_id, receiver_id, content) VALUES (%s, %s, %s)",
        (sender_id, receiver_id, content)
    )
    mysql.connection.commit()
    return jsonify({'success': True, 'message': 'Message is sent successfully'})


# ২. Inbox দেখানো (Header এর message icon)
@app.route('/api/messages/inbox/<int:user_id>', methods=['GET'])
def get_inbox(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT m.id, m.content, m.is_read, m.created_at, u.name as sender_name
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.receiver_id = %s
        ORDER BY m.created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    columns = [col[0] for col in cur.description]
    messages = [dict(zip(columns, row)) for row in rows]
    return jsonify({'messages': messages})


# ৩. Unread count (badge number এর জন্য)
@app.route('/api/messages/unread-count/<int:user_id>', methods=['GET'])
def unread_count(user_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM messages WHERE receiver_id = %s AND is_read = FALSE",
        (user_id,)
    )
    count = cur.fetchone()[0]
    return jsonify({'count': count})

# ==================== MESSAGE ROUTES END ====================


# Run server
if __name__ == '__main__':
    app.run(debug=True)

    