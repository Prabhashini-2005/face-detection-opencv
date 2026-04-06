import sqlite3
import os

base_dir = r"C:\FaceSimple"
db_path = os.path.join(base_dir, "attendance.db")
labels_txt = os.path.join(base_dir, "labels.txt")

# Read labels.txt: format "id:name"
label_map = {}
with open(labels_txt, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(":", 1)
        if len(parts) != 2:
            continue
        label_id = int(parts[0])
        name = parts[1]
        label_map[label_id] = name

conn = sqlite3.connect(db_path)
cur = conn.cursor()

for student_id, name in label_map.items():
    cur.execute("""
        INSERT OR IGNORE INTO students (student_id, name)
        VALUES (?, ?)
    """, (student_id, name))

conn.commit()

# Show all students
cur.execute("SELECT student_id, name FROM students")
rows = cur.fetchall()
conn.close()

print("Students in database:")
for r in rows:
    print(r[0], "-", r[1])




