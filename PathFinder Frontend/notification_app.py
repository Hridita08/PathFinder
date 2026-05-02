from flask import Flask, render_template, jsonify, request
import mysql.connector
from datetime import datetime
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=current_dir,
            static_folder=current_dir,
            static_url_path='')


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
        id          INT AUTO_INCREMENT PRIMARY KEY,
        message     TEXT NOT NULL,
        type        VARCHAR(50) DEFAULT 'default',
        is_read     TINYINT(1) DEFAULT 0,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    for col, definition in [
        ("is_read",    "TINYINT(1) DEFAULT 0"),
        ("created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("type",       "VARCHAR(50) DEFAULT 'default'")
    ]:
        try:
            cursor.execute(f"ALTER TABLE notifications ADD COLUMN {col} {definition}")
            conn.commit()
        except mysql.connector.Error:
            pass

    cursor.execute("SELECT COUNT(*) FROM notifications")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO notifications (message, type, is_read) VALUES
        ('New guide registered',          'system',  0),
        ('Profile updated successfully',  'update',  0),
        ('You received a new message',    'message', 0)
        """)
        conn.commit()

    cursor.close()
    conn.close()


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#Project18#",
        database="pathfinderdb"
    )


def time_ago(dt):
    if not dt:
        return ""
    diff = datetime.now() - dt
    seconds = int(diff.total_seconds())
    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        return f"{seconds // 60}m ago"
    elif seconds < 86400:
        return f"{seconds // 3600}h ago"
    else:
        return f"{seconds // 86400}d ago"


@app.route('/')
def home():
    return render_template('notification.html')


@app.route('/api/notifications')
def get_notifications():
    limit = request.args.get('limit', 5, type=int)
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, message, type, is_read, created_at
        FROM notifications
        ORDER BY id DESC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS total FROM notifications WHERE is_read = 0")
    unread_count = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    notifications = []
    for r in rows:
        notifications.append({
            "id":       r['id'],
            "message":  r['message'],
            "type":     r['type'] or 'default',
            "is_read":  bool(r['is_read']),
            "time_ago": time_ago(r['created_at'])
        })

    return jsonify({
        "notifications": notifications,
        "unread_count":  unread_count
    })


@app.route('/api/notifications/count')
def get_count():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total FROM notifications WHERE is_read = 0")
    count = cursor.fetchone()['total']
    cursor.close()
    conn.close()
    return jsonify({"unread_count": count})


@app.route('/api/notifications/read/<int:notif_id>', methods=['POST'])
def mark_read(notif_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = %s", (notif_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "ok", "id": notif_id})


@app.route('/api/notifications/read-all', methods=['POST'])
def mark_all_read():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1")
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "ok"})


@app.route('/api/notifications/add', methods=['POST'])
def add_notification():
    data    = request.get_json() or {}
    message = data.get('message', '').strip()
    ntype   = data.get('type', 'default')

    if not message:
        return jsonify({"status": "error", "reason": "empty message"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notifications (message, type, is_read) VALUES (%s, %s, 0)",
        (message, ntype)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({"status": "ok", "id": new_id})


if __name__ == '__main__':
    setup_database()
    app.run(debug=True, port=5003)