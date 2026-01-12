# Neural Shadow 🧠🌑
> *The AI that remembers everything you see and hear.*

**Neural Shadow** is a local-first, zero-knowledge desktop intelligence system. It acts as a photographic memory for your digital life, continuously capturing screen content and system audio, indexing it into a local vector database, and allowing for semantic natural language retrieval.

---

## 🚀 Features

- **Total Recall**: 24/7 Background capture of Screen (OCR) and Audio (Whisper).
- **Semnatic Search**: Ask questions like *"What command did I run for Docker last week?"*
- **Diff-Based Optimization**: Only saves screen updates when pixels change (>0.5%).
- **Local-First**: 100% of data stays on your machine.
- **RAG Powered**: Uses **ChromaDB** + **Ollama** (Mistral/Llama3) to answer questions contextually.
- **Encrypted**: All raw screen/audio data is encrypted at rest using Fernet (AES).

## 🛠️ Architecture

The system is built on a modular "Cortex" architecture:

1.  **Senses**: `mss` (Screen) and `soundcard` (Audio) capture raw data.
2.  **Cortex**: `OCR` (Tesseract) and `Whisper` extract text.
3.  **Memory**: `ChromaDB` stores semantic embeddings (`all-MiniLM-L6-v2`).
4.  **Gateway**: `FastAPI` exposes a Search Endpoint.
5.  **Interface**: `Next.js` Cyberpunk Dashboard for interaction.

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (Installed and added to PATH)
- [Ollama](https://ollama.ai/) (Running `ollama serve` with `mistral`)

### Quick Start (Windows)
1.  **Clone the Repo**
    ```bash
    git clone https://github.com/Kshithijm1/NeuralShadow.git
    cd NeuralShadow
    ```
2.  **Install Backend**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Install Frontend**
    ```bash
    cd web
    npm install
    ```
4.  **Run All**
    Double-click `start.bat` or run:
    ```bash
    python main.py      # Terminal 1
    npm run dev --prefix web  # Terminal 2
    ```

## 💡 Usage Examples
Once the system is running, open `http://localhost:3000` and press `Cmd+K` (or `Ctrl+K`) to open the search bar.

### 1. Developer Productivity
> *"What flags did I use for the docker build command yesterday?"*
> *"Show me the python script I was editing an hour ago."*

### 2. Meeting Recall
> *"What action items were assigned to me during the sync?"*
> *"Summarize the feedback from the design review."*

### 3. Digital Wellbeing
> *"What website was I looking at before I got distracted?"*

## 🔒 Security
Neural Shadow is designed with privacy as the #1 priority.
- **Zero-Cloud**: No data is sent to OpenAI or any cloud provider.
- **Encryption**: By default, `ENABLE_ENCRYPTION = True` in `core/config.py`. All `.png` and `.wav` files are encrypted with `secret.key`.

## 🐳 Docker Support
Run the full stack in a container (Experimental):
```bash
docker-compose up --build
```
