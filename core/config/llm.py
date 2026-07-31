import os


# ============== LLM PROVIDER ==============

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
)


# ============== OLLAMA ==============

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3"
)


# ============== GENERATION ==============

LLM_TEMPERATURE = float(
    os.getenv(
        "LLM_TEMPERATURE",
        "0.7"
    )
)

LLM_TIMEOUT = int(
    os.getenv(
        "LLM_TIMEOUT",
        "30"
    )
)