from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=current_dir,
            static_folder=current_dir,
            static_url_path='')

# DB connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#Project18#",
        database="pathfinderdb"
    )

# Create guide table
def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guides (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        qualification VARCHAR(100),
        sector VARCHAR(100),
        email VARCHAR(100),
        password VARCHAR(100)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# =========================
# GUIDE ROUTES
# =========================

@app.route('/')
def guide_form():
    return render_template('register-guide.html')


@app.route('/guide-create-profile', methods=['POST'])
def guide_create():
    data = (
        request.form.get('name'),
        request.form.get('qualification'),
        request.form.get('sector'),
        request.form.get('email'),
        request.form.get('password')
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO guides (name, qualification, sector, email, password)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(sql, data)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('success'))


@app.route('/success')
def success():
    return """
    <h1>🎉 Guide Profile Created Successfully!</h1>
    <a href='/'>Register Another Guide</a>
    """

# RUN
if __name__ == '__main__':
    setup_database()
    app.run(debug=True)