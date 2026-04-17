import mysql.connector

# 1️⃣ Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="pathfinder_db"
)

cursor = conn.cursor()

print("✅ Connected to database")

# -------------------------
# 2️⃣ Register function
# -------------------------
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        print("✅ Registration successful!")
    except:
        print("❌ Username already exists!")

# -------------------------
# 3️⃣ Login function
# -------------------------
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        print("🎉 Login successful! Welcome", username)
    else:
        print("❌ Invalid username or password")

# -------------------------
# 4️⃣ Menu system
# -------------------------
while True:
    print("\n===== LOGIN SYSTEM =====")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        print("👋 Bye!")
        break
    else:
        print("❌ Invalid choice")