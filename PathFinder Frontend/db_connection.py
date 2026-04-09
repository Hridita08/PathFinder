import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="pathfinder_db"
)

cursor = conn.cursor()
print("Database connected successfully!")
cursor.execute("SHOW TABLES;")
for table in cursor.fetchall():
    print(table)
    import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="pathfinder_db"
)
cursor = conn.cursor()

# Table create example
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    email VARCHAR(100)
)
""")
conn.commit()
print("Table 'students' created successfully!")
with open("pathfinderdb.session.sql", "w") as f:
    cursor.execute("SHOW TABLES;")
    for table in cursor.fetchall():
        f.write(str(table) + "\n")