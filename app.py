from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ----- DATABASE CONNECTION -----
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ----- HOME PAGE -----
@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

# ----- CONTACT FORM -----
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    subject = request.form['subject']
    message = request.form['message']

    conn = get_db_connection()
    conn.execute('INSERT INTO contact (name, email, phone, subject, message) VALUES (?, ?, ?, ?, ?)',
                 (name, email, phone, subject, message))
    conn.commit()
    conn.close()
    return redirect('/')

# ----- NEWSLETTER -----
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    conn = get_db_connection()
    conn.execute('INSERT INTO newsletter (email) VALUES (?)', (email,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
