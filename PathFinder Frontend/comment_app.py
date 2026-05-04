from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_PATH = 'comments.db'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Home route — browser এ 127.0.0.1:5000 দিলে সরাসরি page দেখাবে
@app.route('/')
def index():
    return send_from_directory('.', 'comment-section.html')


@app.route('/api/comments', methods=['GET'])
def get_comments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify({'success': True, 'comments': [dict(r) for r in rows]})


@app.route('/api/comments', methods=['POST'])
def post_comment():
    data = request.get_json()
    name = data.get('name', '').strip()
    text = data.get('text', '').strip()

    if not name or not text:
        return jsonify({'success': False, 'message': 'Name and text required'}), 400
    if len(text) > 500:
        return jsonify({'success': False, 'message': 'Too long (max 500 chars)'}), 400

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO comments (name, text, created_at) VALUES (?, ?, ?)',
        (name, text, created_at)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        'success': True,
        'comment': {'id': new_id, 'name': name, 'text': text, 'created_at': created_at}
    }), 201


@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


if __name__ == '__main__':
    init_db()
    print("Server running: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)