import cv2
import os


MODEL_PATH = "data/face_model.yml"


class FaceAuth:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Face model not found. Please enroll first.")

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(MODEL_PATH)

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def reset_face(self):
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
            print("Face model deleted.")
        else:
            print("No face model found.")

        print("Please re-enroll your face.")


    def verify(self, timeout=8):
        """
        Returns True if face is verified within timeout seconds.
        """
        cap = cv2.VideoCapture(0)

        print("Face verification started. Look at the camera.")

        verified = False
        start_time = cv2.getTickCount()
        freq = cv2.getTickFrequency()

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))

                label, confidence = self.recognizer.predict(face)

                
                if confidence < 60:
                    verified = True
                    break

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            cv2.imshow("Face Verification", frame)

            elapsed = (cv2.getTickCount() - start_time) / freq
            if verified or elapsed > timeout:
                break

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

        return verified
