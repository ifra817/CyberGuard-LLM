# CyberGuard LLM 🛡️🤖
> **An AI-Powered Cybersecurity Incident Analysis & Educational Assistant**

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Model](https://img.shields.io/badge/base__model-Llama%203-orange)
![Status](https://img.shields.io/badge/status-In%20Development-yellow)

---

## 📌 Project Overview

**CyberGuard LLM** is a personal, hands-on learning project dedicated to understanding the complete end-to-end process of fine-tuning Large Language Models (LLMs). 

Rather than building a general-purpose chatbot, this project focuses on domain adaptation: fine-tuning Meta's **Llama 3** model on a custom-designed cybersecurity instruction dataset. The resulting assistant is designed to reason about security concepts, analyze user-described security incidents, review suspicious code snippets, and provide clear, beginner-friendly educational guidance.

---

## 🎯 Objectives & Learning Goals

This project was created as a deep dive into open-weight LLMs and domain-specific instruction tuning.

### Primary Objectives
- **End-to-End Fine-Tuning Workflow:** Learn the entire lifecycle from raw dataset design and tokenization to model training, evaluation, and UI integration.
- **Custom Dataset Engineering:** Build a high-quality, structured instruction-following dataset tailored to cybersecurity incident triage.
- **PEFT / LoRA Implementation:** Train efficiently using Parameter-Efficient Fine-Tuning techniques to adapt Llama 3 on consumer hardware.
- **Comparative Evaluation:** Quantitative and qualitative assessment comparing the base Llama 3 model against the fine-tuned checkpoint.

### Technical Skill Areas
- **Architectures:** Transformer-based LLMs, Causal LM training dynamics.
- **Frameworks:** Hugging Face Ecosystem (`transformers`, `datasets`, `peft`, `trl`), PyTorch.
- **Interface & Deployment:** Streamlit interface for local execution and multi-turn interaction.

---

## ✨ Key Features

### 1. Cybersecurity Knowledge Base
Answers fundamental security queries with clear, structured explanations covering:
- Phishing & Social Engineering
- Malware, Ransomware, & Trojan mechanics
- Password Security & Multi-Factor Authentication (MFA)
- Basic Network & Web Application Security
- Secure Coding Practices

### 2. Guided Incident Analysis
Analyzes user-submitted incidents (e.g., suspicious emails, unexpected pop-ups, compromised account symptoms) by providing:
- **Possible Causes:** What might actually be happening behind the scenes.
- **Risk Indicator:** Why the behavior is suspicious.
- **Immediate Action Steps:** Prioritized mitigation steps for non-technical users.
- **Prevention Strategies:** How to avoid similar incidents in the future.

### 3. Code Security Review
Inspects provided code snippets to:
- Identify potentially risky functions or patterns (e.g., unvalidated inputs, hardcoded secrets).
- Highlight areas that warrant further inspection or sandbox testing.
- Communicate uncertainty when missing required context or external dependencies.

---

## 🛠️ Tech Stack

| Category | Tools & Libraries |
| :--- | :--- |
| **Base Model** | Meta Llama 3 |
| **Core ML Framework** | PyTorch, Hugging Face `transformers` |
| **Fine-Tuning & Datasets** | Hugging Face `peft`, `trl` (SFTTrainer), `datasets` |
| **Frontend / Web App** | Streamlit |
| **Language** | Python 3.10+ |

---

## 📁 Repository Structure

```text
CyberGuard-LLM/
├── app/                  # Streamlit web application & user interface
├── training/             # Data preprocessing, tokenization, & fine-tuning scripts
├── evaluation/           # Model benchmarking & comparative evaluation scripts
├── models/               # Checkpoints and adapter weights (git-ignored)
├── docs/                 # Extended documentation and research notes
├── assets/               # Visual assets, screenshots, and diagrams
├── README.md             # Project main overview
├── PROJECT_PLAN.md       # Detailed technical milestone roadmap
├── DATASET_PLAN.md       # Dataset schema, instruction formats, and sources
```

## License
This project is intended for educational and research purposes.
