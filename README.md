# face-attendance-system
Face recognition based attendance system using Python and OpenCV.
# Face Recognition Attendance System (OpenCV)

This project is a simple face recognition–based attendance system built with Python and OpenCV. It captures face images, trains a recognition model, recognizes faces in real time, and marks attendance into a database and Excel sheets.[web:279][web:283]

## Features

- Capture face images for each student and store them in a dataset folder.
- Train a face recognition model using the captured images.
- Recognize faces in real time using a webcam.
- Mark attendance automatically for recognized students.
- Export attendance records to Excel files for reporting.[web:279][web:283]

## Project Structure

Inside the project folder you will see files like:

- `dataset/` – Contains subfolders with images for each person (for example `dataset/Prabhashini/Prabhashini_0.jpg`, etc.). These are used to train the model.[web:283]
- `add_students_from_labels.py` – Adds student details from the labels file into the system.
- `attendance.db` – SQLite database file that stores attendance records.
- `attendance_export.xlsx` – Excel file containing exported attendance.
- `attendance_setup.py` – Script to create/initialize tables or basic attendance structure.
- `attendance_with_absent.xlsx` – Excel file that includes both present and absent information.
- `capture_faces.py` – Opens webcam and captures multiple images of a student, saving them into `dataset/`.
- `export_attendance_to_excel.py` – Exports attendance from the database to an Excel file.
- `export_with_absent.py` – Exports attendance with absent students included.
- `labels.txt` – Stores the mapping between numeric labels and student names or IDs.
- `recognize.py` – Main script that runs face recognition using the trained model and marks attendance.
- `train_model.py` – Trains the face recognition model on images inside `dataset/` and saves the model.
- `trainer.yml` – Saved trained model file created by `train_model.py`.
- `view_attendance.py` – Script to view attendance records (for example from the database or Excel).[web:279][web:283]

## How It Works

1. **Capture Faces**  
   Run `capture_faces.py` to open the webcam and capture multiple images of each student. The images are stored in `dataset/<student_name>/` and used for training the model.[web:279][web:283]

2. **Train the Model**  
   Run `train_model.py` to read images from `dataset/`, extract features, and train a face recognizer (for example LBPH). The trained model is saved to `trainer.yml` for later use.[web:279][web:283]

3. **Recognize and Mark Attendance**  
   Run `recognize.py` to start real-time recognition. The script uses the webcam, loads `trainer.yml`, identifies faces, and records attendance into `attendance.db` and related Excel files.[web:279][web:283]

4. **View and Export Attendance**  
   - Use `view_attendance.py` to view stored attendance.
   - Use `export_attendance_to_excel.py` and `export_with_absent.py` to generate Excel reports like `attendance_export.xlsx` and `attendance_with_absent.xlsx`.[web:279][web:283]

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/Prabhashini-2005/face-detection-opencv.git
   cd face-detection-opencv
   ```

2. **Create virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   venv\Scripts\activate   # on Windows
   ```

3. **Install dependencies**

   Install OpenCV and other required libraries (for example):

   ```bash
   pip install opencv-python numpy pandas
   ```

   Add any other libraries you used (for example sqlite3 is built-in).[web:301][web:303]

4. **Run the scripts in order**

   - First, run `capture_faces.py` for each new student.
   - Then, run `train_model.py` to update the face recognition model.
   - Finally, run `recognize.py` to recognize faces and mark attendance.[web:279][web:283]

## Future Improvements

- Replace basic face recognition with more advanced deep learning–based models.
- Add a GUI or web interface (using Tkinter or Flask) to make it easier for non-technical users.
- Add user authentication and role-based access for administrators and teachers.[web:261][web:285]

## Screenshots
 ```
![Capture faces - start](screenshots/capture_1.png)
![Capture faces - more samples](screenshots/capture_2.png)
![Training face recognition model](screenshots/train.png)
![Recognize face and mark attendance](screenshots/recognize.png)
![Export attendance to Excel](screenshots/export.png)
![Attendance Excel report](screenshots/attendance_excel.png)
