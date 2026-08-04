"""
app/inference/loader.py

Model Loader module for CyberGuard LLM using llama.cpp GGUF.
"""

import os
import streamlit as st
from llama_cpp import Llama

GGUF_MODEL_PATH = os.path.join("models", "cyberguard_f16.gguf")

@st.cache_resource
def load_cyberguard_engine() -> Llama:
    """Loads the C++ optimized GGUF engine into memory.
    
    Uses 4 CPU threads to maximize speed without freezing the OS.
    """
    with st.spinner("Loading CyberGuard GGUF Engine..."):
        llm = Llama(
            model_path=GGUF_MODEL_PATH,
            n_ctx=2048,
            n_threads=4,
            verbose=False
        )
    return llm