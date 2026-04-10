import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#Project18#",
    database="Pathfinderdb"
)

print("Connected successfully!")