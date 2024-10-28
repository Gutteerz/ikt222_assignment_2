from flask import Flask, render_template, request, redirect
import sqlite3
import bleach

app = Flask(__name__)

# Database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Lage 'Reviews' table
def create_reviews_table():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            );
        ''')
        conn.commit()

# Home
@app.route('/')
def index():
    with get_db_connection() as conn:
        reviews = conn.execute('SELECT * FROM reviews').fetchall()
    return render_template('index.html', reviews=reviews)

# Home Safe
@app.route('/safe')
def index_safe():
    with get_db_connection() as conn:
        reviews = conn.execute('SELECT * FROM reviews').fetchall()
    return render_template('index_safe.html', reviews=reviews)

# Add Review
@app.route('/add', methods=('GET', 'POST'))
def add_review():
    if request.method == 'POST':
        review = request.form['review']
        bleachedReview = bleach.clean(review)
        with get_db_connection() as conn:
            conn.execute('INSERT INTO reviews (content) VALUES (?)', (bleachedReview,))
            conn.commit()
        return redirect('/')
    return render_template('add.html')

if __name__ == '__main__':
    create_reviews_table()
    app.run(debug=True)
