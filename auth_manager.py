from .face_auth import FaceAuth
from .pin_auth import PinAuth


class AuthManager:
    def authenticate(self) -> bool:
        print("\n=== Nova Authentication ===")
        print("1. Face Authentication")
        print("2. PIN Authentication")
        print("3. Reset Face")
        print("4. Reset PIN")

        choice = input("Choose option (1/2/3/4): ").strip()

    
        if choice == "1":
            try:
                face_auth = FaceAuth()
                return face_auth.verify()
            except Exception as e:
                print("Face authentication failed:", e)
                return False

        elif choice == "2":
            pin_auth = PinAuth()
            return pin_auth.verify()

        elif choice == "3":
            print("\n⚠️ Reset Face requires PIN verification")
            pin_auth = PinAuth()

            if pin_auth.verify():
                try:
                    face_auth = FaceAuth()
                    face_auth.reset_face()
                    print("\nFace data reset successfully.")
                    print("Please re-enroll your face by running:")
                    print("python security/face_enroll.py")
                except Exception as e:
                    print("Error resetting face:", e)
            else:
                print("PIN verification failed.")

            return False

        elif choice == "4":
            print("\n Reset PIN requires FACE verification")
            try:
                face_auth = FaceAuth()
                if face_auth.verify():
                    pin_auth = PinAuth()
                    pin_auth.reset_pin()
                    print("\nPIN reset successfully.")
                else:
                    print("Face verification failed.")
            except Exception as e:
                print("Error during PIN reset:", e)

            return False

        else:
            print("Invalid choice.")
            return False
