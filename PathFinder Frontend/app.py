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
# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hridita", #
        database="pathfinder", #
        buffered=True 
    )
@app.route('/')
def start_page():
    return render_template('index.html')
# Registration Student
@app.route('/register-student')
def student_form():
    return render_template('register-student.html')

@app.route('/create-profile', methods=['POST'])
def create_profile():
    # ... (ager moto data collect korar logic) ...
    name = request.form.get('name')
    s_id = request.form.get('student_id')
    dept = request.form.get('dept')
    batch = request.form.get('batch')
    email = request.form.get('email')
    phone = request.form.get('phone')
    pw = request.form.get('password')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO students (name, student_id, department, batch, email, phone, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (name, s_id, dept, batch, email, phone, pw))
    conn.commit()
    cursor.close()
    conn.close()
    
   
    return redirect(url_for('login_page'))


@app.route('/login')
def login_page():
    return render_template('login.html')
# Registration guide
@app.route('/create-guide-profile', methods=['POST'])
def create_guide_profile():
    # request.form theke data neya
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
    
    # Guide table-e data insert
    sql = "INSERT INTO guides (name, email, phone, expertise, experience, password) VALUES (%s, %s, %s, %s, %s, %s)"
    
    cursor.execute(sql, data)
    conn.commit()  # Workbench-e save korbe
    
    cursor.close()
    conn.close()
    
    # Registration sheshe login page-e niye jabe
    return redirect(url_for('login_page'))
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Students table check
    cursor.execute("SELECT * FROM students WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    
    # User na pele Guides table check
    if not user:
        cursor.execute("SELECT * FROM guides WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    if user:
        # User-er information session-e save kora
        session['user_id'] = user.get('id')
        session['user_name'] = user.get('name')
        
        # Login success hole main page-e niye jabe
        return redirect(url_for('main_dashboard'))
    # Login fail hole abar login page-e back korbe error shoho
    return render_template('login.html', error="Invalid Email or Password")
#forget-password page
@app.route('/forgot-password')
def forgot_password_page():
    # Ekhane file-er nam hoboho milte hobe
    return render_template('forget-password.html') 

@app.route('/send-reset-link', methods=['POST'])
def send_reset_link():
    email = request.form.get('email')
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # ১. ইমেইলটি ডাটাবেসে আছে কিনা চেক করা
        cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user:
            cursor.execute("SELECT * FROM guides WHERE email=%s", (email,))
            user = cursor.fetchone()
            
        cursor.close()
        db.close()
        
        if user:
            # ২. OTP তৈরি করা
            otp = str(random.randint(1000, 9999))
            otp_storage[email] = otp # টেম্পোরারি স্টোরেজে রাখা
            session['reset_email'] = email # সেশনে ইমেইল সেভ করা
            
            # ৩. টার্মিনালে OTP প্রিন্ট করা (যেহেতু ইমেইল পাঠাচ্ছেন না)
            print("\n" + "="*30)
            print(f"OTP for {email} is: {otp}")
            print("="*30 + "\n")
            
            return render_template('reset-sent.html') # OTP দেওয়ার পেজে নিয়ে যাবে
        else:
            return render_template('forget-password.html', error="Email not registered!")
            
    except Exception as e:
        print(f"Database Error: {e}")
        return f"Error: {str(e)}"
    
def generate_otp():
    return str(random.randint(1000, 9999))

@app.route('/send-otp', methods=['POST'])
def send_otp():
    email = request.json.get('email')
    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400

    otp = generate_otp()
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
    else:
        return jsonify({"status": "fail", "message": "Invalid OTP Code!"})

@app.route('/new-password')
def new_password_page():
    return render_template('new-password.html')
# --- Resource Search Route ---
@app.route('/search')
def search():
    # User-er query input neya
    query = request.args.get('query', '').strip()

    if not query:
        # Jodi query khali thake, search-result page-e khali list pathabe
        return render_template('search-result.html', results=[], query=query)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # SQL Query: resources table theke name ba sector onujayi search
        sql = "SELECT name, sector, description, link FROM resources WHERE name LIKE %s OR sector LIKE %s"
        
        search_term = f"%{query}%"
        cursor.execute(sql, (search_term, search_term))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        # Search Result page-e data pathano
        return render_template('search-result.html', results=results, query=query)

    except Exception as e:
        print(f"Database Error: {e}")
        return "An error occurred while searching. Please check if 'resources' table exists."
# Main & Profile Routes
@app.route('/main') # Route change kore /main kora hoyeche
def main_dashboard():
    if 'user_name' not in session:
        return redirect(url_for('login_page'))
    user_name = session.get('user_name', 'Guest') 
    return render_template('main.html', user_name=user_name)
@app.route('/profile')
def profile_page():
    return render_template('own_profile.html')

@app.route('/get_profile_data', methods=['GET'])
def get_data():
    user_id = session.get('user_id', 1) 
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT full_name, email, student_id, department, profile_pic FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user and user['profile_pic']:
        user['profile_pic'] = base64.b64encode(user['profile_pic']).decode('utf-8')
    cursor.close()
    db.close()
    return jsonify(user)
# --- ১. নোটিফিকেশন এবং ড্যাশবোর্ড আপডেট API ---
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
@app.route('/api/dashboard_updates')
def dashboard_updates():
    user_id = session.get('user_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # নোটিফিকেশন আনা
    cursor.execute("SELECT message, created_at FROM notifications ORDER BY created_at DESC LIMIT 5")
    notifs = cursor.fetchall()
    
    # এই লুপটির আগে ৪টি স্পেস আছে কিনা চেক করুন
    for n in notifs:
        n['time_ago'] = time_ago(n['created_at'])
        n['created_at'] = str(n['created_at'])

    cursor.execute("SELECT COUNT(*) AS count FROM notifications WHERE is_read = 0")
    unread_notif = cursor.fetchone()['count']
    
    # মেসেজ কাউন্ট
    unread_msg = 0
    if user_id:
        cursor.execute("SELECT COUNT(*) AS count FROM messages WHERE receiver_id = %s AND is_read = 0", (user_id,))
        unread_msg = cursor.fetchone()['count']
        
    cursor.close()
    db.close()
    
    return jsonify({
        "notifications": notifs,
        "unread_notif_count": unread_notif,
        "unread_msg_count": unread_msg
    })
if __name__ == '__main__':
    app.run(debug=True)