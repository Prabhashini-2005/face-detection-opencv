import sqlite3
import os

base_dir = r"C:\FaceSimple"
db_path = os.path.join(base_dir, "attendance.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Table of students (id from labels, name)
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")

# Table of attendance records
cur.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    UNIQUE(student_id, date),
    FOREIGN KEY(student_id) REFERENCES students(student_id)
)
""")

conn.commit()
conn.close()

print("Database and tables created at:", db_path)



