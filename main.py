import sys
from PyQt5.QtWidgets import QApplication

from ui.main_window import NovaWindow
from security.auth_manager import AuthManager


def main():
    auth = AuthManager()
    authenticated = auth.authenticate()

    if not authenticated:
        print("Authentication failed. Exiting Nova.")
        sys.exit(0)

    app = QApplication(sys.argv)
    window = NovaWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
