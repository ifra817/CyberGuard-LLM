# PROJECT_PLAN.md

# CyberGuard LLM — Project Development Plan

## Project Vision
CyberGuard LLM is a hands-on AI engineering project focused on learning the complete lifecycle of adapting an open-weight Large Language Model to a specialized domain through fine-tuning.
Rather than relying on proprietary AI APIs, this project explores how a foundation model (Meta Llama 3) can be transformed into a cybersecurity-focused assistant capable of reasoning about user-reported incidents, explaining cybersecurity concepts, and providing structured educational guidance.
The primary objective is not simply to produce a working chatbot, but to deeply understand the engineering decisions behind modern LLM development.

## Project Goals
By the completion of this project, I aim to understand:
* How transformer-based LLMs operate
* The architecture of Meta Llama 3
* Instruction tuning and supervised fine-tuning
* Dataset engineering and preprocessing
* Parameter-Efficient Fine-Tuning (PEFT)
* LoRA and QLoRA
* Model evaluation and benchmarking
* Deployment of a fine-tuned language model
* End-to-end AI application development

## Development Philosophy
This project follows a research-oriented workflow rather than a tutorial-driven approach.
The objective is to independently study official documentation, understand each engineering decision, and implement the system from first principles wherever possible.
Throughout development, emphasis will be placed on understanding why each technique is used rather than simply learning how to implement it.

## Project Scope

### Included
* Domain-specific fine-tuning using Meta Llama 3
* Custom cybersecurity instruction dataset
* Cybersecurity question answering
* User incident reasoning
* Educational security guidance
* Secure coding assistance
* Lightweight Streamlit interface
* Model evaluation against the base model
* Documentation of the complete learning process

### Excluded (Version 1)
The first version intentionally excludes:
* User authentication
* Databases
* Conversation history
* File uploads
* Malware scanning
* Network traffic analysis
* CVE database integration
* Automated vulnerability scanning
* Retrieval-Augmented Generation (RAG)
* Agentic workflows
* External API integrations

These features may be explored in future iterations after the core fine-tuning workflow has been mastered.

## Functional Requirements
The assistant should be able to:

### 1. Explain Cybersecurity Concepts
Examples include:
* Malware
* Ransomware
* Phishing
* Password Security
* MFA
* SQL Injection
* XSS
* Firewalls
* VPNs
* Network Security
* Secure Coding

### 2. Analyze User Incidents
Given a description of a cybersecurity problem, the model should:
* summarize the issue
* identify possible causes
* explain why the issue may be occurring
* recommend immediate actions
* recommend preventive measures
* communicate uncertainty when evidence is insufficient

### 3. Review Code Snippets
When a user provides code, the assistant should:
* identify suspicious patterns
* explain why certain code deserves attention
* highlight risky APIs or behaviors
* discuss potential security implications
* request additional files or context when required
* avoid unsupported claims

### 4. Educational Guidance
The assistant should prioritize:
* teaching
* explanation
* defensive security
* beginner-friendly language

It should avoid presenting uncertain conclusions as facts.

## Non-Functional Requirements
The project should emphasize:
* Maintainability
* Modularity
* Reproducibility
* Clear documentation
* Lightweight deployment
* Easy experimentation

## Learning Roadmap
The project will be completed in several stages.

### Phase 1 — Research & Foundations
* Study Llama 3 architecture, tokenization limits, and chat templates.
* Deep dive into PEFT methodology (LoRA matrix decomposition, $r$ and $\alpha$ parameter scaling).
* Define hyperparameter research plan.
* **Deliverables:** `docs/RESEARCH_NOTES.md`, environment setup scripts.

### Phase 2 — Dataset Engineering
* Design instruction-response schema (JSONL / Hugging Face Dataset).
* Draft curated seed examples across concept, incident, and code scenarios.
* Run validation scripts for formatting, token lengths, and data balance.
* **Deliverables:** `DATASET_PLAN.md`, train/validation dataset splits.

### Phase 3 — Fine-Tuning Pipeline
* Setup Hugging Face SFTTrainer with PEFT / bitsandbytes (QLoRA config).
* Train LoRA adapters on target linear modules (q_proj, v_proj, etc.).
* Monitor loss curves and manage memory constraints.
* **Deliverables:** Model checkpoints, saved LoRA adapter weights, `training/train.py`.

### Phase 4 — Evaluation & Benchmarking
* Perform qualitative comparison: Base Model vs. Fine-Tuned Model on unseen test prompts.
* Analyze loss metrics, output structure adherence, and hallucination rates.
* **Deliverables:** `docs/EVALUATION_REPORT.md` with side-by-side prompt responses.

### Phase 5 — Application Interface
* Build local Streamlit interface for interactive model testing.
* Implement inference pipeline loading base weights + adapter weights.
* **Deliverables:** `app/app.py`, interactive demo.

### Phase 6 — Final Documentation
* Synthesize all learning notes, failure cases, and architecture decisions into the final repository logs.
* **Deliverables:** Final `README.md`, updated `LEARNING_LOG.md`.

## Engineering Decisions
During development, every major technical decision should be documented.
Examples include:
* Why Llama 3 was selected
* Why PEFT was chosen
* Why LoRA instead of full fine-tuning
* Choice of model size
* Dataset formatting decisions
* Prompt template design
* Evaluation methodology

Each decision should include:
* Problem
* Available Options
* Final Decision
* Rationale
* Trade-offs

## 🚨 Risk Analysis & Mitigation Strategy

| Risk Scenario | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **GPU Out-Of-Memory (OOM)** | High | Use 4-bit quantization (QLoRA), gradient accumulation, and reduced batch sizes (per_device_train_batch_size=1 or 2). |
| **Dataset Overfitting / Memorization** | High | Keep adapter rank ($r$) modest (e.g., $r=8$ or $r=16$), apply dropout, and monitor validation loss closely. |
| **Model Hallucinations** | Medium | Explicitly include "uncertainty response" instruction pairs in the training dataset when context is missing. |
| **Malformed Formatting** | Medium | Standardize all dataset entries using Llama 3's official system/user/assistant prompt formatting syntax. |

## 📊 Success Criteria
The project will be deemed successful when:
* **Pipeline Execution:** The LoRA fine-tuning script trains to completion reproducibly.
* **Domain Improvement:** The fine-tuned adapter shows noticeably higher structure, accuracy, and domain clarity on security prompts compared to base Llama 3.
* **Reasoning Quality:** The model reliably provides structured triage (Cause -> Explanation -> Action -> Prevention) for user scenarios.
* **Engineering Artifacts:** Complete documentation in LEARNING_LOG.md explaining the why behind every major technical choice.

## Risks
Potential challenges include:
* Limited GPU memory
* Small dataset size
* Overfitting
* Poor instruction formatting
* Hallucinated responses
* Long training times
* Hyperparameter tuning

Each challenge should be documented along with the solution adopted.

## Future Roadmap
Possible future extensions include:
* Retrieval-Augmented Generation (RAG)
* CVE database integration
* Threat intelligence feeds
* Security report generation
* File and log analysis
* PDF security analysis
* Memory-enabled conversations
* Multi-turn incident investigations
* Deployment on Hugging Face Spaces
* Model benchmarking against additional open-weight LLMs

## Personal Learning Outcomes
Beyond building an application, this project aims to develop practical AI engineering skills.
By the end of this project, I should be able to confidently explain:
* How LLM fine-tuning works
* Why LoRA and PEFT are widely used
* How instruction datasets are constructed
* The complete training pipeline for an open-weight LLM
* The trade-offs involved in adapting foundation models
* How to evaluate whether fine-tuning was successful

The ultimate goal is not only to build CyberGuard LLM, but to become capable of independently designing, training, evaluating, and deploying future domain-specific language models.