CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    session_type TEXT NOT NULL CHECK(session_type IN ('Scan', 'Report', 'Notification', 'Mitigation')),
    context TEXT
);

CREATE TABLE IF NOT EXISTS input_data (
    id TEXT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    content TEXT NOT NULL,
    session_id TEXT NOT NULL,
    context TEXT,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);

CREATE TABLE IF NOT EXISTS feedback_data (
    id TEXT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    session_id TEXT NOT NULL,
    feedback TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);