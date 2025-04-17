import sys
import json
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer

from frontend.splash_screen import ShadowPhishSplash
from frontend.lang_selector import LanguageSelector

# Importa a aplicação principal
from backend.ShadowPhish import DarkThemeApp

# Função para carregar idioma selecionado
def load_language(lang_code):
    try:
        with open(f"i18n/{lang_code}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERRO] Falha ao carregar idioma '{lang_code}': {e}")
        return {}

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Splash animado
    splash = ShadowPhishSplash()
    splash.show()

    # Após splash, mostra seletor de idioma
    def show_lang_selector():
        lang_window = LanguageSelector(callback=start_main_app)
        lang_window.show()

    # Inicia a aplicação principal com idioma carregado
    def start_main_app(lang_code):
        language_data = load_language(lang_code)

        main_window = DarkThemeApp(lang_code, language_data)
        main_window.setWindowTitle(language_data.get("title", "ShadowPhish - APT Awareness Toolkit"))

        # Se quiser passar a tradução pro app: main_window.language_data = language_data
        main_window.show()
        splash.finish(main_window)

    QTimer.singleShot(2500, show_lang_selector)  # espera 2.5s do splash

    sys.exit(app.exec_())
