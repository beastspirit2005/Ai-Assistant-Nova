from pin_auth import PinAuth

auth = PinAuth()
result = auth.verify()

print("PIN AUTH RESULT:", result)
