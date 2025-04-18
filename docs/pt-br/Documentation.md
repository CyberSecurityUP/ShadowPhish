## 📄 Documentação - ShadowPhish

### 🔐 Artefatos Maliciosos

#### [PT-BR] Gerar PDF Malicioso
Gera um arquivo `.pdf` que ao ser clicado redireciona o usuário para uma URL maliciosa.

- Entrada: URL do site malicioso.
- Saída: `badphish.pdf`.
- Uso: Engenharia social com iscas PDF.

#### [EN] Generate Malicious PDF
Creates a `.pdf` file that, when clicked, redirects the user to a malicious URL.

- Input: Malicious site URL.
- Output: `badphish.pdf`
- Usage: Social engineering with PDF lures.

---

#### [PT-BR] Documento Word com Macro
Gera um código VBA que baixa e executa um shellcode remoto em um `.docm` ou `.doc`.

- Requer: URL de shellcode e caminho local para salvamento.
- Saída: `macro_payload.vba`

#### [EN] Word Macro Document
Creates a VBA macro that downloads and executes a remote shellcode in a Word document.

- Requires: Shellcode URL and local path.
- Output: `macro_payload.vba`

---

#### [PT-BR] PowerShell Ofuscado
Gera um script PowerShell com opções de evasão:
- Base64
- Substituição de variáveis
- Concatenação
- Compressão

#### [EN] Obfuscated PowerShell
Generates an obfuscated PowerShell script with evasion techniques:
- Base64
- Variable substitution
- String concatenation
- Compression

---

#### [PT-BR] VBS com Shellcode Remoto
Cria um dropper em `.vbs` que baixa um shellcode `.bin` via HTTP e o salva em `C:\Users\Public\`.

- Requer: shellcode binário e IP/porta do servidor embutido.
- Inicia um servidor HTTP para entrega.

#### [EN] Remote Shellcode VBS
Creates a `.vbs` dropper that downloads a `.bin` shellcode via HTTP and saves it to `C:\Users\Public\`.

- Requires: binary shellcode and embedded HTTP server.
- Starts a local HTTP server to serve the file.

---

### 🎣 Phishing & Spear-Phishing

#### [PT-BR] Site Falso com Template
Seleciona um template clonado de site famoso e inicia um servidor PHP com coleta de credenciais.

- Templates: Facebook, Instagram, Google, etc.
- Monitoramento de `usernames.txt` em tempo real.

#### [EN] Fake Site from Template
Launches a cloned site template and starts a PHP server with credential collection.

- Templates: Facebook, Instagram, Google, etc.
- Live monitoring of `usernames.txt`.

---

#### [PT-BR] Recaptcha Falso (Pastejack)
Gera um site com recaptcha falso que copia automaticamente um payload para o clipboard.

- Define sistema-alvo: Windows, Linux ou macOS.
- Modifica HTML e JS com base no payload inserido.

#### [EN] Fake Recaptcha (Pastejack)
Generates a fake recaptcha page that auto-copies a payload to the user's clipboard.

- Target OS: Windows, Linux or macOS.
- Modifies the template's HTML and JS with given payload.

---

### 🧠 Deepfake & Deepvoice

#### [PT-BR] Deepfake de Vídeo
Usa o FaceFusion para aplicar troca de rosto em um vídeo fornecido.

- Requer: imagem da face e vídeo.
- Saída: `deepfake_output.mp4`

#### [EN] Deepfake Video
Uses FaceFusion to swap faces in a given video.

- Requires: face image and video file.
- Output: `deepfake_output.mp4`

---

#### [PT-BR] Voz Clonada (Deepvoice)
Gera áudio `.mp3` usando Microsoft Edge TTS com vozes de figuras conhecidas.

- Entrada: texto e escolha de voz.
- Saída: `cloned_voice.mp3`

#### [EN] Cloned Voice (Deepvoice)
Generates `.mp3` audio using Microsoft Edge TTS with famous personalities.

- Input: text and voice.
- Output: `cloned_voice.mp3`

---

### 💻 Simulated C2

#### [PT-BR] Payload C2
Gera payloads de reverse shell em C para Windows, Linux ou macOS e compila automaticamente.

- Cria listener e terminal integrado.
- Inclui comandos rápidos por SO.

#### [EN] C2 Payload
Generates C-based reverse shell payloads for Windows, Linux, or macOS and compiles them.

- Includes listener and terminal.
- Provides default commands per OS.

---

### 🎯 Cadeia APT

#### [PT-BR] Cadeias de Ataque APT
Seleciona um grupo (APT29, FIN7, APT41) e gera uma sequência de ataques simulando sua TTP.

#### [EN] APT Attack Chain
Selects a group (APT29, FIN7, APT41) and generates a simulated chain of their common TTPs.
