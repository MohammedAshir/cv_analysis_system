import sqlite3

# Connect to the database
conn = sqlite3.connect("cv_analysis.db")
cursor = conn.cursor()

# Delete duplicate candidates (keep only one per email)
cursor.execute("""
DELETE FROM candidates 
WHERE rowid NOT IN (
    SELECT MIN(rowid) FROM candidates GROUP BY email
);
""")

conn.commit()
conn.close()

print("Duplicate records deleted successfully.")
