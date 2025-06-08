DROP TABLE IF EXISTS attempts;
DROP TABLE IF EXISTS question_progress;

CREATE TABLE attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL, -- Corresponds to the ID in quiz_data.json
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_answer TEXT, -- The option selected by the user
    is_correct BOOLEAN NOT NULL CHECK (is_correct IN (0, 1)), -- 1 for correct, 0 for incorrect
    quiz_mode TEXT, -- e.g., 'practice', 'timed', 'topic'
    topic TEXT, -- The topic of the question at the time of attempt
    FOREIGN KEY (question_id) REFERENCES question_progress (question_id) -- Link to progress table (optional, for integrity)
);

CREATE TABLE question_progress (
    question_id TEXT PRIMARY KEY, -- Corresponds to the ID in quiz_data.json
    correct_attempts INTEGER NOT NULL DEFAULT 0,
    incorrect_attempts INTEGER NOT NULL DEFAULT 0,
    streak INTEGER NOT NULL DEFAULT 0, -- Consecutive correct answers
    next_review DATETIME, -- For spaced repetition
    last_attempt DATETIME -- Timestamp of the most recent attempt
);
