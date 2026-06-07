CREATE TABLE IF NOT EXISTS ActivityLog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    gesture TEXT,
    action TEXT,
    status TEXT
);
