from flask import Flask, render_template
import mysql.connector
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=current_dir,
            static_folder=current_dir,
            static_url_path='')

# ✅ Auto DB Setup
def setup_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="#Project18#"
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS pathfinderdb")
    cursor.execute("USE pathfinderdb")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INT AUTO_INCREMENT PRIMARY KEY,
        message TEXT
    )
    """)

    # Insert sample data if empty
    cursor.execute("SELECT COUNT(*) FROM notifications")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
        INSERT INTO notifications (message) VALUES
        ('New guide registered'),
        ('Profile updated successfully'),
        ('You received a message')
        """)
        conn.commit()

    cursor.close()
    conn.close()


# DB connect
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#Project18#",
        database="pathfinderdb"
    )


# ✅ Route
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM notifications ORDER BY id DESC LIMIT 5")
    notifications = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS total FROM notifications")
    count = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    return render_template('notification.html',
                           notifications=notifications,
                           count=count)


# RUN
if __name__ == '__main__':
    setup_database()
    app.run(debug=True, port=5003)