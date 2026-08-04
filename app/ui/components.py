"""
app/ui/components.py

Render helpers for the CyberGuard LLM landing-page-to-chat UI: hero header,
compact pinned top bar, sidebar brand/status/benchmarks, and the GitHub
footer CTA.
"""

from typing import Dict, List, Literal, Optional

import streamlit as st

RiskLevel = Literal["low", "medium", "high"]


def render_hero(title: str, subtitle: str) -> None:
    """Render the centered hero header shown only on the empty-chat landing state.

    Args:
        title: Main title, e.g. "CyberGuard LLM 🛡️🤖".
        subtitle: One-line mission statement shown beneath the title.
    """
    st.markdown(
        f"""
        <div class="hero-wrap">
            <h1><span class="gradient-text">{title}</span></h1>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_top_bar(title: str) -> None:
    """Render the compact pinned title bar shown once the chat is active.

    Args:
        title: Short title text, e.g. "CyberGuard LLM 🛡️🤖".
    """
    st.markdown(
        f"""
        <div class="top-bar">
            <h3><span class="gradient-text">{title}</span></h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_landing_input(placeholder: str = "Ask your cybersecurity questions!!", key: str = "landing_form") -> Optional[str]:
    """Render the landing-page question input as a normal in-flow form.

    `st.chat_input` is always pinned to the fixed bottom of the viewport by
    Streamlit itself, which makes it impossible to vertically center
    alongside the hero title/subtitle/chips. This form-based input is a
    regular flow element instead, so it can live inside the same centered
    block as the rest of the landing content. Once the first message is
    sent, the app switches to the real `st.chat_input` for the active
    chat state (see app.py), which is the expected pinned-bottom behavior
    for an ongoing conversation.

    Args:
        placeholder: Placeholder text shown in the empty input.
        key: Unique Streamlit form key.

    Returns:
        The submitted question string, or None if the form wasn't submitted
        this run (or was submitted empty).
    """
    st.markdown('<div class="landing-input-row">', unsafe_allow_html=True)
    with st.form(key=key, clear_on_submit=True, border=False):
        col_input, col_submit = st.columns([6, 1])
        with col_input:
            question = st.text_input(
                label="Question",
                placeholder=placeholder,
                label_visibility="collapsed",
            )
        with col_submit:
            submitted = st.form_submit_button("→")
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted and question.strip():
        return question.strip()
    return None


def render_quick_prompt_chips(prompts: List[str], key_prefix: str = "chip") -> Optional[str]:
    """Render a row of pill-styled quick-prompt buttons.

    Args:
        prompts: List of prompt strings to show as clickable buttons.
        key_prefix: Unique key prefix to avoid Streamlit widget key collisions.

    Returns:
        The prompt string that was clicked this run, or None.
    """
    st.markdown('<div class="chip-row">', unsafe_allow_html=True)
    cols = st.columns(len(prompts))
    clicked: Optional[str] = None
    for col, prompt in zip(cols, prompts):
        with col:
            if st.button(prompt, key=f"{key_prefix}_{prompt}"):
                clicked = prompt
    st.markdown("</div>", unsafe_allow_html=True)
    return clicked


def render_sidebar_brand(app_name: str = "CyberGuard LLM", icon: str = "🛡️🤖") -> None:
    """Render the compact sidebar brand header with gradient app name text."""
    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="logo-row">
                <span class="icon">{icon}</span>
                <span class="name gradient-text">{app_name}</span>
            </div>
            <div class="tag">SOC CONSOLE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_widget(gpu_memory: str, latency_ms: str, lora_status: str = "Active") -> None:
    """Render the sidebar System Performance glass widget."""
    st.sidebar.markdown('<div class="sidebar-section-label">System Performance</div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        f"""
        <div class="glass-status">
            <div class="status-row">
                <span class="status-label">GPU Memory</span>
                <span class="status-value">{gpu_memory}</span>
            </div>
            <div class="status-row">
                <span class="status-label">Latency</span>
                <span class="status-value">{latency_ms}</span>
            </div>
            <div class="status-row">
                <span class="status-label">Adapter Status</span>
                <span class="status-value">{lora_status}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_benchmark_expander(metrics_by_model: Dict[str, Dict[str, float]]) -> None:
    """Render the collapsible sidebar 'Model Comparison & Benchmarks' section.

    Args:
        metrics_by_model: Dict keyed by model display name, each mapping a
            metric label to a 0-100 percentage value.
    """
    with st.sidebar.expander("📊 Model Comparison & Benchmarks"):
        for model_name, metrics in metrics_by_model.items():
            rows = ""
            for label, value in metrics.items():
                clamped = max(0.0, min(100.0, value))
                rows += f"""
                <div class="bench-row">
                    <span>{label}</span>
                    <span>{value:.0f}%</span>
                </div>
                <div class="bench-meter-track">
                    <div class="bench-meter-fill" style="width:{clamped}%;"></div>
                </div>
                """
            st.markdown(
                f"""
                <div class="bench-block">
                    <div class="bench-title">{model_name}</div>
                    {rows}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_sidebar_footer(
    repo_url: str = "https://github.com/your-username/CyberGuard-LLM",
    note: str = "Educational & Research Use Only",
) -> None:
    """Render the sidebar footer note and GitHub CTA button."""
    st.sidebar.markdown(f'<div class="sidebar-footer-note">{note}</div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        f"""
        <a href="{repo_url}" target="_blank" class="github-btn">
            ⭐ View Project on GitHub
        </a>
        """,
        unsafe_allow_html=True,
    )


def render_risk_badge(level: RiskLevel, label: Optional[str] = None) -> str:
    """Return HTML for a risk-level badge (caller renders it via st.markdown)."""
    colors = {"low": "#88D9E6", "medium": "#EE0E79", "high": "#ff6fa8"}
    icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(level, "⚪")
    color = colors.get(level, "#88D9E6")
    return (
        f'<span style="font-family:\'JetBrains Mono\',monospace; font-weight:700; '
        f'font-size:0.72rem; color:{color}; border:1px solid {color}; '
        f'padding:0.22rem 0.65rem; border-radius:6px;">{icon} {label or level.upper()}</span>'
    )