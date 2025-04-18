import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer
from frontend.splash_lang import SplashInicial
from frontend.lang_selector import LanguageSelector

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = SplashInicial()
    splash.show()

    global lang_selector_window
    lang_selector_window = None

    def show_lang_selector():
        global lang_selector_window
        lang_selector_window = LanguageSelector(app)
        lang_selector_window.show()
        splash.finish(lang_selector_window)

    QTimer.singleShot(2000, show_lang_selector)

    sys.exit(app.exec_())
