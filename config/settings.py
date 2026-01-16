"""
Configuration management for the AI Observability Platform.

This module centralizes all configuration settings using environment variables
with sensible defaults for local development.
"""

import os
from pathlib import Path
from typing import Optional

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"sqlite:///{PROJECT_ROOT}/data/observability.db"
)

# Ensure data directory exists
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))  # seconds

# Embedding Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = 384  # For all-MiniLM-L6-v2

# Evaluation Configuration
EVALUATION_BATCH_SIZE = int(os.getenv("EVALUATION_BATCH_SIZE", "10"))
EVALUATION_LOOKBACK_HOURS = int(os.getenv("EVALUATION_LOOKBACK_HOURS", "1"))

# Alert Thresholds
ALERT_HALLUCINATION_THRESHOLD = float(os.getenv("ALERT_HALLUCINATION_THRESHOLD", "0.6"))
ALERT_DRIFT_THRESHOLD = float(os.getenv("ALERT_DRIFT_THRESHOLD", "0.3"))
ALERT_LATENCY_THRESHOLD_MS = float(os.getenv("ALERT_LATENCY_THRESHOLD_MS", "5000"))

# Drift Detection Configuration
DRIFT_BASELINE_WINDOW_DAYS = int(os.getenv("DRIFT_BASELINE_WINDOW_DAYS", "7"))
DRIFT_RECENT_WINDOW_HOURS = int(os.getenv("DRIFT_RECENT_WINDOW_HOURS", "24"))
DRIFT_MIN_SAMPLES = int(os.getenv("DRIFT_MIN_SAMPLES", "10"))

# Dashboard Configuration
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8501"))
DASHBOARD_REFRESH_INTERVAL = int(os.getenv("DASHBOARD_REFRESH_INTERVAL", "60"))  # seconds

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_database_path() -> Path:
    """Get the absolute path to the SQLite database file."""
    if DATABASE_URL.startswith("sqlite:///"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        return Path(db_path)
    raise ValueError(f"Unsupported database URL: {DATABASE_URL}")


def validate_ollama_available() -> bool:
    """Check if Ollama is available and responding."""
    import httpx
    try:
        response = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


# Configuration summary for debugging
def print_config():
    """Print current configuration (useful for debugging)."""
    print("=" * 60)
    print("AI Observability Platform - Configuration")
    print("=" * 60)
    print(f"Database URL: {DATABASE_URL}")
    print(f"API: {API_HOST}:{API_PORT}")
    print(f"Ollama: {OLLAMA_BASE_URL} (Model: {OLLAMA_MODEL})")
    print(f"Embedding Model: {EMBEDDING_MODEL}")
    print(f"Alert Thresholds:")
    print(f"  - Hallucination: {ALERT_HALLUCINATION_THRESHOLD}")
    print(f"  - Drift: {ALERT_DRIFT_THRESHOLD}")
    print(f"  - Latency: {ALERT_LATENCY_THRESHOLD_MS}ms")
    print("=" * 60)


if __name__ == "__main__":
    print_config()
    
    # Validate Ollama
    if validate_ollama_available():
        print("✅ Ollama is available")
    else:
        print("❌ Ollama is not available - please start Ollama service")
