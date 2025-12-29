import hashlib
import os
import getpass


PIN_FILE = "data/pin.hash"


class PinAuth:
    def __init__(self):
        os.makedirs("data", exist_ok=True)

        
        if not os.path.exists(PIN_FILE):
            self._setup_pin()

    def _setup_pin(self):
        print("No PIN found. Please set a new PIN.")
        pin = getpass.getpass("Set PIN: ")
        confirm = getpass.getpass("Confirm PIN: ")

        if pin != confirm:
            raise ValueError("PINs do not match.")

        hashed = self._hash_pin(pin)
        with open(PIN_FILE, "w") as f:
            f.write(hashed)

        print("PIN set successfully.")

    def _hash_pin(self, pin: str) -> str:
        return hashlib.sha256(pin.encode()).hexdigest()

    def verify(self) -> bool:
        entered = getpass.getpass("Enter PIN: ")
        hashed = self._hash_pin(entered)

        with open(PIN_FILE, "r") as f:
            stored = f.read().strip()

        return hashed == stored
    
    def reset_pin(self):
        if os.path.exists(PIN_FILE):
            os.remove(PIN_FILE)
            print("Old PIN removed.")
        self._setup_pin()

