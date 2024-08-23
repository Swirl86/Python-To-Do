# -*- coding: utf-8 -*-

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)

app.config['DATABASE'] = os.path.join(app.instance_path, 'todo.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'instance/todo.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT id, task, created_at, completed FROM todos')
    todos = cur.fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('todo')
    created_at = request.form.get('created_at', None)
    completed = 0

    if task:
        db = get_db()
        if created_at:
            db.execute('INSERT INTO todos (task, created_at, completed) VALUES (?, ?, ?)', [task, created_at, completed])
        else:
            db.execute('INSERT INTO todos (task, completed) VALUES (?, ?)', [task, completed])
        db.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit(todo_id):
    new_task_title = request.form['task_title']
    db = get_db()
    db.execute('UPDATE todos SET task = ? WHERE id = ?', [new_task_title, todo_id])
    db.commit()
    return redirect(url_for('index'))


@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    db = get_db()
    cur = db.execute('SELECT completed FROM todos WHERE id = ?', [todo_id])
    todo = cur.fetchone()

    if todo:
        new_status = not todo['completed']
        db.execute('UPDATE todos SET completed = ? WHERE id = ?', [new_status, todo_id])
        db.commit()

    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    db = get_db()
    db.execute('DELETE FROM todos WHERE id = ?', [todo_id])
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True)
    init_db()
    app.run(debug=True)
