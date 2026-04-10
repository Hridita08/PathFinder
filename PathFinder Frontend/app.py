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
    from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''   # jodi password thake, ekhane dao
app.config['MYSQL_DB'] = 'pathfinder'

mysql = MySQL(app)

@app.route('/')
def home():
    return "Connected successfully!"

if __name__ == '__main__':
    app.run(debug=True)