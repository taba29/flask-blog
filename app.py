from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DB初期化
def init_db():
    with sqlite3.connect('blog.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')

@app.route('/')
def index():
    with sqlite3.connect('blog.db') as conn:
        posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with sqlite3.connect('blog.db') as conn:
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        return redirect('/')
    return render_template('post.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
