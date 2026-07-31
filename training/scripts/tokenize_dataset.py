from pathlib import Path
import json
from datasets import Dataset
from transformers import AutoTokenizer

# -----------------------------------------------------------------------------
# Path Resolution
# -----------------------------------------------------------------------------
# Script path: CyberGuard-LLM/training/scripts/train.py
SCRIPT_DIR = Path(__file__).resolve().parent
TRAINING_DIR = SCRIPT_DIR.parent

PROCESSED_DATA_PATH = TRAINING_DIR / "dataset" / "processed" / "heimdall_llama3_processed.json"
TOKENIZED_DIR = TRAINING_DIR / "dataset" / "tokenized"

MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"

# -----------------------------------------------------------------------------
# Tokenization Logic
# -----------------------------------------------------------------------------
def tokenize_function(example, tokenizer, max_length=2048):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=max_length,
        padding=False,  # Set to False if using dynamic padding in Trainer later
    )

def main():
    # 1. Load Processed JSON Dataset
    print(f"Loading dataset from: {PROCESSED_DATA_PATH}")
    with open(PROCESSED_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    dataset = Dataset.from_list(data)

    # 2. Initialize Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # 3. Apply Tokenization
    print("Tokenizing dataset...")
    tokenized_dataset = dataset.map(
        lambda example: tokenize_function(example, tokenizer),
        batched=True,
        remove_columns=dataset.column_names,  # Keeps target tensors clean
    )

    # 4. Save Tokenized Dataset to Disk
    TOKENIZED_DIR.mkdir(parents=True, exist_ok=True)
    tokenized_dataset.save_to_disk(TOKENIZED_DIR)
    print(f"Tokenized dataset successfully saved to: {TOKENIZED_DIR}")
    print(f"Features: {tokenized_dataset.column_names}")

if __name__ == "__main__":
    main()