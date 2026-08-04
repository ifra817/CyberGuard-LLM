"""
app/app.py

Main Streamlit entry point for CyberGuard LLM. Renders a clutter-free hero
landing page until the first message is sent, then transitions seamlessly
into a pinned-top-bar, multi-turn chat interface.

Run with (from the repo root):
    streamlit run app/app.py
"""
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

from inference.generator import (
    ModelVariant,
    estimate_gpu_memory_gb,
    estimate_latency_ms,
    get_benchmark_metrics,
    load_model,
    stream_response,
)
from ui.components import (
    render_benchmark_expander,
    render_hero,
    render_landing_input,
    render_quick_prompt_chips,
    render_sidebar_brand,
    render_sidebar_footer,
    render_status_widget,
    render_top_bar,
)
from ui.style import inject_custom_css, inject_landing_layout_css

# --------------------------------------------------------------------------
# Page Config & Theme
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="CyberGuard LLM",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded",
)
inject_custom_css()

APP_TITLE = "CyberGuard LLM 🛡️🤖"
APP_NAME = "CyberGuard LLM"
APP_SUBTITLE = "AI-Powered Cybersecurity Incident Triage & Educational Assistant"
QUICK_PROMPTS = [
    "Explain phishing mechanics",
    "How does MFA bypass work?",
    "Password hashing standards",
]
GITHUB_REPO_URL = "https://github.com/ifra817/CyberGuard-LLM"


# --------------------------------------------------------------------------
# Session State
# --------------------------------------------------------------------------
def init_session_state() -> None:
    """Initialize all Streamlit session_state keys used across the app."""
    defaults = {
        "model_variant": ModelVariant.FINE_TUNED,
        "messages": [],  # list[dict]: {"role": "user"/"assistant", "content": str}
        "last_latency_ms": 187.0,
        "last_gpu_mem_gb": 11.2,
        "pending_prompt": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# --------------------------------------------------------------------------
# Sidebar (always visible, uncluttered)
# --------------------------------------------------------------------------
def render_sidebar() -> None:
    """Render the sidebar: brand, model toggle, status widget, benchmarks, footer."""
    render_sidebar_brand(APP_NAME)

    st.sidebar.markdown('<div class="sidebar-section-label">Model</div>', unsafe_allow_html=True)
    variant_label = st.sidebar.radio(
        label="Active inference model",
        options=[ModelVariant.FINE_TUNED.value, ModelVariant.BASE.value],
        index=0 if st.session_state["model_variant"] == ModelVariant.FINE_TUNED else 1,
        label_visibility="collapsed",
    )
    st.session_state["model_variant"] = (
        ModelVariant.FINE_TUNED if variant_label == ModelVariant.FINE_TUNED.value else ModelVariant.BASE
    )

    handle = load_model(st.session_state["model_variant"])

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    render_status_widget(
        gpu_memory=f"{st.session_state['last_gpu_mem_gb']:.1f} GB",
        latency_ms=f"{st.session_state['last_latency_ms']:.0f} ms",
        lora_status="Active" if handle.lora_active else "Inactive",
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    render_benchmark_expander(get_benchmark_metrics())

    # Push footer toward the bottom of the sidebar.
    st.sidebar.markdown("<div style='margin-top:auto; padding-top:2rem;'></div>", unsafe_allow_html=True)
    render_sidebar_footer(repo_url=GITHUB_REPO_URL)


render_sidebar()


# --------------------------------------------------------------------------
# Response handling (shared by both states)
# --------------------------------------------------------------------------
def handle_new_prompt(prompt: str) -> None:
    """Append the user prompt, stream the assistant reply, and update state."""
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Pass session messages so generator receives multi-turn history
        full_reply = st.write_stream(
            stream_response(st.session_state["messages"], st.session_state["model_variant"])
        )

    st.session_state["messages"].append({"role": "assistant", "content": full_reply})
    st.session_state["last_latency_ms"] = estimate_latency_ms(st.session_state["model_variant"])
    st.session_state["last_gpu_mem_gb"] = estimate_gpu_memory_gb()


# --------------------------------------------------------------------------
# Main Area: State 1 (Landing) vs State 2 (Active Chat)
# --------------------------------------------------------------------------
has_messages = len(st.session_state["messages"]) > 0

if not has_messages:
    # ---- State 1: Centered hero landing page -------------------------
    inject_landing_layout_css()

    render_hero(title=APP_TITLE, subtitle=APP_SUBTITLE)
    clicked_prompt = render_quick_prompt_chips(QUICK_PROMPTS, key_prefix="landing")
    typed_prompt = render_landing_input(placeholder="Ask your cybersecurity questions!!")

    effective_prompt = clicked_prompt or typed_prompt
    if effective_prompt:
        handle_new_prompt(effective_prompt)
        st.rerun()

else:
    # ---- State 2: Compact top bar + active chat stream -----------------
    render_top_bar(APP_TITLE)

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    chat_prompt = st.chat_input("Ask your cybersecurity questions!!")
    if chat_prompt:
        handle_new_prompt(chat_prompt)
        st.rerun()