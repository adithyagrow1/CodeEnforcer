<p align="center">
  <img src="static/image.jpeg" alt="CodeEnforcer Banner" width="100%" />
</p>

<h1 align="center">CodeEnforcer</h1>

<p align="center">
  <b>AI-Powered GitHub Pull Request Review Agent</b><br/>
  <sub>Automatically analyze code diffs and surface bugs with severity labels, root-cause descriptions, and fix suggestions — powered by DeepSeek Coder on AMD MI300X.</sub>
</p>

<p align="center">
  <a href="https://github.com/adithyagrow1/CodeEnforcer"><img src="https://img.shields.io/badge/GitHub-CodeEnforcer-181717?logo=github&logoColor=white" alt="GitHub Repo" /></a>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/DeepSeek_Coder-6.7B-4A90D9?logo=codeium&logoColor=white" alt="DeepSeek Coder" />
  <img src="https://img.shields.io/badge/AMD-MI300X-ED1C24?logo=amd&logoColor=white" alt="AMD MI300X" />
  <img src="https://img.shields.io/badge/ROCm-7.2-orange?logo=amd&logoColor=white" alt="ROCm" />
  <img src="https://img.shields.io/badge/Hackathon-lablab.ai_×_AMD-blueviolet" alt="Hackathon" />
</p>

---

## 📌 What is CodeEnforcer?

**CodeEnforcer** is an AI-powered code review agent that analyzes GitHub Pull Requests in real time. Paste any public PR URL into the web interface, and the system will:

1. Fetch the full diff from the GitHub API
2. Split the diff into manageable chunks
3. Send each chunk to **DeepSeek Coder 6.7B** running on an **AMD Instinct MI300X** GPU
4. Return structured bug reports with severity labels, problem descriptions, and fix suggestions
5. Display everything in a clean, dark-themed dashboard with color-coded severity indicators

No manual setup per-repo — just paste a URL and go.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Real-Time PR Analysis** | Paste a GitHub PR URL and get an instant, structured review via the web UI |
| 🚦 **Severity Classification** | Issues are labeled **High** (🔴), **Medium** (🟡), or **Low** (🟢) with color-coded cards |
| 🛡️ **Security Bug Detection** | Catches SQL injection, auth flaws, hardcoded secrets, and other security issues |
| 📐 **Code Quality Analysis** | Identifies code smells, style violations, logic errors, and missing edge cases |
| ⚡ **GPU-Accelerated Inference** | Runs DeepSeek Coder 6.7B on AMD Instinct MI300X for fast inference via vLLM + ROCm |
| 🌑 **Dark-Themed Web UI** | Glassmorphism-styled dashboard with JetBrains Mono code font and smooth animations |
| 📊 **Chunk Summaries** | Each diff chunk receives a one-line summary so you can skim large PRs |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Web Browser                          │
│              (Dark-themed UI · HTML/CSS/JS)                 │
└──────────────────────┬──────────────────────────────────────┘
                       │  POST /review  { url }
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (ui.py)                   │
│         Serves the UI and handles /review endpoint          │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────▼───────────────────┐
          │     main.py (Orchestrator)     │
          │  Coordinates the full pipeline │
          └─┬──────────┬──────────┬────────┘
            │          │          │
   ┌────────▼──┐ ┌─────▼──────┐ ┌─▼──────────┐
   │ fetcher.py│ │ chunker.py │ │reviewer.py │
   │  PyGithub │ │ Splits diff│ │ Calls LLM  │
   │  API call │ │ into chunks│ │ per chunk  │
   └───────────┘ └────────────┘ └──────┬─────┘
                                      │
                               ┌──────▼──────────────────┐
                               │  DeepSeek Coder 6.7B    │
                               │  served via Ollama/vLLM │
                               │  on AMD MI300X (ROCm)   │
                               └─────────────────────────┘
```

**Pipeline Flow:**

1. **`fetcher.py`** — Authenticates via a GitHub token and fetches the PR diff using `PyGithub`
2. **`chunker.py`** — Splits the raw diff into ≤ 3 000-character chunks to fit the model's context window
3. **`reviewer.py`** — Sends each chunk to DeepSeek Coder with a structured prompt and parses the JSON response
4. **`main.py`** — Orchestrates the above modules, aggregates issues, sorts by severity, and returns the final report
5. **`ui.py`** — FastAPI server that serves the web UI and exposes the `/review` API endpoint

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python · FastAPI · Uvicorn |
| **GitHub Integration** | PyGithub · GitHub REST API |
| **LLM** | DeepSeek Coder 6.7B |
| **Inference Runtime** | Ollama / vLLM |
| **GPU** | AMD Instinct MI300X (192 GB HBM3) |
| **GPU SDK** | ROCm 7.2 |
| **Frontend** | HTML · CSS (glassmorphism) · Vanilla JS |
| **Font Stack** | Tactic Sans · JetBrains Mono |

---

## 🚀 How to Run Locally

### Prerequisites

- Python 3.10+
- A [GitHub Personal Access Token](https://github.com/settings/tokens) (classic, with `repo` scope for private repos or no scope for public repos)
- [Ollama](https://ollama.com/) installed **or** a running vLLM instance with DeepSeek Coder

### 1 · Clone the Repository

```bash
git clone https://github.com/adithyagrow1/CodeEnforcer.git
cd CodeEnforcer
```

### 2 · Create a Virtual Environment & Install Dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install fastapi uvicorn pygithub python-dotenv requests
```

### 3 · Set Up Your Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=ghp_your_personal_access_token_here
```

### 4 · Start the LLM Backend

**Option A — Ollama (recommended for local dev):**

```bash
ollama pull deepseek-coder:6.7b
ollama serve
```

**Option B — vLLM on AMD MI300X:**

```bash
python -m vllm.entrypoints.openai.api_server \
  --model deepseek-ai/deepseek-coder-6.7b-instruct \
  --device rocm
```

> Update `OLLAMA_URL` in `reviewer.py` if your inference server is on a different host/port.

### 5 · Launch CodeEnforcer

```bash
python ui.py
```

Open your browser at **[http://127.0.0.1:8001](http://127.0.0.1:8001)** and paste a GitHub PR URL to start reviewing.

---

## 📈 AMD MI300X Benchmark Results

> Benchmarks run with DeepSeek Coder 6.7B, batch size 1, ~3 000-token prompt.

| Metric | MI300X | CPU (baseline) |
|---|:---:|:---:|
| Time to First Token (TTFT) | — | — |
| Tokens / second | — | — |
| Full chunk review latency | — | — |
| VRAM utilization | — | — |
| Peak throughput (batch 8) | — | — |

*Fill in measured values after running benchmarks on the AMD Developer Cloud.*

---

## 📸 Screenshots

<p align="center">
  <em>Screenshots coming soon — the web UI features a dark glassmorphism design with severity-coded issue cards.</em>
</p>

<!-- Uncomment and replace with actual screenshots:
<p align="center">
  <img src="screenshots/home.png" alt="Home Screen" width="80%" />
</p>
<p align="center">
  <img src="screenshots/review.png" alt="Review Results" width="80%" />
</p>
-->

---

## 📁 Project Structure

```
CodeEnforcer/
├── ui.py              # FastAPI server — serves UI & /review endpoint
├── main.py            # Pipeline orchestrator
├── fetcher.py         # GitHub PR diff fetcher (PyGithub)
├── chunker.py         # Diff → chunks splitter
├── reviewer.py        # LLM inference per chunk (DeepSeek Coder)
├── app.py             # Alternative Gradio UI (optional)
├── templates/
│   └── index.html     # Main web interface
├── static/
│   ├── image1.jpg     # Background image
│   └── *.woff2        # Tactic Sans font files
├── .env               # GitHub token (not committed)
└── .gitignore
```

---

## 🏆 Built For

<p align="center">
  <a href="https://lablab.ai"><img src="https://img.shields.io/badge/lablab.ai-AMD_Hackathon-blueviolet?style=for-the-badge" alt="lablab.ai AMD Hackathon" /></a>
</p>

---

## 🧰 Built With

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PyGithub-181717?style=for-the-badge&logo=github&logoColor=white" alt="PyGithub" />
  <img src="https://img.shields.io/badge/DeepSeek_Coder-6.7B-4A90D9?style=for-the-badge" alt="DeepSeek Coder" />
  <img src="https://img.shields.io/badge/vLLM-FF6F00?style=for-the-badge" alt="vLLM" />
  <img src="https://img.shields.io/badge/ROCm-7.2-orange?style=for-the-badge&logo=amd&logoColor=white" alt="ROCm" />
  <img src="https://img.shields.io/badge/AMD-Instinct_MI300X-ED1C24?style=for-the-badge&logo=amd&logoColor=white" alt="AMD MI300X" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
</p>

---

<p align="center">
  Made with 🧡 by <a href="https://github.com/adithyagrow1">adithyagrow1</a>
</p>
