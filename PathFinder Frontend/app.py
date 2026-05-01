from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
import base64

app = Flask(__name__, 
            template_folder=".", 
            static_folder=".", 
            static_url_path='')
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
# Main & Profile Routes
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

if __name__ == '__main__':
    app.run(debug=True)