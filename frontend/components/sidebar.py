"""Sidebar component with navigation and backend status."""
from __future__ import annotations

import streamlit as st

from frontend.api_client import health_check


def render_sidebar() -> str:
    """Render sidebar and return the selected page name."""
    with st.sidebar:
        # ── Logo / Brand ──
        st.markdown(
            """
            <div style="text-align:center; padding: 1rem 0 0.5rem;">
                <span style="font-size:2.2rem;">🚀</span>
                <h2 style="margin:0.2rem 0 0; font-size:1.4rem;">
                    <span class="gradient-text">RepoRover</span>
                </h2>
                <p style="color:var(--text-muted); font-size:0.75rem; margin:0; letter-spacing:0.05em; text-transform:uppercase;">
                    Codebase Intelligence
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ── Navigation ──
        page = st.radio(
            "Navigate",
            [
                "🏠 Home",
                "📥 Ingest Repository",
                "💬 Query Codebase",
                "🔍 Graph Explorer",
                "⚙️ Settings",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")

        # ── Backend status ──
        st.markdown(
            '<p style="color:var(--text-muted); font-size:0.7rem; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;">Backend Status</p>',
            unsafe_allow_html=True,
        )

        status = health_check()
        if status.get("ok"):
            neo4j_ok = status.get("neo4j", False)
            st.markdown(
                f"""
                <div class="status-badge status-online">
                    <span class="pulse-dot online"></span> API Online
                </div>
                """,
                unsafe_allow_html=True,
            )
            if neo4j_ok:
                st.markdown(
                    '<div class="status-badge status-online" style="margin-top:6px;"><span class="pulse-dot online"></span> Neo4j Connected</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="status-badge status-offline" style="margin-top:6px;"><span class="pulse-dot offline"></span> Neo4j Down</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                """
                <div class="status-badge status-offline">
                    <span class="pulse-dot offline"></span> API Offline
                </div>
                """,
                unsafe_allow_html=True,
            )
            err = status.get("error", "")
            if err:
                st.caption(f"_{err[:80]}_")

        # ── API URL config ──
        st.markdown("<br>", unsafe_allow_html=True)
        api_url = st.text_input(
            "API URL",
            value=st.session_state.get("api_url", "http://localhost:8000"),
            key="api_url_input",
            label_visibility="collapsed",
            placeholder="http://localhost:8000",
        )
        if api_url != st.session_state.get("api_url", "http://localhost:8000"):
            st.session_state["api_url"] = api_url

        st.markdown(
            """
            <div style="text-align:center; padding:2rem 0 0.5rem;">
                <p style="color:var(--text-muted); font-size:0.65rem;">
                    Built with GraphRAG · v0.1.0
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return page
