# Python-To-Do

A simple to-do list application built with Flask. This project demonstrates basic CRUD operations and file handling in a Flask web application.

## Features

- **Add New Todos**: Create new tasks with optional descriptions and subtasks.
- **Edit Todos**: Modify existing tasks and their descriptions.
- **Delete Todos**: Remove tasks and their associated subtasks.
- **Mark as Completed**: Toggle the completion status of tasks and subtasks.
- **Subtasks Management**: Add, edit, and delete subtasks for each main task.
- **Data Persistence**: Seed database from a text file if empty, ensuring initial data is available.

## Technologies Used

- **Flask**: Web framework for building the web application.
- **SQLite**: Lightweight database used for storing to-do items and subtasks.
- **HTML/CSS**: Frontend technologies for designing the user interface.
- **Bootstrap**: CSS framework for styling and layout.
- **JavaScript**: For interactive frontend behavior.

## File Structure

- **`app/`**: Contains application source code.
  - **`__init__.py`**: Initializes the Flask application and sets up the database.
  - **`routes.py`**: Contains route definitions and business logic.
  - **`db.py`**: Handles database interactions.
  - **`dummy_values.txt`**: Sample data used for seeding the database.
- **`instance/`**: Contains instance-specific files like the SQLite database and dummy data file.
- **`requirements.txt`**: Lists project dependencies.

## Database Seeding

If the database is empty upon initialization, it will be seeded with data from `dummy_values.txt`. This file contains sample to-dos and subtasks to populate the database.

## Run the Application

### Create a Virtual Environment:

```bash
python -m venv venv
```

### Activate the Virtual Environment:

  - On Windows:
    ```bash
    venv\Scripts\activate
    ```
  
  - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

### Install Dependencies:

```bash
pip install -r requirements.txt
```

### To start the application, use the following command:

```bash
flask run
```
*By default, the application will be available at http://127.0.0.1:5000/.*
