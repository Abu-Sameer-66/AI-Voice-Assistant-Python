# 🤖 AI Voice Assistant (Python)

> **A production-grade voice assistant capable of task automation, system control, and natural language processing.** > *Built to demonstrate Python's capability in OS-level interaction and API integration.*

---

### ⚡ Key Features
- **🎙️ Wake Word Detection:** Implements an always-listening loop (waiting for *"Jarvis"*).
- **🧠 Intelligent Brain:** Integrated with **OpenAI GPT-3.5 Turbo** for context-aware conversations.
- **⚙️ Automation Suite:** - Opens core applications (Google, YouTube, Facebook).
  - Fetches real-time headlines via **NewsAPI**.
  - plays music from a curated local library.
- **🏗️ Modular Architecture:** Separates execution logic (`main.py`) from data structures (`musiclibrary.py`) for scalability.

---

### 🛠️ Tech Stack & Dependencies

| Category | Technology |
| :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white) |
| **AI Core** | `OpenAI API` (GPT-3.5 Turbo) |
| **Voice Ops** | `SpeechRecognition` `pyttsx3` `gTTS` |
| **Network** | `Requests` (API Handling) |

---

### 🚀 How to Run Locally

**1. Clone the repository**
```bash
git clone [https://github.com/Abu-Sameer-66/AI-Voice-Assistant-Python.git](https://github.com/Abu-Sameer-66/AI-Voice-Assistant-Python.git)
cd AI-Voice-Assistant-Python
