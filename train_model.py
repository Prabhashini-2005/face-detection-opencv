import os
import cv2
import numpy as np

# Paths
base_dir = r"C:\FaceSimple"
dataset_dir = os.path.join(base_dir, "dataset")
trainer_path = os.path.join(base_dir, "trainer.yml")

# Initialize face recognizer and face detector
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def get_images_and_labels(dataset_dir):
    faces = []
    labels = []
    label_map = {}
    current_label = 0

    # Loop over each person folder
    for person_name in os.listdir(dataset_dir):
        person_folder = os.path.join(dataset_dir, person_name)
        if not os.path.isdir(person_folder):
            continue

        # Give each person an integer label
        label_map[current_label] = person_name

        # Loop over each image
        for img_name in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_name)

            # Read image in grayscale
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            # Detect face (optional but safer)
            faces_rects = face_cascade.detectMultiScale(img, 1.3, 5)
            for (x, y, w, h) in faces_rects:
                face_roi = img[y:y+h, x:x+w]
                faces.append(face_roi)
                labels.append(current_label)
                break  # one face per image

        current_label += 1

    return faces, labels, label_map

print("Loading images and labels...")
faces, labels, label_map = get_images_and_labels(dataset_dir)

print("Total faces:", len(faces))
print("Total labels:", len(set(labels)))

if len(faces) == 0:
    print("No faces found for training. Check dataset path.")
    exit()

print("Training recognizer...")
recognizer.train(faces, np.array(labels))
recognizer.write(trainer_path)
print("Training complete. Model saved to:", trainer_path)

# Save label map for later (simple txt file)
labels_txt = os.path.join(base_dir, "labels.txt")
with open(labels_txt, "w", encoding="utf-8") as f:
    for label_id, name in label_map.items():
        f.write(f"{label_id}:{name}\n")

print("Labels saved to:", labels_txt)


