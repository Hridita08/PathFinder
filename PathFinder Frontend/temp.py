from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

# ✅ Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=current_dir,
            static_folder=current_dir,
            static_url_path='')

# ✅ Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#Project18#",
        database="pathfinderdb"
    )

# ✅ Database Setup
def setup_database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            student_id VARCHAR(50),
            department VARCHAR(50),
            batch VARCHAR(20),
            email VARCHAR(100),
            phone VARCHAR(20),
            password VARCHAR(100)
        )
        """)

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ Student Table Ready!")

    except Exception as e:
        print(f"❌ DB Setup Error: {e}")


# =========================
# 🔵 STUDENT FORM PAGE
# =========================

@app.route('/')
def student_form():
    return render_template('register-student.html')


# =========================
# 🔵 HANDLE FORM SUBMIT
# =========================

@app.route('/create-profile', methods=['POST'])
def create_profile():
    try:
        # 🔥 HTML er name attribute onujayi data nite hobe
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        dept = request.form.get('dept')
        batch = request.form.get('batch')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO students (name, student_id, department, batch, email, phone, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (name, student_id, dept, batch, email, phone, password))
        conn.commit()

        cursor.close()
        conn.close()

        print(f"✅ Student Registered: {name}")

        return redirect(url_for('home'))

    except mysql.connector.Error as err:
        return f"❌ Database Error: {err}"


# =========================
# 🏠 HOME PAGE
# =========================

@app.route('/home')
def home():
    return """
    <h1>🎉 Profile Created Successfully!</h1>
    <a href='/'>➕ Register Another Student</a>
    """


# =========================
# 🚀 RUN APP
# =========================

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)