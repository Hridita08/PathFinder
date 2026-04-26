from flask import Flask, render_template, request
import mysql.connector
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=current_dir,
            static_folder=current_dir,
            static_url_path='')

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#Project18#",
        database="pathfinderdb"
    )

@app.route('/')
def home():
    return render_template('search.html')


@app.route('/search')
def search():
    query = request.args.get('query')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT * FROM guides
    WHERE name LIKE %s OR sector LIKE %s
    """

    search_term = f"%{query}%"
    cursor.execute(sql, (search_term, search_term))

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('search-result.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True, port=5002)