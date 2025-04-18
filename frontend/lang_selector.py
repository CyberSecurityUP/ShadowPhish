from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide2.QtCore import Qt, QTimer
import subprocess
import sys
import os

from frontend.splash_screen import ShadowPhishSplash  # Splash principal

class LanguageSelector(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("Select Language")
        self.setFixedSize(400, 200)
        self.app = app

        layout = QVBoxLayout()
        self.label = QLabel("Selecione o idioma / Select your language")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.pt_btn = QPushButton("Português 🇧🇷")
        self.pt_btn.clicked.connect(self.start_portuguese)
        layout.addWidget(self.pt_btn)

        self.en_btn = QPushButton("English 🇺🇸")
        self.en_btn.clicked.connect(self.start_english)
        layout.addWidget(self.en_btn)

        self.setLayout(layout)

    def start_portuguese(self):
        self.start_app("ShadowPhish-PTBR.py")

    def start_english(self):
        self.start_app("ShadowPhish-EN.py")

    def start_app(self, filename):
        splash = ShadowPhishSplash()
        splash.show()

        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", filename))

        if os.path.exists(full_path):
            # Abre o script do idioma como subprocesso
            QTimer.singleShot(1500, lambda: subprocess.Popen([sys.executable, full_path]))
            # Fecha splash e LanguageSelector
            QTimer.singleShot(1800, lambda: (splash.close(), self.close(), self.app.quit()))
        else:
            print(f"[ERRO] Script não encontrado: {full_path}")
