import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#Project18#",
    database="Pathfinder"
)

print("Connected successfully!")

cursor = db.cursor()
cursor.execute("SELECT * FROM users")

for row in cursor:
    print(row)