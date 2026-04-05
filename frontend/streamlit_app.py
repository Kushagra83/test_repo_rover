"""
RepoRover – Streamlit Frontend
Run:  streamlit run frontend/streamlit_app.py
"""
from __future__ import annotations

import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path so we can import 'frontend' module
root_path = Path(__file__).resolve().parents[1]
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# ── Page config (must be first Streamlit call) ──────────────────────────
st.set_page_config(
    page_title="RepoRover · Codebase Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject custom CSS ──────────────────────────────────────────────────
from frontend.theme import inject_custom_css
inject_custom_css()

# ── Sidebar ─────────────────────────────────────────────────────────────
from frontend.components.sidebar import render_sidebar
current_page = render_sidebar()

# ── Page router ─────────────────────────────────────────────────────────
if current_page == "🏠 Home":
    from frontend.pages.home import render
    render()
elif current_page == "📥 Ingest Repository":
    from frontend.pages.ingest import render
    render()
elif current_page == "💬 Query Codebase":
    from frontend.pages.query import render
    render()
elif current_page == "🔍 Graph Explorer":
    from frontend.pages.graph_explorer import render
    render()
elif current_page == "⚙️ Settings":
    from frontend.pages.settings_page import render
    render()
