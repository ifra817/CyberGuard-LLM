from pathlib import Path
import json

import torch

from datasets import Dataset

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
)

from peft import (
    LoraConfig,
    get_peft_model,
)

from trl.trainer.sft_trainer import SFTTrainer

def tokenize_function(example):                   
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=2048,
        padding="longest"
    )

BASE_DIR = Path(__file__).resolve().parent.parent
TOKENIZED_DIR = BASE_DIR / "dataset" / "tokenized"
json_path = BASE_DIR / "dataset"/ "processed" / "heimdall_llama3_processed.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

dataset = Dataset.from_list(data)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
tokenizer.pad_token = tokenizer.eos_token  # Set pad token to eos token

tokenized_dataset = dataset.map(tokenize_function)
tokenized_dataset.save_to_disk(TOKENIZED_DIR)
print(tokenized_dataset[0].keys())      
