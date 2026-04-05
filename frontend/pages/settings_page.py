"""Settings / Admin page."""
from __future__ import annotations

import streamlit as st

from frontend.api_client import health_check, reset_database


def render() -> None:
    st.markdown(
        """
        <div style="margin-bottom:1.5rem;">
            <h1 style="margin-bottom:0.25rem;">⚙️ Settings</h1>
            <p style="color:var(--text-secondary); font-size:0.95rem;">
                Backend connection, health diagnostics, and administrative actions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Connection ──
    st.markdown("### 🔌 Backend Connection")
    api_url = st.session_state.get("api_url", "http://localhost:8000")

    st.markdown(
        f"""
        <div class="rover-card">
            <p style="color:var(--text-secondary); margin:0 0 0.5rem;">Current API URL</p>
            <code style="font-size:1.05rem; color:var(--accent-cyan);">{api_url}</code>
            <p style="color:var(--text-muted); font-size:0.75rem; margin-top:0.5rem;">
                Change this in the sidebar text input.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Health check ──
    st.markdown("### 🩺 Health Check")
    if st.button("🔄 Refresh Status", key="settings_health"):
        with st.spinner("Checking..."):
            status = health_check()

        if status.get("ok"):
            st.success("✅ Backend is reachable and healthy.")
            col1, col2 = st.columns(2)
            col1.metric("API", "✅ Online")
            col2.metric("Neo4j", "✅ Connected" if status.get("neo4j") else "❌ Disconnected")
        else:
            st.error(f"❌ Backend unreachable: {status.get('error', 'Unknown error')}")

    # ── Danger zone ──
    st.markdown("---")
    st.markdown("### ⚠️ Danger Zone")
    st.markdown(
        """
        <div class="rover-card" style="border-color: rgba(251,113,133,0.3);">
            <p style="color:var(--accent-rose); font-weight:600; margin:0 0 0.5rem;">Reset Database</p>
            <p style="color:var(--text-secondary); font-size:0.85rem; margin:0;">
                This will <strong>wipe the entire Neo4j database</strong> and delete all ChromaDB + work directories.
                All ingested data will be permanently lost. Use this only during development.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_confirm, col_reset = st.columns([3, 1])
    with col_confirm:
        confirm = st.text_input(
            'Type "RESET" to confirm',
            key="reset_confirm",
            placeholder='Type RESET to enable the button',
            label_visibility="collapsed",
        )
    with col_reset:
        reset_disabled = confirm != "RESET"
        if st.button(
            "💣 Reset Everything",
            disabled=reset_disabled,
            key="reset_btn",
            use_container_width=True,
        ):
            with st.spinner("Resetting..."):
                res = reset_database()
            if "error" in res:
                st.error(res["error"])
            else:
                st.success(f"✅ {res.get('message', 'Database reset complete.')}")
                if res.get("directories_deleted"):
                    st.caption(f"Deleted: {', '.join(res['directories_deleted'])}")
                if res.get("directories_failed_locks"):
                    st.warning(f"Could not delete (file locks): {', '.join(res['directories_failed_locks'])}")

    # ── About ──
    st.markdown("---")
    st.markdown("### ℹ️ About RepoRover")
    st.markdown(
        """
        <div class="rover-card">
            <table style="width:100%; color:var(--text-secondary); font-size:0.85rem;">
                <tr><td style="padding:4px 0; font-weight:600; color:var(--text-primary);">Version</td><td>0.1.0</td></tr>
                <tr><td style="padding:4px 0; font-weight:600; color:var(--text-primary);">Graph DB</td><td>Neo4j (Aura / local)</td></tr>
                <tr><td style="padding:4px 0; font-weight:600; color:var(--text-primary);">Vector Store</td><td>ChromaDB (persistent)</td></tr>
                <tr><td style="padding:4px 0; font-weight:600; color:var(--text-primary);">Embeddings</td><td>sentence-transformers/all-MiniLM-L6-v2</td></tr>
                <tr><td style="padding:4px 0; font-weight:600; color:var(--text-primary);">LLM</td><td>OpenAI-compatible (Groq, OpenRouter, etc.)</td></tr>
                <tr><td style="padding:4px 0; font-weight:600; color:var(--text-primary);">AST Parser</td><td>tree-sitter (Python, JS, TS)</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
