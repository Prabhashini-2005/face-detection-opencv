import sqlite3
import os

base_dir = r"C:\FaceSimple"
db_path = os.path.join(base_dir, "attendance.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
SELECT students.name, attendance.date, attendance.status
FROM attendance
JOIN students ON attendance.student_id = students.student_id
ORDER BY attendance.date, students.name
""")
rows = cur.fetchall()
conn.close()

# Table header
print("+----------------+------------+---------+")
print("| Name           | Date       | Status  |")
print("+----------------+------------+---------+")

# Table rows
for name, date_val, status in rows:
    print(f"| {name:<14} | {date_val} | {status:<7} |")

print("+----------------+------------+---------+")




