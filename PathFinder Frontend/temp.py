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

# ✅ Database Setup (Only Student Table)
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
# 🔵 STUDENT ROUTES
# =========================

# Show student form
@app.route('/')
def student_form():
    return render_template('register-student.html')


# Handle student form
@app.route('/create-profile', methods=['POST'])
def create_profile():
    data = (
        request.form.get('name'),
        request.form.get('student_id'),
        request.form.get('dept'),
        request.form.get('batch'),
        request.form.get('email'),
        request.form.get('phone'),
        request.form.get('password')
    )

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO students (name, student_id, department, batch, email, phone, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, data)
        conn.commit()

        cursor.close()
        conn.close()

        print(f"✅ Student Registered: {data[0]}")
        return redirect(url_for('home'))

    except mysql.connector.Error as err:
        return f"❌ Database Error: {err}"


# =========================
# 🏠 HOME PAGE (Only Student)
# =========================

@app.route('/home')
def home():
    return """
    <h1>🎉 Profile Created Successfully!</h1>
    <a href='/'>Student Register</a>
    """


# =========================
# 🚀 RUN APP
# =========================

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)