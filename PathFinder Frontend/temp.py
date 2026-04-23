from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

# 1️⃣ Automatic Path Setup: Eita dile TemplateNotFound error hobe na
# Program jekhanei thakuk, eita current folder-ke template folder hisebe dhorbe
current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=current_dir, 
            static_folder=current_dir,
            static_url_path='')

# 2️⃣ Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="pathfinder_db"
    )

# 3️⃣ Database Setup (Auto table creation)
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
        print("✅ Database & Tables are ready!")
    except Exception as e:
        print(f"❌ DB Setup Error: {e}")

# 4️⃣ Web Route: Show Registration Form
@app.route('/')
def index():
    # Eita ekhon temp.py er pashe thaka register-student.html khujbe
    return render_template('register-student.html')

# 5️⃣ Web Route: Handle Form Submission
@app.route('/create-profile', methods=['POST'])
def create_profile():
    if request.method == 'POST':
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
            
            print(f"✅ Web Registration Successful for: {data[0]}")
            return redirect(url_for('home'))
        except mysql.connector.Error as err:
            return f"❌ Database Error: {err}"

@app.route('/home')
def home():
    return "<h1>🎉 Student Profile Created Successfully!</h1><a href='/'>Back to Register</a>"

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)