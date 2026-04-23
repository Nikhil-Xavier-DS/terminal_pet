import requests
import subprocess
import sys
import time
import platform

OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
OLLAMA_PULL_URL = "http://localhost:11434/api/pull"


# 🔍 Check if Ollama API is reachable
def is_ollama_running():
    try:
        requests.get(OLLAMA_TAGS_URL, timeout=1)
        return True
    except:
        return False


# 🚀 Try to start Ollama automatically
def try_start_ollama():
    system = platform.system()

    print("🔄 Attempting to start Ollama...")

    try:
        if system == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Ollama"])
        elif system == "Windows":
            subprocess.Popen(["ollama", "serve"], shell=True)
        else:  # Linux
            subprocess.Popen(["ollama", "serve"])
    except Exception as e:
        print(f"⚠️ Could not auto-start Ollama: {e}")


# ⏳ Wait until Ollama is ready
def wait_for_ollama(timeout=30):
    start_time = time.time()

    while time.time() - start_time < timeout:
        if is_ollama_running():
            print("✅ Ollama is running.")
            return True

        time.sleep(1)

    print("❌ Ollama did not start within timeout.")
    return False


# 📦 Ensure model exists (and pull if needed)
def ensure_model(model_name):
    # Step 1: check if running
    if not is_ollama_running():
        try_start_ollama()

        print("⏳ Waiting for Ollama to be ready...")
        if not wait_for_ollama():
            print("❌ Please start Ollama manually.")
            sys.exit(1)

    # Step 2: list models
    try:
        res = requests.get(OLLAMA_TAGS_URL)
        models = [m["name"] for m in res.json().get("models", [])]
    except Exception:
        print("❌ Failed to query Ollama models.")
        sys.exit(1)

    # Step 3: check model
    if model_name in models:
        print(f"✅ Model '{model_name}' already available.")
        return

    # Step 4: pull model
    print(f"⬇️ Model '{model_name}' not found. Pulling...")

    res = requests.post(OLLAMA_PULL_URL, json={
        "name": model_name,
        "stream": False
    })

    if res.status_code == 200:
        print(f"✅ Model '{model_name}' downloaded.")
    else:
        print("❌ Failed to pull model.")
        print(res.text)
        sys.exit(1)