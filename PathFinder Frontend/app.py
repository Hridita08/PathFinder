from flask import Flask, render_template, request, jsonify, session
import mysql.connector
import base64

app = Flask(__name__, template_folder=".")
app.secret_key = "your_secret_key"

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hridita",
        database="pathfinder"
    )
# Registration Student
@app.route('/register-student')
def student_form():
    return render_template('register-student.html')

@app.route('/create-profile', methods=['POST'])
def create_profile():
    data = (
        request.form.get('name'), request.form.get('student_id'),
        request.form.get('dept'), request.form.get('batch'),
        request.form.get('email'), request.form.get('phone'),
        request.form.get('password')
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO students (name, student_id, department, batch, email, phone, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('profile_page'))

@app.route('/register-guide')
def guide_form():
    return render_template('register-guide.html')

@app.route('/create-guide-profile', methods=['POST'])
def create_guide_profile():
    data = (
        request.form.get('name'), request.form.get('email'),
        request.form.get('phone'), request.form.get('expertise'),
        request.form.get('experience'), request.form.get('password')
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO guides (name, email, phone, expertise, experience, password) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))
@app.route('/')
def index():
    return render_template('main.html')

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

@app.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id', 1)
    full_name = request.form.get('name')
    student_id = request.form.get('student_id')
    email = request.form.get('email')
    dept = request.form.get('dept')
    db = get_db_connection()
    cursor = db.cursor()
    sql = "UPDATE users SET full_name=%s, student_id=%s, email=%s, department=%s WHERE id=%s"
    cursor.execute(sql, (full_name, student_id, email, dept, user_id))
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            img_binary = file.read()
            cursor.execute("UPDATE users SET profile_pic=%s WHERE id=%s", (img_binary, user_id))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"status": "success"})

@app.route('/remove_profile_pic', methods=['POST'])
def remove_pic():
    user_id = session.get('user_id', 1)
    db = get_db_connection()
    cursor = db.cursor()
   
    cursor.execute("UPDATE users SET profile_pic = NULL WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)