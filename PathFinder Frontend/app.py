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
    from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#Project18#",
    database="Pathfinderdb"
)

cursor = db.cursor()

# 🔹 Home Route
@app.route('/')
def home():
    return "Flask Running ✅"

# 🔹 Registration Page (GET)
@app.route('/register')
def register():
    return render_template("register.html")

# 🔹 Registration Data Save (POST)
@app.route('/register', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    val = (name, email, password)

    cursor.execute(sql, val)
    db.commit()

    return "Registration Successful ✅"
# 🔹 GET → page show 
@app.route('/register-student')
def register_student():
    return render_template("register-student.html")


# 🔹 POST → form data database 
@app.route('/register-student', methods=['POST'])
def register_student_post():
    name = request.form['name']
    student_id = request.form['student_id']
    department = request.form['department']
    batch = request.form['batch']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']

    sql = """
    INSERT INTO users (name, student_id, department, batch, email, phone, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    val = (name, student_id, department, batch, email, phone, password)

    cursor.execute(sql, val)
    db.commit()

    return "Student Profile Created ✅"