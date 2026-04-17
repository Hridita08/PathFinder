import mysql.connector

# 1️⃣ Connect once
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="pathfinder_db"
)

cursor = conn.cursor()

print("✅ Database connected successfully!")

# 2️⃣ Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    email VARCHAR(100)
)
""")

conn.commit()
print("✅ Table 'students' created successfully!")

# 3️⃣ Show tables
cursor.execute("SHOW TABLES;")

print("\n📌 Tables in database:")
for table in cursor.fetchall():
    print(table)

# 4️⃣ Insert test data (optional)
cursor.execute("""
INSERT INTO students (name, age, email)
VALUES ('Toumi', 20, 'toumi@gmail.com')
""")

conn.commit()
print("✅ Sample data inserted!")

# 5️⃣ Show data
cursor.execute("SELECT * FROM students")

print("\n📌 Students data:")
for row in cursor.fetchall():
    print(row)