# 🕵️‍♂️ ShadowPhish - APT Awareness Toolkit

**Versão:** 1.0  
**Autor:** Joas A Santos

> Simulador visual para conscientização sobre APTs, phishing, engenharia social e ameaças cibernéticas.

---

## 🔥 Funcionalidades

- ✅ Geração de PDFs maliciosos
- ✅ Macros Word com shellcode remoto
- ✅ PowerShell evasivo com opções de codificação, compressão e IEX
- ✅ VBS remoto com shellcode + servidor embutido
- ✅ Sites de phishing prontos (.sites/)
- ✅ Recaptcha Falso (PasteJack)
- ✅ Deepfake (FaceFusion) e DeepVoice (TTS)
- ✅ Geração de Payload C2 para Windows, Linux e macOS
- ✅ Terminal interativo com listener embutido
- ✅ Cadeias de ataque APT29, APT41, FIN7
- ✅ Smishing (SMS) e Vishing (ligação com áudio)
- ✅ Gerador de LNK malicioso
- ✅ HTML Smuggling (base64 + download automático ou por clique)
- ✅ Simulador de Ransomware e Decryptor
- ✅ Geração de QR Code malicioso

---

## ⚙️ Requisitos

- Python 3.10+
- PHP (para servidores de phishing)
- GCC / MinGW
- ffmpeg + facefusion (para deepfake)
- Internet (para TTS, APIs)

Instale as dependências:
```bash
pip install -r requirements.txt
```

---

## 🚀 Como usar

```bash
python main.py
```

- Uma splash screen será exibida
- Selecione o idioma desejado
- A interface principal será carregada

---

## 📁 Estrutura

```
.
├── main.py
├── backend/           # Código principal
├── frontend/          # Splash + seletor de idioma
├── .sites/            # Templates de phishing
├── .fake-recaptcha/   # Recaptcha falso com payload automático
├── outputs/           # Arquivos gerados
├── i18n/              # Traduções em JSON
└── requirements.txt
```

---

## 🙏 Créditos

- Desenvolvido por **Joas A Santos**
- Templates `.sites/` extraídos e adaptados do excelente projeto [Zphisher](https://github.com/htr-tech/zphisher)

---

## ⚠️ Aviso Legal

> Esta ferramenta é **estritamente educacional**, voltada para **conscientização e simulações** de segurança ofensiva.  
> **Não utilize em ambientes reais sem autorização.**

---

# 🕵️‍♂️ ShadowPhish - APT Awareness Toolkit

**Version:** 1.0  
**Author:** Joas A Santos

> Visual simulator for cybersecurity awareness, phishing, and APT-based social engineering.

---

## 🔥 Features

- ✅ Malicious PDF generator
- ✅ Word macro with remote shellcode
- ✅ PowerShell obfuscation (Base64, IEX, compression, variables)
- ✅ Remote VBS + embedded HTTP server
- ✅ Prebuilt phishing websites (.sites/)
- ✅ Fake Recaptcha (PasteJack style)
- ✅ Deepfake video (FaceFusion) and DeepVoice TTS
- ✅ Payload generator for Windows, Linux, macOS
- ✅ Built-in reverse shell listener with command interface
- ✅ APT Chains (APT29, APT41, FIN7)
- ✅ Smishing (SMS) and Vishing (voice call via Twilio)
- ✅ Malicious LNK shortcut builder
- ✅ HTML Smuggling generator (Base64 embedded)
- ✅ Simulated Ransomware + Decryptor
- ✅ QR Code phishing generator

---

## ⚙️ Requirements

- Python 3.10+
- PHP (for phishing sites)
- GCC / MinGW
- ffmpeg + facefusion
- Internet access (for DeepVoice and APIs)

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

```bash
python main.py
```

- Animated splash screen will appear
- Choose your language
- Toolkit interface will load

---

## 📁 Project Structure

```
.
├── main.py
├── backend/           # Main logic
├── frontend/          # Splash + language selector
├── .sites/            # Phishing templates
├── .fake-recaptcha/   # Fake Recaptcha pastejack
├── outputs/           # Generated files
├── i18n/              # Translations
└── requirements.txt
```

---

## 🙏 Credits

- Developed by **Joas A Santos**
- `.sites/` templates inspired and adapted from [Zphisher](https://github.com/htr-tech/zphisher)

---

## ⚠️ Legal Notice

> This toolkit is **strictly for educational and awareness purposes** only.  
> Do **not use** in real environments without **explicit authorization**.
