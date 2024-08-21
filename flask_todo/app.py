# -*- coding: utf-8 -*-

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)

app.config['DATABASE'] = os.path.join(app.instance_path, 'todo.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

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
    cur = db.execute('SELECT id, task FROM todos')
    todos = cur.fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('todo')
    if task:
        db = get_db()
        db.execute('INSERT INTO todos (task) VALUES (?)', [task])
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
