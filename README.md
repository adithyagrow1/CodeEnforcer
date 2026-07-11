# CodeEnforcer 🛡️

> AI-powered GitHub Pull Request review agent running on AMD Instinct MI300X GPU

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![ROCm](https://img.shields.io/badge/ROCm-7.2-red.svg)](https://rocm.docs.amd.com)
[![vLLM](https://img.shields.io/badge/vLLM-0.16.1-purple.svg)](https://vllm.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is CodeEnforcer?

CodeEnforcer is an AI agent that automatically reviews GitHub Pull Requests. Paste any public GitHub PR URL and get an instant structured code review — with bug severity labels, specific problem descriptions, and actionable fix suggestions.

All inference runs on **DeepSeek Coder 1.3B** served via **vLLM on AMD Instinct MI300X GPU** using the ROCm software stack.

Built for the **lablab.ai AMD Hackathon**.

---

## Demo

![CodeEnforcer Demo](https://raw.githubusercontent.com/adithyagrow1/CodeEnforcer/main/assets/demo.png)

---

## Features

- **Instant PR Analysis** — paste any GitHub PR URL and get results in seconds
- **Severity Classification** — issues labeled as High, Medium, or Low
- **Structured Output** — every issue comes with a problem description and a specific fix suggestion
- **GPU-Accelerated Inference** — DeepSeek Coder running on AMD MI300X via vLLM and ROCm
- **Clean Web UI** — dark-themed interface built with FastAPI and vanilla JS
- **Chunked Processing** — large PRs are split into chunks for efficient LLM processing

---

## Architecture
GitHub PR URL
↓
fetcher.py          → Fetches PR diff via GitHub API (PyGithub)
↓
chunker.py          → Splits diff into 3000-char chunks
↓
reviewer.py         → Sends each chunk to DeepSeek Coder via vLLM
↓
main.py             → Aggregates results, sorts by severity
↓
ui.py + index.html  → Displays structured review in web UI

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Web Framework | FastAPI + Uvicorn |
| GitHub Integration | PyGithub |
| LLM | DeepSeek Coder 1.3B Instruct |
| Inference Server | vLLM 0.16.1 |
| GPU Software | AMD ROCm 7.2 |
| GPU Hardware | AMD Instinct MI300X (192GB VRAM) |
| Frontend | HTML, CSS, Vanilla JS |

---

## Benchmark Results

Tested on **AMD Instinct MI300X** with DeepSeek Coder 1.3B via vLLM:

| Metric | MI300X Result |
|--------|--------------|
| Average Inference Time | 2.20s per chunk |
| Tokens per Second | 90.9 tok/sec |
| VRAM Used | 192GB available |
| Consistency (5 runs) | ~0% variance |
| Min Inference Time | 2.20s |
| Max Inference Time | 2.21s |

---

## How to Run Locally

### Prerequisites
- Python 3.10+
- GitHub Personal Access Token
- AMD GPU with ROCm (for full GPU inference) or CPU (slower)

### 1. Clone the repo
```bash
git clone https://github.com/adithyagrow1/CodeEnforcer.git
cd CodeEnforcer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install requests pygithub python-dotenv fastapi uvicorn
```

### 4. Set up environment variables
Create a `.env` file in the project root:
GITHUB_TOKEN=your_github_personal_access_token_here

Get your token at: github.com → Settings → Developer settings → Personal access tokens

### 5. Start vLLM server (requires AMD GPU with ROCm)
```bash
vllm serve deepseek-ai/deepseek-coder-1.3b-instruct --port 8080 --host 0.0.0.0
```

### 6. Run the web UI
```bash
python ui.py
```

Open http://127.0.0.1:8001 in your browser.

---

## How to Run Benchmark
```bash
python benchmark.py
```

This runs 5 inference calls and reports average time, tokens/sec, and consistency metrics.

---

## Project Structure
CodeEnforcer/
├── fetcher.py          # GitHub PR diff fetcher
├── chunker.py          # Splits diff into LLM-sized chunks
├── reviewer.py         # LLM inference via vLLM
├── main.py             # Pipeline orchestrator
├── ui.py               # FastAPI web server
├── benchmark.py        # GPU benchmark script
├── benchmark_results.json  # Saved benchmark results
├── templates/
│   └── index.html      # Web UI frontend
└── .env                # GitHub token (not committed)

---

## Example Output

```json
{
  "pr_title": "Add authentication module",
  "author": "adithyagrow1",
  "files_changed": 8,
  "total_issues": 2,
  "issues": [
    {
      "severity": "high",
      "line_reference": "auth.py",
      "issue": "SQL injection vulnerability via f-string query",
      "suggestion": "Use parameterized queries instead of f-strings"
    },
    {
      "severity": "medium", 
      "line_reference": "auth.py",
      "issue": "Password logged in plain text",
      "suggestion": "Remove print statement containing sensitive data"
    }
  ]
}
```

---

## Built With

- [DeepSeek Coder](https://github.com/deepseek-ai/DeepSeek-Coder) — Code-specialized LLM
- [vLLM](https://github.com/vllm-project/vllm) — High-throughput LLM serving
- [AMD ROCm](https://rocm.docs.amd.com) — GPU software stack
- [AMD Instinct MI300X](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html) — GPU hardware
- [FastAPI](https://fastapi.tiangolo.com) — Web framework
- [PyGithub](https://github.com/PyGithub/PyGithub) — GitHub API client

---

## Built By

**M Adithya** — 3rd year B.Tech CSE (AI/ML)  
GitHub: [@adithyagrow1](https://github.com/adithyagrow1)

Built for the **lablab.ai AMD Hackathon**

---

*CodeEnforcer — AI-powered code review on AMD MI300X*
