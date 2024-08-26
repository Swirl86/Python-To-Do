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

    # Register the teardown function
    app.teardown_appcontext(db.close_connection)

    return app
