from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# ==============================
# 🔹 DATABASE CONNECTION
# ==============================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#Project18#",   # তোমার password
    database="Pathfinderdb"
)

cursor = db.cursor()

# ==============================
# 🔹 HOME ROUTE
# ==============================
@app.route('/')
def home():
    return "Flask Running ✅ | Go to /register-student or /register-guide"

# ==============================
# 🔹 STUDENT SECTION
# ==============================

# 👉 Student Form Show
@app.route('/register-student')
def register_student():
    return render_template("register-student.html")

# 👉 Student Data Save
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

# ==============================
# 🔹 GUIDE SECTION
# ==============================

# 👉 Guide Form Show
@app.route('/register-guide')
def register_guide():
    return render_template("register-guide.html")

# 👉 Guide Data Save
@app.route('/register-guide', methods=['POST'])
def register_guide_post():
    name = request.form['name']
    qualification = request.form['qualification']
    sector = request.form['sector']
    email = request.form['email']
    password = request.form['password']

    sql = """
    INSERT INTO guides (name, qualification, sector, email, password)
    VALUES (%s, %s, %s, %s, %s)
    """

    val = (name, qualification, sector, email, password)

    cursor.execute(sql, val)
    db.commit()

    return "Guide Profile Created ✅"

# ==============================
# 🔹 TEST DATABASE
# ==============================
@app.route('/testdb')
def test_db():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return str(tables)

# ==============================
# 🔹 RUN SERVER
# ==============================
if __name__ == "__main__":
    app.run(debug=True)