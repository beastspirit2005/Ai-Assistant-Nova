from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QComboBox,
    QMessageBox
)


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Nova Settings")
        self.setFixedSize(360, 320)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)

        # =========================
        # VOICE SETTINGS
        # =========================
        voice_label = QLabel("Voice")
        voice_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(voice_label)

        self.auto_speak_checkbox = QCheckBox("Speak responses automatically")
        self.auto_speak_checkbox.setChecked(False)
        main_layout.addWidget(self.auto_speak_checkbox)

        # =========================
        # APPEARANCE SETTINGS
        # =========================
        appearance_label = QLabel("Appearance")
        appearance_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(appearance_label)

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark", "Light"])
        main_layout.addWidget(self.theme_selector)

        # =========================
        # MEMORY SETTINGS
        # =========================
        memory_label = QLabel("Memory")
        memory_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(memory_label)

        self.memory_enabled_checkbox = QCheckBox("Enable memory saving")
        self.memory_enabled_checkbox.setChecked(True)
        main_layout.addWidget(self.memory_enabled_checkbox)

        self.clear_memory_button = QPushButton("Clear all memory")
        main_layout.addWidget(self.clear_memory_button)

        # =========================
        # FOOTER BUTTONS
        # =========================
        main_layout.addStretch()

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()

        self.close_button = QPushButton("Close")
        footer_layout.addWidget(self.close_button)

        main_layout.addLayout(footer_layout)

        # =========================
        # SIGNALS
        # =========================
        self.close_button.clicked.connect(self.close)
        self.clear_memory_button.clicked.connect(self.confirm_clear_memory)

    # =========================
    # SETTINGS ACCESS
    # =========================
    def get_settings(self):
        """
        Returns current settings selected by the user.
        This method is intentionally simple.
        """
        return {
            "auto_speak": self.auto_speak_checkbox.isChecked(),
            "theme": self.theme_selector.currentText(),
            "memory_enabled": self.memory_enabled_checkbox.isChecked()
        }

    # =========================
    # MEMORY CLEAR CONFIRMATION
    # =========================
    def confirm_clear_memory(self):
        reply = QMessageBox.question(
            self,
            "Clear Memory",
            "Are you sure you want to clear all saved memory?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Actual clearing logic will be handled in main_window later
            QMessageBox.information(
                self,
                "Memory Cleared",
                "All memory will be cleared."
            )
