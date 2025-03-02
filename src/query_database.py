import sqlite3
import json

DB_NAME = "cv_analysis.db"

def get_all_candidates():
    """Retrieve all stored candidates and their analysis."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT c.id, c.name, c.email, c.skills, c.education, c.experience, a.summary, a.python_dev_fit, a.missing_details
    FROM candidates c
    LEFT JOIN cv_analysis a ON c.id = a.candidate_id
    """)

    candidates = cursor.fetchall()
    conn.close()

    for candidate in candidates:
        print("\n🔹 Candidate Details:")
        print(f"ID: {candidate[0]}")
        print(f"Name: {candidate[1]}")
        print(f"Email: {candidate[2]}")
        print(f"Skills: {json.loads(candidate[3])}")  # ✅ Convert JSON back to list
        print(f"Education: {json.loads(candidate[4])}")  # ✅ Convert JSON back
        print(f"Experience: {json.loads(candidate[5])}")  # ✅ Convert JSON back
        print("\n🔹 LLM Analysis:")
        print(f"Summary: {candidate[6]}")
        print(f"Python Dev Fit: {candidate[7]}")
        print(f"Missing Details: {json.loads(candidate[8])}")  # ✅ Convert JSON back

get_all_candidates()
