import sys
import os
import subprocess
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer
from frontend.splash_screen import ShadowPhishSplash
from frontend.lang_selector import LanguageSelector

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Splash animado
    splash = ShadowPhishSplash()
    splash.show()

    # Mostra o seletor após o splash
    def show_lang_selector():
        app.lang_window = LanguageSelector()  # Mantém viva a janela
        app.lang_window.show()
        splash.finish(app.lang_window)

    QTimer.singleShot(2500, show_lang_selector)
    sys.exit(app.exec_())
