
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
    return str(data)

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

    