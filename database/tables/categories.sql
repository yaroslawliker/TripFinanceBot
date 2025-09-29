CREATE TABLE categories {
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    budget REAL DEFAULT 0,
    start_datetime TEXT,
    end_datetime TEXT,
    FOREIGN KEY(user_id) REFERENCES users(chat_id) NOT NULL
}