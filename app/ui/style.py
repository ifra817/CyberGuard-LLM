"""
app/ui/style.py

Custom CSS theme for CyberGuard LLM's landing-page-to-chat UI.
Loads the local `bg.jpg` background image as a Base64 data URI so the app
has no dependency on an external image host.

Usage:
    from app.ui.style import inject_custom_css
    inject_custom_css()
"""

import base64
from pathlib import Path

import streamlit as st

COLORS = {
    "midnight_navy": "#0B132B",
    "dark_teal": "#0A5265",
    "burgundy": "#6B0032",
    "neon_pink": "#EE0E79",
    "ice_cyan": "#88D9E6",
    "slate_light": "#E2E8F0",
}

# app/ui/style.py -> app/assets/bg.jpg
BACKGROUND_IMAGE_PATH = Path(__file__).resolve().parent.parent / "assets" / "bg.jpg"


def _get_base64_image(image_path: Path) -> str:
    """Read a local image file and return it as a Base64 data URI string.

    Args:
        image_path: Path to the local image file (e.g. `app/assets/bg.jpg`).

    Returns:
        A `data:image/<ext>;base64,...` string ready to drop into a CSS
        `background-image: url(...)` declaration. Returns an empty string
        if the file can't be found, so the app degrades gracefully to a
        plain dark background instead of crashing.
    """
    try:
        image_bytes = image_path.read_bytes()
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        suffix = image_path.suffix.lstrip(".").lower()
        mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix
        return f"data:image/{mime};base64,{encoded}"
    except FileNotFoundError:
        return ""


def inject_landing_layout_css() -> None:
    """Inject the landing-only vertical-centering rule for `.block-container`.

    Widgets rendered by Streamlit (hero markdown, quick-prompt chips, the
    landing input form) all live as direct children of `.block-container`,
    so turning that container into a centered flex column groups them
    together in the middle ~65% of the viewport. Call this ONLY while on
    the landing screen (`len(st.session_state.messages) == 0`) — its mere
    presence in the DOM is what toggles the layout, so simply not calling
    it once a chat is active restores normal top-aligned scrolling.
    """
    st.markdown(
        """
        <style>
        .block-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 65vh;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_custom_css() -> None:
    """Inject the full CyberGuard LLM CSS theme. Call once, immediately
    after `st.set_page_config(...)` in app.py."""
    bg_data_uri = _get_base64_image(BACKGROUND_IMAGE_PATH)
    # 1. Darken overlay opacity from 0.60 -> 0.88 / 0.92 to heavily dim the background image
    bg_declaration = (
        f"linear-gradient(rgba(11, 19, 43, 0.88), rgba(11, 19, 43, 0.92)), "
        f"url('{bg_data_uri}') no-repeat center center fixed"
        if bg_data_uri
        else "linear-gradient(rgba(11, 19, 43, 1), rgba(11, 19, 43, 1))"
    )

    css = f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');

    :root {{
        --navy: {COLORS['midnight_navy']};
        --teal: {COLORS['dark_teal']};
        --burgundy: {COLORS['burgundy']};
        --pink: {COLORS['neon_pink']};
        --cyan: {COLORS['ice_cyan']};
        --text: {COLORS['slate_light']};
    }}

    /* ============================================================ */
    /* Background — local image + dark overlay, blends into sidebar  */
    /* ============================================================ */
    html, body {{
        margin: 0;
        padding: 0;
        height: 100%;
    }}
     .stApp {{
        background: {bg_declaration} !important;
        background-size: cover !important;
        background-color: var(--navy) !important;
        min-height: 100vh;
        width: 100%;
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }}


    /* Streamlit wraps content in inner app-view / bottom containers that
       otherwise paint their own opaque background over ours. Force them
       transparent so the full-bleed image shows through everywhere,
       including behind the fixed chat-input bar. */
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"],
    [data-testid="stChatFloatingInputContainer"],
    div[data-testid="stBottom"] > div,
    div[class*="stBottom"],
    .stChatInputContainer {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    #MainMenu, footer {{
        visibility: hidden;
        height: 0;
    }}

    /* Keep the header container itself transparent instead of hiding it —
       hiding it with display:none/visibility:hidden also removes the
       sidebar collapse/expand toggle that lives inside it. */
    [data-testid="stHeader"] {{
        background: transparent !important;
        z-index: 99999 !important;
    }}

    /* ============================================================ */
    /* Sidebar re-open control — Streamlit hardcodes this button to  */
    /* a fixed 32x32px box with overflow:hidden, which clips any      */
    /* ::after label content. Explicitly unclip it before applying   */
    /* the pill/label styling.                                        */
    /* ============================================================ */
    [data-testid="collapsedControl"],
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapseButton"] button {{
        width: auto !important;
        height: auto !important;
        min-width: unset !important;
        min-height: unset !important;
        max-width: unset !important;
        max-height: unset !important;
        overflow: visible !important;
        position: fixed !important;
        top: 1rem !important;
        left: 1rem !important;
        z-index: 100000 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        background: rgba(11, 19, 43, 0.92) !important;
        border: 1px solid rgba(238, 14, 121, 0.5) !important;
        border-radius: 20px !important;
        padding: 6px 14px !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 0 14px rgba(238, 14, 121, 0.35) !important;
        cursor: pointer !important;
    }}

    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] button svg {{
        fill: var(--pink) !important;
        color: var(--pink) !important;
        width: 16px !important;
        height: 16px !important;
        flex-shrink: 0 !important;
    }}

    [data-testid="collapsedControl"]::after,
    [data-testid="collapsedControl"] button::after {{
        content: "View Metrics & SOC Console" !important;
        color: var(--cyan) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
        display: inline-block !important;
        line-height: 1 !important;
    }}

    [data-testid="collapsedControl"]:hover,
    [data-testid="collapsedControl"] button:hover {{
        border-color: var(--cyan) !important;
        box-shadow: 0 0 16px rgba(136, 217, 230, 0.5) !important;
    }}

    .block-container {{
        padding-top: 3rem;
        padding-bottom: 6rem;
        max-width: 780px;
    }}

    /* ============================================================ */
    /* Typography                                                     */
    /* ============================================================ */
    h1, h2, h3, h4, h5 {{
        font-family: 'Space Grotesk', sans-serif;
        color: var(--text);
        font-weight: 700;
    }}

    p, span, li, label {{
        color: var(--text);
        line-height: 1.6;
    }}

    code {{
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--cyan) !important;
        background: rgba(136, 217, 230, 0.08) !important;
    }}

    a {{ color: var(--pink) !important; }}

    hr {{ border-color: rgba(136, 217, 230, 0.14); margin: 1.25rem 0; }}

    .gradient-text {{
        background: linear-gradient(90deg, var(--cyan), var(--pink));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    /* ============================================================ */
    /* Hero landing section (State 1: no messages yet)                */
    /* ============================================================ */
    .hero-wrap {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 1.5rem;
        width: 100%;
    }}

    .hero-wrap h1 {{
        font-size: 2.6rem;
        margin: 0 0 0.6rem 0;
    }}

    .hero-wrap .hero-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: var(--cyan);
        opacity: 0.85;
        font-weight: 400;
        max-width: 480px;
        margin: 0 auto 2rem auto;
    }}

    /* ============================================================ */
    /* Compact pinned top bar (State 2: active chat)                  */
    /* ============================================================ */
    .top-bar {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.25rem 0 1.5rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(136, 217, 230, 0.12);
    }}

    .top-bar h3 {{
        margin: 0;
        font-size: 1.25rem;
    }}

    /* ============================================================ */
    /* Quick-prompt pill buttons                                       */
    /* ============================================================ */
    .chip-row {{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: 2rem;
    }}

    .chip-row .stButton > button {{
        background: rgba(136, 217, 230, 0.06);
        color: var(--cyan);
        border: 1px solid rgba(136, 217, 230, 0.3);
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 500;
        padding: 0.45rem 1.1rem;
        box-shadow: none;
        backdrop-filter: blur(6px);
        width: 100%;
    }}

    .chip-row .stButton > button:hover {{
        border-color: var(--pink);
        color: var(--pink);
        box-shadow: 0 0 10px rgba(238, 14, 121, 0.25);
        transform: none;
    }}

    /* ============================================================ */
    /* Sidebar                                                         */
    /* ============================================================ */
    section[data-testid="stSidebar"] {{
        background: var(--navy);
        border-right: 1px solid rgba(136, 217, 230, 0.10);
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding-top: 2rem;
        padding-left: 1.25rem;
        padding-right: 1.25rem;
        display: flex;
        flex-direction: column;
        min-height: 96vh;
    }}

    .sidebar-brand {{
        padding-bottom: 1.25rem;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid rgba(136, 217, 230, 0.10);
    }}

    .sidebar-brand .logo-row {{
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.2rem;
    }}

    .sidebar-brand .logo-row .icon {{ font-size: 1.35rem; }}

    .sidebar-brand .logo-row .name {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.0rem;
    }}

    .sidebar-brand .tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        color: var(--pink);
        letter-spacing: 1.1px;
        opacity: 0.85;
    }}

    .sidebar-section-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: var(--cyan);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.6rem;
        opacity: 0.9;
    }}

    /* Glassmorphic sidebar widgets */
    .glass-status {{
        background: rgba(136, 217, 230, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(136, 217, 230, 0.16);
        border-radius: 10px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
        padding: 1rem 1.1rem;
    }}

    .status-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.4rem 0;
    }}

    .status-row + .status-row {{
        border-top: 1px solid rgba(136, 217, 230, 0.08);
    }}

    .status-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        color: var(--cyan);
        opacity: 0.85;
    }}

    .status-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: var(--text);
        font-weight: 500;
    }}

    /* Benchmark rows inside sidebar expander */
    .bench-block {{ margin-bottom: 1rem; }}

    .bench-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        color: var(--text);
    }}

    .bench-row {{
        display: flex;
        justify-content: space-between;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--cyan);
        margin-bottom: 0.3rem;
    }}

    .bench-meter-track {{
        width: 100%;
        height: 5px;
        border-radius: 999px;
        background: rgba(136, 217, 230, 0.12);
        overflow: hidden;
        margin-bottom: 0.6rem;
    }}

    .bench-meter-fill {{
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--cyan), var(--pink));
    }}

    /* Sidebar footer */
    .sidebar-footer-note {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: var(--text);
        opacity: 0.55;
        text-align: center;
        margin-bottom: 0.9rem;
    }}

    .github-btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        width: 100%;
        padding: 0.6rem 0;
        border-radius: 8px;
        border: none;
        background: linear-gradient(135deg, var(--pink) 0%, var(--burgundy) 100%);
        color: white !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 0.82rem;
        text-decoration: none !important;
        box-shadow: 0 0 12px rgba(238, 14, 121, 0.35);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }}

    .github-btn:hover {{
        box-shadow: 0 0 20px rgba(238, 14, 121, 0.6);
        transform: translateY(-1px);
        color: white !important;
    }}

    /* ============================================================ */
    /* Buttons (general)                                              */
    /* ============================================================ */
    .stButton > button, .stFormSubmitButton > button {{
        background: linear-gradient(135deg, var(--pink) 0%, var(--burgundy) 100%);
        color: white;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 0.86rem;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.4rem;
        box-shadow: 0 0 10px rgba(238, 14, 121, 0.35);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }}

    .stButton > button:hover, .stFormSubmitButton > button:hover {{
        box-shadow: 0 0 18px rgba(238, 14, 121, 0.6);
        transform: translateY(-1px);
    }}

    /* ============================================================ */
    /* Inputs & chat                                                   */
    /* ============================================================ */
    .stTextInput input {{
        background-color: rgba(11, 19, 43, 0.55) !important;
        backdrop-filter: blur(8px);
        color: var(--text) !important;
        border: 1px solid rgba(136, 217, 230, 0.22) !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.85rem !important;
    }}

    .stTextInput input:focus {{
        border-color: var(--pink) !important;
        box-shadow: 0 0 0 1px rgba(238, 14, 121, 0.35) !important;
    }}

    div[role="radiogroup"] label {{ color: var(--text) !important; }}

    /* Landing-page input form: compact send button sitting flush beside
       the text field, and a transparent form wrapper (no dark panel). */
    .landing-input-row [data-testid="stForm"] {{
        background: transparent;
        border: none;
        padding: 0;
    }}

    .landing-input-row .stButton > button,
    .landing-input-row .stFormSubmitButton > button {{
        padding: 0.7rem 1.1rem;
        margin-top: 0;
    }}

    /* ============================================================ */
    /* Chat input — the OUTER wrapper is the single pill capsule;     */
    /* the textarea and send button sit seamlessly inside it rather   */
    /* than each having their own separate boxed styling.              */
    /* ============================================================ */
    div[data-testid="stChatInput"] {{
        background: rgba(11, 19, 43, 0.80) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(136, 217, 230, 0.3) !important;
        border-radius: 16px !important;
        padding: 6px 14px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }}

    div[data-testid="stChatInput"]:focus-within {{
        border-color: var(--pink) !important;
        box-shadow: 0 0 15px rgba(238, 14, 121, 0.4) !important;
    }}

    /* Inner textarea becomes background-less so it blends into the
       outer capsule instead of forming its own inner box. */
    [data-testid="stChatInput"] textarea,
    .stChatInput textarea {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 8px 4px !important;
        min-height: 48px !important;
        color: var(--text) !important;
        font-size: 1rem !important;
    }}

    /* Send button sits cleanly inside the right edge of the capsule. */
    [data-testid="stChatInput"] button[data-testid="stChatInputSubmitButton"],
    [data-testid="stChatInput"] button {{
        background: linear-gradient(135deg, var(--pink) 0%, var(--burgundy) 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 10px rgba(238, 14, 121, 0.35) !important;
        align-self: center !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}

    [data-testid="stChatInput"] button:hover {{
        box-shadow: 0 0 16px rgba(238, 14, 121, 0.6) !important;
        transform: scale(1.05) !important;
    }}

     /* 2. Make message bubbles more opaque and increase blur to protect text readability */
    div[data-testid="stChatMessage"] {{
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        backdrop-filter: blur(12px) !important;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.7rem;
        max-width: 85%;
    }}

    /* User bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {{
        flex-direction: row-reverse;
        margin-left: auto;
        margin-right: 0;
        background: rgba(238, 14, 121, 0.25) !important;
        border: 1px solid rgba(238, 14, 121, 0.45) !important;
    }}

    /* Assistant bubble: Raised opacity from 0.35 -> 0.85 */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {{
        flex-direction: row;
        margin-right: auto;
        margin-left: 0;
        background: rgba(11, 19, 43, 0.85) !important;
        border: 1px solid rgba(136, 217, 230, 0.3) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--teal); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--pink); }}

     /* 2. Make message bubbles more opaque and increase blur to protect text readability */
    div[data-testid="stChatMessage"] {{
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        backdrop-filter: blur(12px) !important;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.7rem;
        max-width: 85%;
    }}

    /* User bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {{
        flex-direction: row-reverse;
        margin-left: auto;
        margin-right: 0;
        background: rgba(238, 14, 121, 0.25) !important;
        border: 1px solid rgba(238, 14, 121, 0.45) !important;
    }}

    /* Assistant bubble: Raised opacity from 0.35 -> 0.85 */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {{
        flex-direction: row;
        margin-right: auto;
        margin-left: 0;
        background: rgba(11, 19, 43, 0.85) !important;
        border: 1px solid rgba(136, 217, 230, 0.3) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)