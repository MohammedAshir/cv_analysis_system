import sqlite3
import json

# Database file name
DB_NAME = "cv_analysis.db"

def get_db_connection():
    """Establish and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Enables dict-like row access
    return conn

def create_tables():
    """Create necessary tables in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table for storing extracted CV data
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        skills TEXT,
        education TEXT,
        experience TEXT,
        original_text TEXT
    )
    """)

    # Table for storing LLM analysis results
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cv_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER NOT NULL,
        summary TEXT,
        python_dev_fit TEXT,
        missing_details TEXT,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()


def store_candidate(structured_data, raw_text):
    """Insert extracted CV data into the database if not already present."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if the candidate already exists (based on email)
    cursor.execute("SELECT id FROM candidates WHERE email = ?", (structured_data.get("email"),))
    existing_candidate = cursor.fetchone()

    if existing_candidate:
        conn.close()
        return existing_candidate[0]  # Return existing candidate ID

    # If candidate does not exist, insert new record
    cursor.execute("""
    INSERT INTO candidates (name, email, phone, skills, education, experience, original_text) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        structured_data.get("name"),
        structured_data.get("email"),
        structured_data.get("phone"),
        json.dumps(structured_data.get("skills", [])),  
        json.dumps(structured_data.get("education", "")),
        json.dumps(structured_data.get("experience", "")), 
        raw_text
    ))

    candidate_id = cursor.lastrowid  
    conn.commit()
    conn.close()
    return candidate_id



def store_analysis(candidate_id, analysis):
    """Insert LLM analysis into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO cv_analysis (candidate_id, summary, python_dev_fit, missing_details) 
    VALUES (?, ?, ?, ?)
    """, (
        candidate_id,
        analysis.get("summary", ""),
        analysis.get("python_dev_fit", ""),
        json.dumps(analysis.get("missing_details", []))  # Store missing details as JSON
    ))

    conn.commit()
    conn.close()


def get_all_candidates():
    """Fetch all candidates for selection dropdown."""
    conn = get_db_connection()
    candidates = conn.execute('SELECT id, name FROM candidates').fetchall()
    conn.close()
    
    return [dict(candidate) for candidate in candidates]  # Convert rows to dict


def get_candidate_data(candidate_id):
    """Fetch structured candidate data from the database."""
    conn = get_db_connection()
    candidate = conn.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,)).fetchone()
    conn.close()
    
    return dict(candidate) if candidate else None


def get_candidate_analysis(candidate_id):
    """Fetch LLM analysis results for a given candidate."""
    conn = get_db_connection()
    analysis = conn.execute('SELECT * FROM cv_analysis WHERE candidate_id = ?', (candidate_id,)).fetchone()
    conn.close()
    
    return dict(analysis) if analysis else None


def delete_candidate(candidate_id):
    """Delete a candidate and their analysis from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM candidates WHERE id = ?', (candidate_id,))
    cursor.execute('DELETE FROM cv_analysis WHERE candidate_id = ?', (candidate_id,))

    conn.commit()
    conn.close()
