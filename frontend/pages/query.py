"""Query Codebase page – chat-style Q&A interface."""
from __future__ import annotations

import streamlit as st

from frontend.api_client import query_codebase, query_context


def _init_chat_state() -> None:
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "query_repo_id" not in st.session_state:
        st.session_state.query_repo_id = ""


def render() -> None:
    _init_chat_state()

    st.markdown(
        """
        <div style="margin-bottom:1rem;">
            <h1 style="margin-bottom:0.25rem;">💬 Query Codebase</h1>
            <p style="color:var(--text-secondary); font-size:0.95rem;">
                Ask questions about your ingested codebase. Powered by hybrid GraphRAG retrieval + LLM.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Config bar ──
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        repo_id = st.text_input(
            "🏷️ Repo ID",
            value=st.session_state.query_repo_id,
            placeholder="my-app",
            key="query_repo_input",
        )
        st.session_state.query_repo_id = repo_id
    with col2:
        top_k = st.slider("Top K", min_value=1, max_value=20, value=8, key="query_top_k")
    with col3:
        mode = st.selectbox("Mode", ["💡 Full Answer", "📄 Context Only"], key="query_mode")

    st.markdown("---")

    # ── Chat history ──
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_messages:
            st.markdown(
                """
                <div style="text-align:center; padding:3rem 0; color:var(--text-muted);">
                    <p style="font-size:2.5rem; margin-bottom:0.5rem;">🧠</p>
                    <p style="font-size:1rem;">Ask anything about your codebase</p>
                    <p style="font-size:0.8rem; color:var(--text-muted);">
                        Try: "How does authentication work?" · "Where is the database initialized?" · "What functions call the query service?"
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for msg in st.session_state.chat_messages:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="chat-user">🧑‍💻 &nbsp; {msg["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    with st.expander(f'🤖 RepoRover  ·  {msg.get("context_items", "?")} context items', expanded=True):
                        st.markdown(msg["content"])

    # ── Input ──
    st.markdown("<br>", unsafe_allow_html=True)
    question = st.chat_input("Ask a question about the codebase...", key="query_chat_input")

    if question:
        if not repo_id:
            st.warning("Please set a **Repo ID** above before asking a question.")
            return

        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": question})

        # Query backend
        with st.spinner("🔍 Retrieving context & generating answer..."):
            if mode == "💡 Full Answer":
                result = query_codebase(repo_id=repo_id, question=question, top_k=top_k)
                answer_key = "answer"
            else:
                result = query_context(repo_id=repo_id, question=question, top_k=top_k)
                answer_key = "context"

        if "error" in result:
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": f"❌ **Error:** {result['error']}",
                "context_items": 0,
            })
        else:
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": result.get(answer_key, "No response."),
                "context_items": result.get("context_items", 0),
            })

        st.rerun()

    # ── Clear chat ──
    st.markdown("<br>", unsafe_allow_html=True)
    col_clear, _ = st.columns([1, 5])
    with col_clear:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()
