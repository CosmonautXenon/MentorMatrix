from cs50 import SQL

# Declare db without setting it to None
db = SQL("sqlite:///dev.db")

def init_db():
    """
    Initializes the database by creating necessary tables.
    """
    global db  # Declare db as global to modify the global object


    # Create the necessary tables
    db.execute('''CREATE TABLE IF NOT EXISTS transcripts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')

    db.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transcript_id INTEGER,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE);''')

    db.execute('''CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transcript_id INTEGER NOT NULL,
                    file_type TEXT CHECK(file_type IN ('audio', 'youtube', 'pdf')) NOT NULL,
                    name TEXT NOT NULL,
                    metadata TEXT,  -- JSON or additional metadata
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE);''')
    
    db.execute('''CREATE TABLE IF NOT EXISTS quizzes (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               note_id INTEGER NOT NULL,
               FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE);''')

    # Create indexes for faster lookups
    db.execute('CREATE INDEX IF NOT EXISTS idx_transcript_id ON notes (transcript_id);')
    db.execute('CREATE INDEX IF NOT EXISTS idx_file_transcript_id ON files (transcript_id);')
