from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import mysql.connector
import base64
import random

app = Flask(__name__,
            template_folder=".",
            static_folder=".",
            static_url_path='')
app.secret_key = "your_secret_key"
otp_storage = {}

# ==================== DATABASE ====================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hridita",
        database="pathfinder",
        buffered=True
    )

# ==================== PAGES ====================
@app.route('/')
def start_page():
    return render_template('index.html')

@app.route('/main')
def main_dashboard():
    if 'user_name' not in session:
        return redirect(url_for('login_page'))
    return render_template('main.html', user_name=session.get('user_name', 'Guest'))

@app.route('/inbox')
def inbox_page():
    # FIX: Do NOT redirect to login. Render inbox and let JS handle session fallback.
    return render_template('inbox.html')

@app.route('/profile')
def profile_page():
    if 'user_name' not in session:
        return redirect(url_for('login_page'))
    return render_template('own_profile.html')

@app.route('/settings')
def settings_page():
    return render_template('settings.html')

@app.route('/saved-posts')
def saved_posts_page():
    if 'user_name' not in session:
        return redirect(url_for('login_page'))
    return render_template('saved_posts.html')

@app.route('/technical')
def technical_page():
    return render_template('technical.html')

@app.route('/non-technical')
def non_technical_page():
    return render_template('non-technical.html')

# ==================== AUTH ====================
@app.route('/register-student')
def student_form():
    return render_template('register-student.html')

@app.route('/create-profile', methods=['POST'])
def create_profile():
    name = request.form.get('name')
    s_id = request.form.get('student_id')
    dept = request.form.get('dept')
    batch = request.form.get('batch')
    email = request.form.get('email')
    phone = request.form.get('phone')
    pw = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO students (name, student_id, department, batch, email, phone, password) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (name, s_id, dept, batch, email, phone, pw))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')

    # POST: handle login
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if not email or not password:
        return render_template('login.html', error='Please enter email and password')

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        user = None
        user_type = None

        try:
            cursor.execute("SELECT * FROM students WHERE email=%s AND password=%s", (email, password))
            user = cursor.fetchone()
            if user:
                user_type = 'student'
        except Exception as e:
            print(f'Students login error: {e}')

        if not user:
            try:
                cursor.execute("SELECT * FROM guides WHERE email=%s AND password=%s", (email, password))
                user = cursor.fetchone()
                if user:
                    user_type = 'guide'
            except Exception as e:
                print(f'Guides login error: {e}')

        cursor.close()
        db.close()

        if user:
            user_name = (
                user.get('name') or user.get('full_name') or
                user.get('username') or email.split('@')[0]
            )
            session['user_id'] = user.get('id')
            session['user_name'] = user_name
            session['user_email'] = user.get('email', email)
            session['user_type'] = user_type
            print(f'Login OK: {user_name} id={user.get("id")} type={user_type}')
            return redirect(url_for('main_dashboard'))

        # Better error message
        try:
            db2 = get_db_connection()
            c2 = db2.cursor(dictionary=True)
            c2.execute("SELECT id FROM students WHERE email=%s", (email,))
            exists = c2.fetchone()
            if not exists:
                c2.execute("SELECT id FROM guides WHERE email=%s", (email,))
                exists = c2.fetchone()
            c2.close()
            db2.close()
            error = 'Incorrect password. Please try again.' if exists else 'No account found with this email.'
        except Exception:
            error = 'Invalid email or password.'

        return render_template('login.html', error=error)

    except Exception as e:
        print(f'Login exception: {e}')
        return render_template('login.html', error=f'Server error: {str(e)}')

@app.route('/create-guide-profile', methods=['POST'])
def create_guide_profile():
    data = (
        request.form.get('name'),
        request.form.get('email'),
        request.form.get('phone'),
        request.form.get('expertise'),
        request.form.get('experience'),
        request.form.get('password')
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO guides (name, email, phone, expertise, experience, password) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('login_page'))

# (POST login handled above in login_page)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# ==================== FORGOT PASSWORD ====================
@app.route('/forgot-password')
def forgot_password_page():
    return render_template('forget-password.html')

@app.route('/send-reset-link', methods=['POST'])
def send_reset_link():
    email = request.form.get('email')
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user:
            cursor.execute("SELECT * FROM guides WHERE email=%s", (email,))
            user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            otp = str(random.randint(1000, 9999))
            otp_storage[email] = otp
            session['reset_email'] = email
            print(f"\n{'='*30}\nOTP for {email}: {otp}\n{'='*30}\n")
            return render_template('reset-sent.html')
        else:
            return render_template('forget-password.html', error="Email not registered!")
    except Exception as e:
        print(f"DB Error: {e}")
        return f"Error: {str(e)}"

@app.route('/send-otp', methods=['POST'])
def send_otp():
    email = request.json.get('email')
    if not email:
        return jsonify({"status": "error", "message": "Email required"}), 400
    otp = str(random.randint(1000, 9999))
    otp_storage[email] = otp
    print(f"OTP for {email}: {otp}")
    return jsonify({"status": "success", "message": "OTP sent to console"})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = session.get('reset_email')
    user_otp = data.get('otp')
    if email in otp_storage and otp_storage[email] == user_otp:
        return jsonify({"status": "success", "redirect": url_for('new_password_page')})
    return jsonify({"status": "fail", "message": "Invalid OTP!"})

@app.route('/new-password')
def new_password_page():
    return render_template('new-password.html')

# ==================== SEARCH ====================
@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return render_template('search-result.html', results=[], query=query)
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT name, sector, description, link FROM resources WHERE name LIKE %s OR sector LIKE %s"
        term = f"%{query}%"
        cursor.execute(sql, (term, term))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('search-result.html', results=results, query=query)
    except Exception as e:
        print(f"DB Error: {e}")
        return "Search error. Please check if 'resources' table exists."

# ==================== PROFILE ====================
@app.route('/get_profile_data', methods=['GET'])
def get_data():
    user_id = session.get('user_id')

    # No session — return what we know from session (no 401, just minimal data)
    if not user_id:
        return jsonify({
            "full_name": session.get('user_name', ''),
            "email": session.get('user_email', ''),
            "student_id": None,
            "department": None,
            "profile_pic": None
        })

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    user = None

    # Try students table
    try:
        cursor.execute(
            "SELECT name AS full_name, email, student_id, department FROM students WHERE id=%s",
            (user_id,)
        )
        user = cursor.fetchone()
    except Exception as e:
        print(f"Students query error: {e}")

    # Try guides table
    if not user:
        try:
            cursor.execute(
                "SELECT name AS full_name, email, NULL AS student_id, expertise AS department FROM guides WHERE id=%s",
                (user_id,)
            )
            user = cursor.fetchone()
        except Exception as e:
            print(f"Guides query error: {e}")

    if user:
        user['profile_pic'] = None

    # ALWAYS try to get profile_pic from users table (separate from student/guide data)
    try:
        cursor.execute("SELECT profile_pic FROM users WHERE id=%s", (user_id,))
        pic_row = cursor.fetchone()
        if pic_row and pic_row.get('profile_pic'):
            pic_b64 = base64.b64encode(pic_row['profile_pic']).decode('utf-8')
            if user:
                user['profile_pic'] = pic_b64
            else:
                # users table has full profile
                cursor.execute("SELECT full_name, email, student_id, department, profile_pic FROM users WHERE id=%s", (user_id,))
                user = cursor.fetchone()
                if user and user.get('profile_pic') and isinstance(user['profile_pic'], (bytes, bytearray)):
                    user['profile_pic'] = base64.b64encode(user['profile_pic']).decode('utf-8')
    except Exception as e:
        print(f"Profile pic fetch error: {e}")

    cursor.close()
    db.close()

    if user:
        if not user.get('full_name'):
            user['full_name'] = session.get('user_name', 'User')
        return jsonify(user)

    return jsonify({
        "full_name": session.get('user_name', 'User'),
        "email": session.get('user_email', ''),
        "student_id": None,
        "department": None,
        "profile_pic": None
    })

@app.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

    db = get_db_connection()
    cursor = db.cursor()

    name = request.form.get('name')
    student_id_val = request.form.get('student_id')
    email = request.form.get('email')
    dept = request.form.get('dept')
    image_file = request.files.get('image')

    try:
        # Update name/info in students table
        if name:
            try:
                cursor.execute(
                    "UPDATE students SET name=%s, student_id=%s, email=%s, department=%s WHERE id=%s",
                    (name, student_id_val, email, dept, user_id)
                )
                db.commit()
                session['user_name'] = name
            except Exception:
                # Try guides table
                cursor.execute(
                    "UPDATE guides SET name=%s, email=%s WHERE id=%s",
                    (name, email, user_id)
                )
                db.commit()
                session['user_name'] = name

        # Handle profile picture upload — store in users table if it exists
        if image_file and image_file.filename:
            image_data = image_file.read()
            try:
                # Try to update existing row
                cursor.execute("UPDATE users SET profile_pic=%s WHERE id=%s", (image_data, user_id))
                if cursor.rowcount == 0:
                    # Insert new row if not exists
                    cursor.execute(
                        "INSERT INTO users (id, profile_pic) VALUES (%s, %s) ON DUPLICATE KEY UPDATE profile_pic=%s",
                        (user_id, image_data, image_data)
                    )
                db.commit()
            except Exception as img_err:
                print(f"Profile pic save error: {img_err}")
                # Not fatal — frontend saves to localStorage anyway

    except Exception as e:
        cursor.close()
        db.close()
        print(f"Update profile error: {e}")
        return jsonify({"status": "error", "message": str(e)})

    cursor.close()
    db.close()
    return jsonify({"status": "success"})

@app.route('/remove_profile_pic', methods=['POST'])
def remove_profile_pic():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error"}), 401
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET profile_pic=NULL WHERE id=%s", (user_id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ==================== NOTIFICATIONS ====================
def time_ago(dt):
    if not dt:
        return ""
    diff = datetime.now() - dt
    seconds = int(diff.total_seconds())
    if seconds < 60: return "Just now"
    elif seconds < 3600: return f"{seconds // 60}m ago"
    elif seconds < 86400: return f"{seconds // 3600}h ago"
    else: return f"{seconds // 86400}d ago"

@app.route('/api/dashboard_updates')
def dashboard_updates():
    user_id = session.get('user_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT message, created_at FROM notifications ORDER BY created_at DESC LIMIT 5")
    notifs = cursor.fetchall()
    for n in notifs:
        n['time_ago'] = time_ago(n['created_at'])
        n['created_at'] = str(n['created_at'])

    cursor.execute("SELECT COUNT(*) AS count FROM notifications WHERE is_read=0")
    unread_notif = cursor.fetchone()['count']

    unread_msg = 0
    if user_id:
        try:
            cursor.execute("SELECT COUNT(*) AS count FROM messages WHERE receiver_id=%s AND is_read=0", (user_id,))
            unread_msg = cursor.fetchone()['count']
        except:
            pass

    cursor.close()
    db.close()

    return jsonify({
        "notifications": notifs,
        "unread_notif_count": unread_notif,
        "unread_msg_count": unread_msg
    })

# ==================== MESSAGES API ====================
@app.route('/api/messages/inbox/<int:user_id>')
def get_inbox(user_id):
    """Get all messages for a user"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.*, 
                   s.name as sender_name, 
                   r.name as receiver_name
            FROM messages m
            LEFT JOIN students s ON m.sender_id = s.id
            LEFT JOIN students r ON m.receiver_id = r.id
            WHERE m.sender_id=%s OR m.receiver_id=%s
            ORDER BY m.created_at DESC
        """, (user_id, user_id))
        messages = cursor.fetchall()
        for msg in messages:
            if msg.get('created_at'):
                msg['created_at'] = str(msg['created_at'])
        cursor.close()
        db.close()
        return jsonify({"messages": messages})
    except Exception as e:
        print(f"Inbox error: {e}")
        return jsonify({"messages": [], "error": str(e)})

@app.route('/api/messages/send', methods=['POST'])
def send_message():
    """Send a message"""
    data = request.json
    sender_id = data.get('sender_id') or session.get('user_id')
    receiver_id = data.get('receiver_id')
    receiver_name = data.get('receiver_name')
    sender_name = data.get('sender_name') or session.get('user_name')
    content = data.get('content', '')
    post_ref = data.get('post_ref', '')

    if not content:
        return jsonify({"status": "error", "message": "Content required"}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Resolve receiver_id from name if not provided
        if not receiver_id and receiver_name:
            cursor.execute("SELECT id FROM students WHERE name=%s LIMIT 1", (receiver_name,))
            row = cursor.fetchone()
            if not row:
                cursor.execute("SELECT id FROM guides WHERE name=%s LIMIT 1", (receiver_name,))
                row = cursor.fetchone()
            if row:
                receiver_id = row['id']

        if sender_id and receiver_id:
            cursor.execute("""
                INSERT INTO messages (sender_id, receiver_id, content, post_ref, is_read, created_at)
                VALUES (%s, %s, %s, %s, 0, NOW())
            """, (sender_id, receiver_id, content, post_ref))
            db.commit()

        cursor.close()
        db.close()
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Send message error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ==================== SESSION INFO (for JS) ====================
@app.route('/api/me')
def get_me():
    """Return current session user info for JS"""
    return jsonify({
        "user_id": session.get('user_id', 0),
        "user_name": session.get('user_name', ''),
        "logged_in": 'user_id' in session
    })

if __name__ == '__main__':
    app.run(debug=True)