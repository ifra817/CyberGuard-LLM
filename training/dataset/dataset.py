import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "processed"
OUTPUT_FILE = PROCESSED_DIR / "heimdall_llama3_processed.json"

DATASET_URL = "hf://datasets/AlicanKiraz0/Cybersecurity-Dataset-Heimdall-v1.1/train-set-conversations.json"

def load_dataset(path_or_url: str) -> pd.DataFrame:
    """Load JSON records into a Pandas DataFrame."""
    print(f"Loading raw dataset from {path_or_url}...")
    # Standard read_json loads the list of message arrays
    df = pd.read_json(path_or_url)
    print(f"Loaded {len(df)} total conversation instances.")
    return df

def validate_and_filter(df: pd.DataFrame) -> list:
    """Validate each conversation list and throw out broken or empty messages."""
    print("Validating messages...")
    clean_conversations = []
    
    for _, row in df.iterrows():
        messages = []
        
        # Check system prompt if present
        if "system" in row and pd.notna(row["system"]) and str(row["system"]).strip():
            messages.append({"role": "system", "content": str(row["system"]).strip()})
            
        # Check user prompt
        if "user" in row and pd.notna(row["user"]) and str(row["user"]).strip():
            messages.append({"role": "user", "content": str(row["user"]).strip()})
            
        # Check assistant prompt
        if "assistant" in row and pd.notna(row["assistant"]) and str(row["assistant"]).strip():
            messages.append({"role": "assistant", "content": str(row["assistant"]).strip()})
            
        # Ensure at least a user and assistant pair exist
        if len(messages) >= 2:
            clean_conversations.append(messages)
            
    print(f"Validation complete. Retained {len(clean_conversations)} valid conversations.")
    return clean_conversations

def format_chat_template(messages: list) -> str:
    """
    Formats the list of turn objects into standard Llama-3 Chat prompt:
    <|begin_of_text|><|start_header_id|>role<|end_header_id|>

    content<|eot_id|>
    """
    formatted_prompt = "<|begin_of_text|>"
    
    for msg in messages:
        role = msg["role"].strip().lower()
        content = msg["content"].strip()
        
        formatted_prompt += f"<|start_header_id|>{role}<|end_header_id|>\n\n{content}<|eot_id|>"
        
    return formatted_prompt

def process_dataset():
    """Main execution block following your project pipeline steps."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load
    df = load_dataset(DATASET_URL)
    
    # 2 & 3. Validate & Filter
    cleaned_conversations = validate_and_filter(df)
    
    # 4. Convert into Llama chat format
    print("Formatting conversations into Llama-3 prompt template...")
    processed_records = []
    
    for idx, messages in enumerate(cleaned_conversations):
        formatted_text = format_chat_template(messages)
        
        processed_records.append({
            "id": idx,
            "text": formatted_text,
            "messages": messages  # Keeping raw structured messages for HuggingFace SFT / Trainer compatibility
        })
        
    # 5. Save processed dataset
    print(f"Saving processed data to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_records, f, indent=2, ensure_ascii=False)
        
    print("Dataset processing complete!")

if __name__ == "__main__":
    process_dataset()