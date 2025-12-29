import cv2
import os
import numpy as np

DATASET_DIR = "data/faces"
MODEL_PATH = "data/face_model.yml"


def enroll_face(user_id=1, samples=20):
    os.makedirs(DATASET_DIR, exist_ok=True)

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    count = 0
    print("Face enrollment started. Look at the camera.")

    while count < samples:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            filename = f"{DATASET_DIR}/{user_id}_{count}.jpg"
            cv2.imwrite(filename, face)
            count += 1
            print(f"Captured {count}/{samples}")

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Face Enrollment", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    print("Training model...")

    faces, labels = [], []
    for file in os.listdir(DATASET_DIR):
        img = cv2.imread(os.path.join(DATASET_DIR, file), cv2.IMREAD_GRAYSCALE)
        faces.append(img)
        labels.append(user_id)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    recognizer.save(MODEL_PATH)

    print("Face enrollment completed successfully.")


if __name__ == "__main__":
    enroll_face()
