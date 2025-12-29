from security.auth_manager import AuthManager


auth = AuthManager()
result = auth.authenticate()

print("\nFINAL AUTH RESULT:", result)
