from flask import Flask
import mysql.connector

app = Flask(__name__)

# 🔹 DATABASE CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#Project18#",   # তোমার password
    database="Pathfinderdb"
)

cursor = db.cursor()

# 🔹 TEST ROUTE
@app.route('/')
def home():
    return "Flask + MySQL Connected Successfully ✅"

# 🔹 TEST DATABASE ROUTE
@app.route('/testdb')
def test_db():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return str(tables)

if __name__ == "__main__":
    app.run(debug=True)