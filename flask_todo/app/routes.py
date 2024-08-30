from flask import Blueprint, render_template, request, redirect, url_for
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    db_connection = db.get_db()
    todos = db_connection.execute('SELECT * FROM todos').fetchall()
    subtasks = db_connection.execute('SELECT * FROM subtasks').fetchall()

    todos_with_subtasks = []
    for todo in todos:
        todo_dict = dict(todo)
        todo_dict['subtasks'] = [dict(subtask) for subtask in subtasks if subtask['todo_id'] == todo['id']]
        todos_with_subtasks.append(todo_dict)

    return render_template('index.html', todos=todos_with_subtasks)


@bp.route('/add', methods=['POST'])
def add():
    task = request.form.get('todo')
    description = request.form.get('description', '')
    subtasks = request.form.getlist('subtask')  # Get all subtasks from the form

    db_connection = db.get_db()
    # Insert the main todo
    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO todos (task, description, completed) VALUES (?, ?, ?)', [task, description, 0])
    todo_id = cursor.lastrowid

    # Insert subtasks
    for subtask in subtasks:
        if subtask:  # Avoid inserting empty subtasks
            cursor.execute('INSERT INTO subtasks (todo_id, task, completed) VALUES (?, ?, ?)', [todo_id, subtask, 0])

    db_connection.commit()
    return redirect(url_for('main.index'))


@bp.route('/add_subtask', methods=['POST'])
def add_subtask():
    title = request.form.get('subtask_title')
    todo_id = request.form.get('todo_id')

    if not title or not todo_id:
        return redirect(url_for('main.index'))

    db_connection = db.get_db()
    db_connection.execute('INSERT INTO subtasks (todo_id, task) VALUES (?, ?)', [todo_id, title])
    db_connection.commit()

    return redirect(url_for('main.index'))


@bp.route('/edit/<int:todo_id>', methods=['POST'])
def edit(todo_id):
    new_task = request.form.get('task_title', '').strip()
    new_description = request.form.get('task_description', '').strip()

    if new_task:
        db_connection = db.get_db()
        db_connection.execute(
            'UPDATE todos SET task = ?, description = ? WHERE id = ?',
            [new_task, new_description, todo_id]
        )
        db_connection.commit()

    return redirect(url_for('main.index'))


@bp.route('/delete_subtask/<int:subtask_id>')
def delete_subtask(subtask_id):
    db_connection = db.get_db()
    db_connection.execute('DELETE FROM subtasks WHERE id = ?', [subtask_id])
    db_connection.commit()
    return redirect(url_for('main.index'))


@bp.route('/delete_todo/<int:todo_id>')
def delete_todo(todo_id):
    db_connection = db.get_db()
    db_connection.execute('DELETE FROM subtasks WHERE todo_id = ?', [todo_id])
    db_connection.execute('DELETE FROM todos WHERE id = ?', [todo_id])
    db_connection.commit()
    return redirect(url_for('main.index'))


@bp.route('/toggle_todo/<int:todo_id>')
def toggle_todo(todo_id):
    db_connection = db.get_db()
    todo = db_connection.execute('SELECT * FROM todos WHERE id = ?', [todo_id]).fetchone()
    if todo:
        new_completed_status = 0 if todo['completed'] else 1
        db_connection.execute('UPDATE todos SET completed = ? WHERE id = ?', [new_completed_status, todo_id])
        db_connection.commit()

    return redirect(url_for('main.index'))


@bp.route('/toggle_subtask/<int:subtask_id>')
def toggle_subtask(subtask_id):
    db_connection = db.get_db()
    subtask = db_connection.execute('SELECT * FROM subtasks WHERE id = ?', [subtask_id]).fetchone()

    if subtask:
        # Calculate new completed status
        new_completed_status = 0 if subtask['completed'] else 1

        # Update the subtask item
        db_connection.execute('UPDATE subtasks SET completed = ? WHERE id = ?', [new_completed_status, subtask_id])
        db_connection.commit()

        # Check if all subtasks are completed
        todo_id = subtask['todo_id']
        all_subtasks = db_connection.execute('SELECT * FROM subtasks WHERE todo_id = ?', [todo_id]).fetchall()

        if all(subtask['completed'] for subtask in all_subtasks):
            db_connection.execute('UPDATE todos SET completed = ? WHERE id = ?', [1, todo_id])
        else:
            db_connection.execute('UPDATE todos SET completed = ? WHERE id = ?', [0, todo_id])

        db_connection.commit()

    return redirect(url_for('main.index'))
