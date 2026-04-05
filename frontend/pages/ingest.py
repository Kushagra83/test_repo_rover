"""Ingest Repository page."""
from __future__ import annotations

import streamlit as st

from frontend.api_client import ingest_repo, peek_chroma


def render() -> None:
    st.markdown(
        """
        <div style="margin-bottom:1.5rem;">
            <h1 style="margin-bottom:0.25rem;">📥 Ingest Repository</h1>
            <p style="color:var(--text-secondary); font-size:0.95rem;">
                Feed a codebase into RepoRover. Supports local folders and remote Git URLs.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Form ──
    with st.container():
        col1, col2 = st.columns([2, 1])

        with col1:
            source = st.text_input(
                "📂 Repository Source",
                placeholder="e.g.  D:\\projects\\my-app  or  https://github.com/user/repo.git",
                help="Local absolute path or a remote Git clone URL",
            )

        with col2:
            repo_id = st.text_input(
                "🏷️ Repo ID (alias)",
                placeholder="e.g. my-app",
                help="A short, stable identifier to reference this repo later in queries",
            )

        branch = st.text_input(
            "🌿 Branch (optional)",
            placeholder="main",
            help="Only used for remote Git URLs. Leave blank for the default branch.",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Submit ──
    col_btn, col_status = st.columns([1, 3])
    with col_btn:
        ingest_clicked = st.button("🚀 Start Ingestion", use_container_width=True)

    if ingest_clicked:
        if not source or not repo_id:
            st.warning("Please provide both a **source** and a **repo ID**.")
            return

        with st.status("Ingesting repository...", expanded=True) as status_ui:
            st.write("🔍 Resolving source (clone if remote)...")
            st.write("🌳 Parsing ASTs & extracting symbols...")
            st.write("📊 Building Neo4j graph & vector embeddings...")

            result = ingest_repo(repo_id=repo_id, source=source, branch=branch or None)

            if "error" in result:
                status_ui.update(label="❌ Ingestion failed", state="error")
                st.error(result["error"])
            else:
                status_ui.update(label="✅ Ingestion complete!", state="complete")

                # Results
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                c1.metric("Repo ID", result.get("repo_id", repo_id))
                c2.metric("Files Indexed", result.get("files_indexed", "—"))
                c3.metric("Symbols Indexed", result.get("symbols_indexed", "—"))

                # Save to history
                history = st.session_state.setdefault("ingested_repos", [])
                if repo_id not in history:
                    history.append(repo_id)

                st.balloons()

    # ── Previously ingested repos ──
    st.markdown("---")
    st.markdown("### 📋 Quick Peek")
    st.caption("Check how many symbols are indexed for a repo in ChromaDB.")

    peek_id = st.text_input(
        "Repo ID to peek",
        placeholder="my-app",
        key="peek_repo_id",
        label_visibility="collapsed",
    )
    if st.button("🔎 Peek", key="peek_btn"):
        if peek_id:
            with st.spinner("Querying ChromaDB..."):
                res = peek_chroma(peek_id)
            if "error" in res:
                st.error(res["error"])
            else:
                count = res.get("symbol_count", -1)
                if count >= 0:
                    st.success(f"**{peek_id}** has **{count}** symbol embeddings in ChromaDB.")
                else:
                    st.warning(f"Collection for **{peek_id}** not found or empty.")
        else:
            st.info("Enter a repo ID above.")
