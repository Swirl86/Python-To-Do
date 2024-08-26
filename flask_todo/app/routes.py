from flask import Blueprint, render_template, request, redirect, url_for
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    todos = db.get_db().execute('SELECT * FROM todos').fetchall()
    return render_template('index.html', todos=todos)

@bp.route('/add', methods=['POST'])
def add():
    task = request.form.get('todo', '').strip()
    if task:
        db.get_db().execute('INSERT INTO todos (task, completed) VALUES (?, ?)', [task, 0])
        db.get_db().commit()
    return redirect(url_for('main.index'))

@bp.route('/edit/<int:todo_id>', methods=['POST'])
def edit(todo_id):
    new_task = request.form.get('task_title', '').strip()
    if new_task:
        db.get_db().execute('UPDATE todos SET task = ? WHERE id = ?', [new_task, todo_id])
        db.get_db().commit()
    return redirect(url_for('main.index'))

@bp.route('/delete/<int:todo_id>')
def delete(todo_id):
    db.get_db().execute('DELETE FROM todos WHERE id = ?', [todo_id])
    db.get_db().commit()
    return redirect(url_for('main.index'))

@bp.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    todo = db.get_db().execute('SELECT * FROM todos WHERE id = ?', [todo_id]).fetchone()
    if todo:
        new_completed_status = 0 if todo['completed'] else 1
        db.get_db().execute('UPDATE todos SET completed = ? WHERE id = ?', [new_completed_status, todo_id])
        db.get_db().commit()
    return redirect(url_for('main.index'))
