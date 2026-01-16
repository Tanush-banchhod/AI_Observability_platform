# 🔍 AI Observability Platform

A local-first, free observability platform for monitoring LLM applications with hallucination detection, semantic drift analysis, and real-time alerting.

## 🎯 Features

- **Telemetry Collection**: Capture LLM inputs, outputs, latency, and metadata
- **Hallucination Detection**: LLM-as-a-judge evaluation using local Ollama models
- **Semantic Drift Detection**: Embedding-based analysis to detect distribution shifts
- **Smart Alerting**: Rule-based threshold alerts for quality degradation
- **Real-time Dashboard**: Streamlit-based visualization of metrics and trends

## 🛠️ Tech Stack

- **API**: FastAPI
- **Database**: SQLite + SQLAlchemy ORM
- **Evaluation LLM**: Ollama (llama3:8b / mistral:7b)
- **Embeddings**: sentence-transformers
- **Dashboard**: Streamlit
- **Scheduling**: Python scripts (cron-compatible)

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+**
2. **Ollama** installed and running:
   ```bash
   # Install Ollama: https://ollama.ai/
   ollama pull llama3:8b
   # or
   ollama pull mistral:7b
   ```

### Installation

```bash
# Clone the repository
cd AI_Observability_platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py
```

### Running the Platform

```bash
# Terminal 1: Start FastAPI server
cd api
uvicorn main:app --reload --port 8000

# Terminal 2: Start Streamlit dashboard
streamlit run dashboard/app.py

# Terminal 3: Run evaluation job (periodic)
python scripts/run_evaluation.py
```

## 📊 Usage Example

### Sending Telemetry from Your LLM App

```python
import requests
import time

# Your LLM application
prompt = "What is the capital of France?"
start = time.time()
response = "Paris is the capital of France."  # Your LLM output
latency = time.time() - start

# Send to observability platform
requests.post("http://localhost:8000/api/v1/telemetry", json={
    "app_id": "my_chatbot",
    "model_name": "gpt-3.5-turbo",
    "prompt": prompt,
    "response": response,
    "latency_ms": latency * 1000,
    "metadata": {"user_id": "123", "session": "abc"}
})
```

## 🗄️ Database Schema

### `llm_requests`
- Stores all incoming telemetry data
- Indexed by timestamp and app_id

### `llm_evaluations`
- Hallucination scores and drift metrics
- Linked to requests via foreign key

### `alerts`
- Active alerts based on threshold rules
- Severity levels and timestamps

## 🔄 Workflow

1. **LLM App** → Sends telemetry to FastAPI
2. **FastAPI** → Validates and stores in SQLite
3. **Batch Job** → Periodically evaluates quality with Ollama
4. **Drift Detector** → Computes embedding-based drift
5. **Alert Engine** → Applies threshold rules
6. **Dashboard** → Visualizes metrics and alerts

## 🚨 Alert Rules

- Hallucination score below threshold (default: 0.6)
- Drift distance exceeds baseline (default: 0.3)
- High latency (default: >5000ms)
- Error rate spikes

## 📈 Dashboard Features

- **Overview**: Request volume, average latency, quality trends
- **Evaluations**: Hallucination scores over time
- **Drift Analysis**: Semantic drift visualization
- **Alerts**: Active alerts and historical trends
- **Request Explorer**: Drill down into individual LLM calls

## 🏗️ Architecture Principles

- **Local-first**: No cloud dependencies, runs entirely on your machine
- **Free**: Uses only open-source and free tools
- **Modular**: Clean separation of concerns
- **Extensible**: Easy to add new metrics and evaluators
- **Production-ready code**: Type hints, error handling, logging

## 📝 License

MIT License - Free for personal and commercial use

## 🤝 Contributing

This is a portfolio project. Feel free to fork and extend!

---

**Built with ❤️ for the LLM community**
