from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__, 
            template_folder=os.path.dirname(os.path.abspath(__file__)),
            static_folder=os.path.dirname(os.path.abspath(__file__)))

# =========================
# DATABASE CONNECTION
# =========================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#Project18#",
        database="pathfinderdb"
    )

# =========================
# CREATE TABLE
# =========================
def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guides (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        qualification VARCHAR(100),
        sector VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255)
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# =========================
# ROUTES
# =========================

# GUIDE FORM PAGE
@app.route('/')
def guide_form():
    return render_template('register-guide.html')

# FORM SUBMIT
@app.route('/guide-create-profile', methods=['POST'])
def guide_create():
    name = request.form.get('name')
    qualification = request.form.get('qualification')
    sector = request.form.get('sector')
    email = request.form.get('email')
    password = generate_password_hash(request.form.get('password'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # EMAIL CHECK
    cursor.execute("SELECT * FROM guides WHERE email=%s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return "<h3 style='color:red'>❌ this Email is already registered!</h3><a href='/'>← go back</a>"

    # INSERT
    cursor.execute("""
    INSERT INTO guides (name, qualification, sector, email, password)
    VALUES (%s,%s,%s,%s,%s)
    """, (name, qualification, sector, email, password))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('success'))

# SUCCESS PAGE
@app.route('/success')
def success():
    return """
    <div style="font-family:sans-serif;text-align:center;padding:60px">
      <h1 style="color:#2e7d32">🎉 Guide Profile created successfully!</h1>
      <a href="/" style="color:#2e7d32">← New profile create</a>
    </div>
    """

# =========================
# RUN
# =========================
if __name__ == '__main__':
    setup_database()
    app.run(debug=True)