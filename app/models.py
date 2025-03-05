from cs50 import SQL  # type: ignore

db = SQL("sqlite:///instance/dev.db")


def init_db():
    """
    Initializes the database by creating the necessary tables and indexes.

    This function sets up the following tables:
        - `users`: (Clerk-managed, unchanged)
        - `transcripts`, `notes`, `files`, `quizzes`, `quiz_questions`,
          `decks`, `flashcards`, `quiz_results`, and `podcasts` with UUID primary keys.
    """

    global db  # Declare db as global to modify the global object

    # The following tables use a default UUID (128-bit) generated by SQLite.
    # The expression lower(hex(randomblob(16))) generates a 32-character hex string.
    db.execute("""CREATE TABLE IF NOT EXISTS transcripts (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    transcript_id TEXT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    user_id TEXT NOT NULL DEFAULT '',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transcript_id TEXT NOT NULL,
                    file_type TEXT CHECK(file_type IN ('audio', 'youtube', 'pdf')) NOT NULL,
                    name TEXT NOT NULL,
                    metadata TEXT,
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE);""")

    db.execute("""CREATE TABLE IF NOT EXISTS quizzes (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    transcript_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS quiz_questions (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    quiz_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    question_type TEXT CHECK(question_type IN ('open_ended', 'multiple_choice')) NOT NULL,
                    options TEXT,  -- Store multiple-choice options as a JSON string
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS decks (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    title TEXT NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS flashcards (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    deck_id TEXT NOT NULL,
                    note_id TEXT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE,
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS quiz_results (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    quiz_id TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
                );""")

    db.execute("""CREATE TABLE IF NOT EXISTS podcasts (
                    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                    note_id TEXT,
                    content TEXT NOT NULL,
                    path TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                );""")

    # Create indexes for faster lookups
    db.execute("CREATE INDEX IF NOT EXISTS idx_transcript_id ON notes (transcript_id);")
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_file_transcript_id ON files (transcript_id);"
    )
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_quiz_transcript_id ON quizzes (transcript_id);"
    )
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_quiz_question_quiz_id ON quiz_questions (quiz_id);"
    )
    db.execute("CREATE INDEX IF NOT EXISTS idx_deck_title ON decks (title);")
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_flashcard_deck_id ON flashcards (deck_id);"
    )

    # Create index for faster user-based queries
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_notes_user_id ON notes (user_id);
    """)


if __name__ == "__main__":
    init_db()  # This is just a debugging step
