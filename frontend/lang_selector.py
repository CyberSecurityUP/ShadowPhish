from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide2.QtCore import Qt
import subprocess
import sys
import os

class LanguageSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selecione o idioma / Select language")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        self.label = QLabel("Escolha o idioma / Choose language")
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
        print("[INFO] Iniciando versão em Português...")
        self.close()
        self.run_script("ShadowPhish-PTBR.py")

    def start_english(self):
        print("[INFO] Starting English version...")
        self.close()
        self.run_script("ShadowPhish-EN.py")

    def run_script(self, script_name):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", script_name))

        if os.path.exists(script_path):
            subprocess.Popen([sys.executable, script_path])
        else:
            print(f"[ERRO] Script não encontrado: {script_path}")
