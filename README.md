# ShadowPhish - APT Awareness Toolkit  

Versão: 1.0  
Autor: Joas A Santos  

Descrição:
----------
ShadowPhish é uma poderosa ferramenta gráfica para simulação de ameaças cibernéticas
e conscientização sobre APTs (Advanced Persistent Threats), focada em engenharia social, 
phishing, deepfake e payloads ofensivos para treinamento e demonstração.

Funcionalidades:
----------------
✔ Geração de PDF e Macro maliciosos  
✔ PowerShell evasivo com codificação e compressão  
✔ VBS com download de shellcode e servidor embutido  
✔ Sites de phishing prontos e recaptcha falso com pastejack  
✔ Deepfake de rosto (vídeo) e clonagem de voz (TTS)  
✔ Payload C2 para Windows, Linux e macOS com shell reversa  
✔ Cadeia de ataque baseada em APT29, APT41, FIN7  
✔ Smishing e Vishing via Twilio  
✔ Gerador de Atalhos LNK maliciosos  
✔ HTML Smuggling com arquivos base64  
✔ Simulador de Ransomware e Decryptor  
✔ Geração de QR Code apontando para link malicioso  

Requisitos:
-----------
- Python 3.10+  
- MinGW (para compilar payloads Windows)  
- GCC (Linux/macOS)  
- PHP (para sites de phishing)  
- Internet (para deepfake e TTS)  

Instalação:
-----------
1. Instale os requisitos:  
   `pip install -r requirements.txt`

2. Rode a aplicação:  
   `python main.py`

Pastas:
-------
- backend/         → Código principal da aplicação  
- frontend/        → Splash screen e seletor de idioma  
- .sites/          → Templates HTML para phishing (baseados no projeto Zphisher)  
- .fake-recaptcha/ → Template para simulação de Recaptcha malicioso  
- outputs/         → Arquivos gerados  
- i18n/            → Traduções em JSON  

Créditos:
---------
- Desenvolvido por Joas A Santos  
- Templates `.sites/` baseados no projeto Zphisher:  
  🔗 https://github.com/htr-tech/zphisher/tree/master/.sites

Licença:
--------
🔒 Ferramenta destinada **exclusivamente para fins educacionais**, 
simulações de conscientização e uso ético autorizado.

