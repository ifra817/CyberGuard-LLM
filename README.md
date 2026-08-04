# CyberGuard LLM 🛡️🤖

> **An AI-Powered Cybersecurity Incident Analysis & Educational Assistant**

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Base Model](https://img.shields.io/badge/base__model-Llama--3.2--3B--Instruct-orange)
![Method](https://img.shields.io/badge/fine--tuning-QLoRA%204--bit-purple)
![Status](https://img.shields.io/badge/status-In%20Development-yellow)

---

## 📌 Project Overview

**CyberGuard LLM** is an open-weight Large Language Model domain-adapted for cybersecurity incident analysis and education. Built by fine-tuning **Meta Llama-3.2-3B-Instruct** using 4-bit **QLoRA (Quantized Low-Rank Adaptation)**, this assistant analyzes user-described security threats, evaluates suspicious code, explains complex security concepts, and provides actionable remediation guidance through a local Streamlit interface.

---

## ✨ Key Features

* **Cybersecurity Knowledge Base:** Answers queries on phishing, malware/ransomware mechanics, MFA, network protocols, web vulnerabilities (SQLi, XSS), and secure coding practices.
* **Guided Incident Analysis:** Evaluates reported symptoms (e.g., suspicious emails, compromised credentials) to provide root cause analysis, risk severity indicators, and prioritized mitigation steps.
* **Code Security Review:** Audits code snippets for potential vulnerabilities, hardcoded credentials, and unsafe input handling.
* **Dual-Model Comparative Interface:** Allows side-by-side comparison between the base Llama 3.2 model and the fine-tuned CyberGuard checkpoint.

---

## 🛠️ Tech Stack

| Category | Tools & Libraries |
| :--- | :--- |
| **Base Model** | Meta Llama-3.2-3B-Instruct |
| **Fine-Tuning Method** | 4-bit QLoRA (`peft`, `bitsandbytes`, `trl` SFTTrainer) |
| **Core ML Framework** | PyTorch, Hugging Face `transformers` |
| **Inference Engine** | `llama.cpp` (GGUF format) |
| **Frontend UI** | Streamlit |
| **Language** | Python 3.10 / 3.11 / 3.12 |

---

## 📁 Repository Structure

```plaintext
CYBERGUARD-LLM/
├── app/                      # Streamlit web application
│   ├── assets/               # UI graphics and background assets
│   │   └── bg.jpg
│   ├── inference/            # Model loading & token streaming logic
│   │   ├── generator.py      # Prompt formatting and token generation
│   │   └── loader.py         # Engine & GGUF initialization
│   ├── prompts/              # System personas and prompt templates
│   ├── ui/                   # Custom CSS and UI layout modules
│   │   ├── components.py
│   │   └── style.py
│   └── app.py                # Main Streamlit application entry point
├── docs/                     # Architectural guides and research notes
├── evaluation/               # Evaluation scripts and benchmarks
├── experiments/              # Fine-tuning notebooks
│   └── cyberguard-llm-fine-tuning.ipynb
├── models/                   # Fine-tuned weights and GGUF checkpoints
│   ├── cyberguard-lora-v1/   # Trained QLoRA adapter weights
│   ├── merged_cyberguard/    # Merged base + LoRA model
│   └── cyberguard_f16.gguf   # Quantized GGUF model for local CPU inference
├── scripts/                  # Model utilities
│   ├── export_to_gguf.py     # Converts merged PyTorch models to GGUF format
│   └── merge_model.py        # Merges LoRA adapter with base model weights
├── training/                 # Data preprocessing pipeline
│   ├── dataset/
│   │   ├── processed/
│   │   ├── raw/
│   │   └── tokenized/
│   ├── config.py
│   └── dataset.py
├── .gitignore
├── PROJECT_PLAN.md
├── README.md
└── requirements.txt          # Global Python dependencies
```

## ⚙️ How CyberGuard LLM Works

### 1. Model Architecture
* **Base Model:** Meta Llama-3.2-3B-Instruct
* **Fine-Tuning Technique:** QLoRA (4-bit NF4 quantization + trainable LoRA adapters)
* **Libraries:** Hugging Face `transformers`, `peft`, `trl` (`SFTTrainer`), and `bitsandbytes`

During fine-tuning, the base 3B foundation model remains frozen in 4-bit precision while lightweight trainable adapter matrices are attached to target attention projection layers.

### 2. Fine-Tuning & Quantization Pipeline
* **Cloud Training (Kaggle):** The QLoRA training pipeline is executed inside a GPU-enabled Kaggle environment using the notebooks located in `experiments/`.
* **Adapter Export:** Trained LoRA adapter weights are saved to `models/cyberguard-lora-v1/`.
* **Model Merging:** `scripts/merge_model.py` combines the LoRA adapter back into the full-precision base Llama-3.2 weights (`models/merged_cyberguard/`).
* **GGUF Conversion:** `scripts/export_to_gguf.py` utilizes `llama.cpp` to convert the merged model into `models/cyberguard_f16.gguf` for fast, lightweight local CPU execution.

## 🚀 Step-by-Step Setup & Execution Guide

Follow these steps to run the application locally on your machine.

### Prerequisites
* **Python:** 3.10, 3.11, or 3.12 (Python 3.14 is currently unsupported by core PyTorch/Transformers dependencies).
* **Git & C++ Build Tools:** (CMake or GCC/Clang if compiling `llama.cpp` manually).

### Step 1: Clone the Repository
```bash
git clone [https://github.com/your-username/CYBERGUARD-LLM.git](https://github.com/your-username/CYBERGUARD-LLM.git)
cd CYBERGUARD-LLM
```

### Step 2: Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Prepare Model Weights
Ensure your GGUF model file or LoRA adapters are placed in the `models/` directory:
* Place your converted GGUF model at `models/cyberguard_f16.gguf`.
* **Optional:** If starting from raw LoRA weights, run the merge and export utilities:

```bash
python scripts/merge_model.py
python scripts/export_to_gguf.py
```

### Step 5: Launch the Streamlit Interface
Run the application from the root directory:

```bash
# Windows (PowerShell)
$env:PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"
streamlit run app/app.py

# Linux / macOS / Windows (CMD)
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
streamlit run app/app.py
```

Open `http://localhost:8501` in your web browser to interact with CyberGuard LLM.

## ⚠️ Current Limitations
* **CPU Performance Bottleneck:** Running 3B parameter model inference locally on entry-level hardware (e.g., Dual-Core / Core i3 CPUs) results in higher token generation latency compared to dedicated GPU systems.
* **Dataset Scale & Scope:** Fine-tuning was performed on a single, focused cybersecurity instruction dataset. Broader coverage requires expanding to multi-source datasets.
* **Training Steps:** Fine-tuning was executed for a limited number of training steps (due to Kaggle GPU time constraints) rather than reaching full loss convergence.
* **Non-Production Rating:** The model is an educational prototype and should not replace dedicated Security Operations Center (SOC) tooling or security audits.

## 🔮 Future Roadmap
* **RAG Integration:** Connect local cybersecurity knowledge bases and CVE databases using Retrieval-Augmented Generation.
* **Dataset Expansion:** Train on multi-turn SOC dialogue sets and real-world threat intelligence feeds.
* **Quantization Optimization:** Export to 4-bit GGUF (`Q4_K_M`) to drastically reduce CPU inference latency on budget hardware.

## License
This project is intended for educational and research purposes.
