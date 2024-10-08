CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS subtasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    todo_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)) DEFAULT 0,
    FOREIGN KEY (todo_id) REFERENCES todos(id)
);