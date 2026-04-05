"""Premium dark-mode theme for RepoRover Streamlit UI."""
from __future__ import annotations

import streamlit as st


def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
        /* ── Imports ─────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        /* ── Root variables ──────────────────────────────── */
        :root {
            --bg-primary: #0a0e1a;
            --bg-secondary: #111827;
            --bg-card: rgba(17, 24, 39, 0.7);
            --bg-card-hover: rgba(31, 41, 55, 0.8);
            --border-subtle: rgba(99, 102, 241, 0.15);
            --border-glow: rgba(99, 102, 241, 0.4);
            --accent-primary: #6366f1;
            --accent-secondary: #818cf8;
            --accent-cyan: #22d3ee;
            --accent-emerald: #34d399;
            --accent-amber: #fbbf24;
            --accent-rose: #fb7185;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            --gradient-cyan: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
            --gradient-success: linear-gradient(135deg, #059669 0%, #34d399 100%);
            --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.15);
            --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.3);
            --radius: 12px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* ── Global overrides ────────────────────────────── */
        .stApp {
            background: var(--bg-primary) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f1629 0%, #0a0e1a 100%) !important;
            border-right: 1px solid var(--border-subtle) !important;
        }
        /* Sidebar Navigation Menu (styled st.radio) */
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
            gap: 0.25rem !important;
        }

        /* The clickable nav item container */
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
            background-color: transparent !important;
            border-radius: 8px !important;
            padding: 0.6rem 0.75rem !important;
            margin-bottom: 0.3rem !important;
            cursor: pointer !important;
            transition: all 0.2s ease-in-out !important;
            border-left: 3px solid transparent !important;
        }

        /* Nav item text */
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label div[data-testid="stMarkdownContainer"] p {
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            color: var(--text-secondary) !important;
            font-family: 'Inter', sans-serif !important;
            margin: 0 !important;
        }

        /* Hover effect */
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
            background-color: rgba(255, 255, 255, 0.05) !important;
        }
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover div[data-testid="stMarkdownContainer"] p {
            color: var(--text-primary) !important;
        }

        /* Active/Selected State */
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(90deg, rgba(99, 102, 241, 0.15), transparent) !important;
            border-left: 3px solid var(--accent-primary) !important;
            border-radius: 0 8px 8px 0 !important;
        }
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) div[data-testid="stMarkdownContainer"] p {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
        }

        /* Hide the native radio circles */
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }

        /* Hide default Streamlit sidebar navigation */
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Headers */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }
        h1 { color: var(--text-primary) !important; }
        h2 { color: var(--text-primary) !important; }
        h3 { color: var(--text-secondary) !important; }

        /* Inputs */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif !important;
            transition: var(--transition) !important;
        }
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: var(--shadow-glow) !important;
        }

        /* Buttons */
        .stButton > button {
            background: var(--gradient-primary) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.5rem !important;
            transition: var(--transition) !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
        }
        .stButton > button:active {
            transform: translateY(0px) !important;
        }

        /* Success / Error / Info boxes */
        .stAlert {
            border-radius: var(--radius) !important;
            border: 1px solid var(--border-subtle) !important;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius) !important;
            padding: 1rem !important;
            backdrop-filter: blur(10px) !important;
            transition: var(--transition) !important;
        }
        div[data-testid="stMetric"]:hover {
            border-color: var(--border-glow) !important;
            box-shadow: var(--shadow-glow) !important;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
        }

        /* Code blocks */
        code, .stCodeBlock {
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px !important;
        }
        .stTabs [data-baseweb="tab"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: var(--radius) !important;
            color: var(--text-secondary) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            transition: var(--transition) !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            border-color: var(--accent-primary) !important;
            color: var(--text-primary) !important;
        }
        .stTabs [aria-selected="true"] {
            background: var(--gradient-primary) !important;
            color: white !important;
            border-color: transparent !important;
        }

        /* Divider */
        hr {
            border-color: var(--border-subtle) !important;
        }

        /* Custom card component */
        .rover-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius);
            padding: 1.5rem;
            backdrop-filter: blur(10px);
            transition: var(--transition);
            margin-bottom: 1rem;
        }
        .rover-card:hover {
            border-color: var(--border-glow);
            box-shadow: var(--shadow-glow);
            transform: translateY(-2px);
        }

        /* Gradient text */
        .gradient-text {
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
        }

        /* Status badge */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
        }
        .status-online {
            background: rgba(52, 211, 153, 0.15);
            color: #34d399;
            border: 1px solid rgba(52, 211, 153, 0.3);
        }
        .status-offline {
            background: rgba(251, 113, 133, 0.15);
            color: #fb7185;
            border: 1px solid rgba(251, 113, 133, 0.3);
        }

        /* Chat message styling */
        .chat-user {
            background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.1));
            border: 1px solid rgba(99,102,241,0.2);
            border-radius: 16px 16px 4px 16px;
            padding: 1rem 1.25rem;
            margin: 0.5rem 0;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }
        .chat-assistant {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 16px 16px 16px 4px;
            padding: 1rem 1.25rem;
            margin: 0.5rem 0;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            line-height: 1.7;
        }

        /* Pulse animation for status dot */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            animation: pulse 2s ease-in-out infinite;
        }
        .pulse-dot.online { background: #34d399; }
        .pulse-dot.offline { background: #fb7185; }

        /* Hero section */
        .hero-section {
            text-align: center;
            padding: 2rem 0;
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 0.5rem;
            line-height: 1.1;
        }
        .hero-subtitle {
            font-size: 1.15rem;
            color: var(--text-secondary);
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }

        /* Feature card grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }
        .feature-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius);
            padding: 1.5rem;
            transition: var(--transition);
            text-align: center;
        }
        .feature-card:hover {
            border-color: var(--border-glow);
            box-shadow: var(--shadow-glow);
            transform: translateY(-4px);
        }
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.75rem;
        }
        .feature-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.4rem;
        }
        .feature-desc {
            font-size: 0.85rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        /* Spinner */
        .stSpinner > div {
            border-top-color: var(--accent-primary) !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border-subtle);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-primary);
        }

        /* Slider */
        .stSlider > div > div > div {
            color: var(--accent-primary) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
