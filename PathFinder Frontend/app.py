
from flask import Flask
from flask_mysqldb import MySQL

from flask import request, jsonify
import random



# Flask app
app = Flask(__name__)

from flask_cors import CORS
CORS(app)

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
    # return str(data)
    

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
        interests=%s,
        education=%s,
        expertise=%s,
        experience=%s,
        bio=%s,
        profile_pic=%s
    WHERE id=%s
    """

    cur.execute(query, (
        name, student_id , interests, education,
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
    

# Run server
if __name__ == '__main__':
    app.run(debug=True)

    