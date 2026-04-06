import cv2
import os
import sqlite3
from datetime import date
import pandas as pd  # for Excel export

base_dir = r"C:\FaceSimple"
trainer_path = os.path.join(base_dir, "trainer.yml")
labels_txt = os.path.join(base_dir, "labels.txt")
db_path = os.path.join(base_dir, "attendance.db")
excel_path = os.path.join(base_dir, "attendance_with_absent.xlsx")

# Load label map from labels.txt
def load_labels(labels_txt):
    label_map = {}
    if not os.path.exists(labels_txt):
        print("labels.txt not found:", labels_txt)
        return label_map
    with open(labels_txt, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # format: id:name
            parts = line.split(":", 1)
            if len(parts) != 2:
                continue
            label_id = int(parts[0])
            name = parts[1]
            label_map[label_id] = name
    return label_map

label_map = load_labels(labels_txt)
print("Loaded labels:", label_map)

# Connect to database
def get_db_connection():
    conn = sqlite3.connect(db_path)
    return conn

# Mark attendance once per day for a student_id
def mark_attendance(student_id):
    today = date.today().isoformat()  # 'YYYY-MM-DD'
    conn = get_db_connection()
    cur = conn.cursor()

    # Insert only if not already present for today
    cur.execute("""
        INSERT OR IGNORE INTO attendance (student_id, date, status)
        VALUES (?, ?, 'Present')
    """, (student_id, today))

    conn.commit()
    conn.close()

# Export Name, RollNumber, Date, Present/Absent to Excel
def export_with_absent():
    conn = get_db_connection()

    # All distinct dates in attendance
    dates_df = pd.read_sql_query(
        "SELECT DISTINCT date FROM attendance ORDER BY date;", conn
    )

    # All students (you currently have one, but this supports more)
    students_df = pd.read_sql_query(
        "SELECT student_id, name FROM students;", conn
    )

    rows = []
    for _, student in students_df.iterrows():
        for d in dates_df["date"]:
            q = """
            SELECT COUNT(*) AS c
            FROM attendance
            WHERE student_id = ? AND date = ? AND status = 'Present';
            """
            present_df = pd.read_sql_query(
                q, conn, params=(student["student_id"], d)
            )
            is_present = present_df["c"].iloc[0] > 0
            rows.append({
                "Name": student["name"],
                "RollNumber": "239x1a3281",  # your roll number format
                "Date": d,
                "Status": "Present" if is_present else "Absent",
            })

    conn.close()

    result_df = pd.DataFrame(rows)
    result_df.to_excel(excel_path, index=False)
    print("Exported attendance to:", excel_path)

# Keep track of which IDs have already been marked today
marked_today = set()

# Create recognizer and load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(trainer_path)

# Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

print("Starting recognition. Press 'q' to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]

        # Recognize face
        label_id, confidence = recognizer.predict(face_roi)

        # Smaller confidence value = better match
        name = label_map.get(label_id, "Unknown")
        text = f"{name} ({confidence:.0f})"

        # Mark attendance if recognized and confident enough
        if name != "Unknown" and confidence < 80:
            if label_id not in marked_today:
                mark_attendance(label_id)
                marked_today.add(label_id)
                print(f"Marked attendance for ID {label_id} ({name})")

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

    cv2.imshow("Face Recognition - Attendance", frame)

    # Exit only when you press 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Recognition stopped.")

# Automatically export to Excel when you finish (after pressing 'q')
export_with_absent()

