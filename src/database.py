import sqlite3
import json

# Database file name
DB_NAME = "cv_analysis.db"

def create_tables():
    """Create necessary tables in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table for storing extracted CV data
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
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
        candidate_id INTEGER,
        summary TEXT,
        python_dev_fit TEXT,
        missing_details TEXT,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id)
    )
    """)

    conn.commit()
    conn.close()


def store_candidate(structured_data, raw_text):
    """Insert extracted CV data into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

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

    candidate_id = cursor.lastrowid  # Get the last inserted ID
    conn.commit()
    conn.close()
    return candidate_id


def store_analysis(candidate_id, analysis):
    """Insert LLM analysis into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO cv_analysis (candidate_id, summary, python_dev_fit, missing_details) 
    VALUES (?, ?, ?, ?)
    """, (
        candidate_id,
        analysis.get("summary"),
        analysis.get("python_dev_fit"),
        json.dumps(analysis.get("missing_details", []))  # Store missing details as JSON
    ))

    conn.commit()
    conn.close()

