CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    money REAL DEFAULT 0.0,
    datetime TEXT,
    purpose TEXT,
    FOREIGN KEY(category_id) REFERENCES categories(id)
)