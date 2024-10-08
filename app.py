from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the reviews table
def create_reviews_table():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# Home route (display reviews)
@app.route('/')
def index():
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews').fetchall()
    conn.close()
    return render_template('index.html', reviews=reviews)

# Add review route
@app.route('/add', methods=('GET', 'POST'))
def add_review():
    if request.method == 'POST':
        review = request.form['review']
        conn = get_db_connection()
        conn.execute('INSERT INTO reviews (content) VALUES (?)', (review,))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

if __name__ == '__main__':
    create_reviews_table()
    app.run(debug=True)
