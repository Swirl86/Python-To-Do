import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load the config from the instance folder
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'todo.db'),
    )

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)

    # Initialize the database
    from . import db
    with app.app_context():
        db.init_db()
        seed_db_from_file()

    # Register the teardown function
    app.teardown_appcontext(db.close_connection)

    return app

def seed_db_from_file():
    db_connection = db.get_db()

    todos_exist = db_connection.execute('SELECT COUNT(*) FROM todos').fetchone()[0]

    if todos_exist == 0:  # If no todos exist, seed the database
        dummy_file_path = os.path.join(os.path.dirname(__file__), 'dummy_values.txt')

        # Check if file exist
        if not os.path.exists(dummy_file_path):
            print(f"File not found: {dummy_file_path}")
            return

        # Load todos from dummy_values.txt
        with open(dummy_file_path, 'r') as file:
            todos = eval(file.read())  # Note: eval is used here, but be cautious with its use

        for todo in todos:
            cursor = db_connection.cursor()
            cursor.execute('INSERT INTO todos (task, description, completed) VALUES (?, ?, ?)',
                           [todo['task'], todo['description'], todo['completed']])
            todo_id = cursor.lastrowid

            for subtask in todo['subtasks']:
                cursor.execute('INSERT INTO subtasks (todo_id, task, completed) VALUES (?, ?, ?)',
                               [todo_id, subtask['task'], subtask['completed']])

        db_connection.commit()
