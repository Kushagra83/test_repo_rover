"""Home / landing page."""
from __future__ import annotations

import streamlit as st
from pathlib import Path


def render() -> None:
    # ── Hero text ──
    st.markdown(
        """
        <div class="hero-section">
            <h1 class="hero-title">
                <span class="gradient-text">RepoRover</span>
            </h1>
            <p class="hero-subtitle">
                Ingest any codebase. Build a knowledge graph. Ask questions in natural language.
                Powered by <strong>GraphRAG</strong> – combining Neo4j code graphs with semantic vector search.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Feature cards ──
    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">📥</div>
                <div class="feature-title">Smart Ingestion</div>
                <div class="feature-desc">
                    Point at a local folder or Git URL. RepoRover parses ASTs, extracts symbols, builds a code graph in Neo4j, and indexes embeddings in ChromaDB.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Hybrid Retrieval</div>
                <div class="feature-desc">
                    LLM-driven query rewriting combines vector similarity with graph traversal to surface exactly the right code – not just keyword matches.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔗</div>
                <div class="feature-title">Code Graph</div>
                <div class="feature-desc">
                    Functions, classes, files, imports, and call relationships are modeled as a rich graph. Explore execution flows visually.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">Natural Language Q&A</div>
                <div class="feature-desc">
                    Ask architectural questions – "How does auth work?", "Who calls this function?" – and get answers grounded in real code.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Quick start ──
    st.markdown("### 🚀 Quick Start")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="rover-card">
                <h4 style="color:var(--accent-cyan); margin-top:0;">Step 1</h4>
                <p style="color:var(--text-secondary); font-size:0.9rem;">
                    Start the FastAPI backend:<br>
                    <code>uvicorn app.main:app --reload</code>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="rover-card">
                <h4 style="color:var(--accent-emerald); margin-top:0;">Step 2</h4>
                <p style="color:var(--text-secondary); font-size:0.9rem;">
                    Go to <strong>📥 Ingest</strong> and submit a repo path or Git URL with an alias ID.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="rover-card">
                <h4 style="color:var(--accent-secondary); margin-top:0;">Step 3</h4>
                <p style="color:var(--text-secondary); font-size:0.9rem;">
                    Head to <strong>💬 Query</strong> and ask questions about the codebase in plain English.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Tech stack ──
    st.markdown("---")
    st.markdown("### 🛠️ Tech Stack")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Graph DB", "Neo4j")
    c2.metric("Embeddings", "MiniLM-L6")
    c3.metric("Vector Store", "ChromaDB")
    c4.metric("LLM", "Groq / OpenAI")
