from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide2.QtCore import Qt

class LanguageSelector(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.setWindowTitle("Select Language")
        self.setFixedSize(400, 200)
        self.callback = callback  # função para continuar

        layout = QVBoxLayout()
        self.label = QLabel("Selecione o idioma / Select your language")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.pt_btn = QPushButton("Português 🇧🇷")
        self.pt_btn.clicked.connect(lambda: self.set_lang("pt-br"))
        layout.addWidget(self.pt_btn)

        self.en_btn = QPushButton("English 🇺🇸")
        self.en_btn.clicked.connect(lambda: self.set_lang("en"))
        layout.addWidget(self.en_btn)

        self.setLayout(layout)

    def set_lang(self, lang_code):
        self.callback(lang_code)
        self.close()
