from face_auth import FaceAuth

auth = FaceAuth()
result = auth.verify()

print("AUTH RESULT:", result)
