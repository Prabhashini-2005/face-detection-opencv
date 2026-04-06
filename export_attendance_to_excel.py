import sqlite3
import pandas as pd

db_path = r"C:\FaceSimple\attendance.db"
output_path = r"C:\FaceSimple\attendance_with_absent.xlsx"

conn = sqlite3.connect(db_path)

# Get all dates where attendance was taken
dates_df = pd.read_sql_query("SELECT DISTINCT date FROM attendance ORDER BY date;", conn)

# Get your single student
student_df = pd.read_sql_query("SELECT student_id, name FROM students;", conn)
student = student_df.iloc[0]  # only one student

rows = []
for d in dates_df["date"]:
    q = "SELECT COUNT(*) AS c FROM attendance WHERE student_id=? AND date=? AND status='Present';"
    present_df = pd.read_sql_query(q, conn, params=(student["student_id"], d))
    is_present = present_df["c"].iloc[0] > 0
    rows.append({
        "Name": student["name"],
        "RollNumber": "239x1a3281",
        "Date": d,
        "Status": "Present" if is_present else "Absent"
    })

conn.close()

result_df = pd.DataFrame(rows)
result_df.to_excel(output_path, index=False)

print("Exported to:", output_path)
