from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
DB_NAME = "notes.db"

# Базаны жасау
def init_db():
    if not os.path.exists(DB_NAME):
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )""")
            c.execute("""CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                content TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )""")
            conn.commit()

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/notes')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                return redirect('/login')
            except:
                return render_template('register.html', error="Username already exists.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user[0]
                return redirect('/notes')
            else:
                return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/notes')
def notes():
    if 'user_id' not in session:
        return redirect('/login')
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, title, content FROM notes WHERE user_id=?", (session['user_id'],))
        user_notes = c.fetchall()
    return render_template('notes.html', notes=user_notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)",
                      (session['user_id'], title, content))
            conn.commit()
        return redirect('/notes')
    return render_template('add_note.html')

@app.route('/delete/<int:note_id>')
def delete(note_id):
    if 'user_id' not in session:
        return redirect('/login')
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM notes WHERE id=? AND user_id=?", (note_id, session['user_id']))
        conn.commit()
    return redirect('/notes')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
