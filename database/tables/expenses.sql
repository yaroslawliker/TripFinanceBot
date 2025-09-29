CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    money REAL DEFAULT 0.0,
    datetime TEXT,
    purpose TEXT,
    category_id INTEGER NOT NULL,
    FOREIGN KEY(category_id) REFERENCES categories(id)
)