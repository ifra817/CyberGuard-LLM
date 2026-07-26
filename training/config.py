from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "processed"
OUTPUT_FILE = PROCESSED_DIR / "heimdall_llama3_processed.json"

DATASET_URL = "hf://datasets/AlicanKiraz0/Cybersecurity-Dataset-Heimdall-v1.1/train-set-conversations.json"