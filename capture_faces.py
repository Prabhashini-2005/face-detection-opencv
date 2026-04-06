import cv2
import os

# Your name (folder name)
person_name = "Prabhashini"

# Paths
base_dir = r"C:\FaceSimple"

dataset_dir = os.path.join(base_dir, "dataset", person_name)

os.makedirs(dataset_dir, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

print("Capturing faces for", person_name)
print("Press Q to stop early.")

count = 0
max_images = 50  # how many images to save

while True:
    ret, img = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # draw box
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

        # crop face region
        face_roi = gray[y:y+h, x:x+w]

        # save face image
        img_name = os.path.join(dataset_dir, f"{person_name}_{count}.jpg")
        cv2.imwrite(img_name, face_roi)
        count += 1
        print("Saved:", img_name)

        if count >= max_images:
            break

    cv2.imshow("Capturing Faces - " + person_name, img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if count >= max_images:
        break

cap.release()
cv2.destroyAllWindows()
print("Done! Total images saved:", count)
