"""Thin HTTP client for the RepoRover FastAPI backend."""
from __future__ import annotations

import requests
import streamlit as st

DEFAULT_API_URL = "http://127.0.0.1:8080"


def _base_url() -> str:
    return st.session_state.get("api_url", DEFAULT_API_URL).rstrip("/")


def health_check() -> dict:
    """GET /health – returns {"ok": bool, "neo4j": bool}."""
    try:
        r = requests.get(f"{_base_url()}/health", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"ok": False, "neo4j": False, "error": str(e)}


def ingest_repo(repo_id: str, source: str, branch: str | None = None) -> dict:
    """POST /ingest."""
    payload = {"repo_id": repo_id, "source": source}
    if branch:
        payload["branch"] = branch
    try:
        r = requests.post(f"{_base_url()}/ingest", json=payload, timeout=300)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}


def query_codebase(repo_id: str, question: str, top_k: int = 8) -> dict:
    """POST /query – returns {"answer": str, "context_items": int}."""
    payload = {"repo_id": repo_id, "question": question, "top_k": top_k}
    try:
        r = requests.post(f"{_base_url()}/query", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}


def query_context(repo_id: str, question: str, top_k: int = 8) -> dict:
    """POST /query/context – returns raw context without LLM answer."""
    payload = {"repo_id": repo_id, "question": question, "top_k": top_k}
    try:
        r = requests.post(f"{_base_url()}/query/context", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}


def graph_explore(repo_id: str, qualified_name: str, depth: int = 1) -> dict:
    """POST /graph/explore – returns {"nodes": [...], "edges": [...]}."""
    payload = {"repo_id": repo_id, "qualified_name": qualified_name, "depth": depth}
    try:
        r = requests.post(f"{_base_url()}/graph/explore", json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}


def peek_chroma(repo_id: str) -> dict:
    """GET /test/peek/{repo_id}."""
    try:
        r = requests.get(f"{_base_url()}/test/peek/{repo_id}", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def reset_database() -> dict:
    """POST /test/reset – wipes everything."""
    try:
        r = requests.post(f"{_base_url()}/test/reset", timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}
