import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft.peft_model import PeftModel

BASE_MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"
LORA_PATH = "./models/cyberguard-lora-v1"  # Path to your fine-tuned adapter folder
OUTPUT_DIR = "./models/merged_cyberguard"

print("Loading base model into CPU RAM...")
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_ID,
    torch_dtype=torch.float16,
    device_map="cpu"
)

print("Attaching fine-tuned LoRA weights...")
model = PeftModel.from_pretrained(base_model, LORA_PATH)

print("Merging weights into a single model...")
merged_model = model.merge_and_unload()

print(f"Saving merged model to {OUTPUT_DIR}...")
merged_model.save_pretrained(OUTPUT_DIR)

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)
tokenizer.save_pretrained(OUTPUT_DIR)

print("Merge complete!")