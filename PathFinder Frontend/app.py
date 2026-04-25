from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hridita",
    database="pathfinder"
)

cursor = db.cursor()

@app.route("/")
def home():
    return "Server running!"

# INSERT data
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    name = data["name"]
    email = data["email"]

    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.execute(query, (name, email))
    db.commit()

    return jsonify({"message": "User added"})

# FETCH data
@app.route("/get_users", methods=["GET"])
def get_users():
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)