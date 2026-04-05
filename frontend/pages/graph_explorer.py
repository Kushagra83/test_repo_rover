"""Graph Explorer page – explore the Neo4j code graph visually."""
from __future__ import annotations

import streamlit as st

from frontend.api_client import graph_explore


def render() -> None:
    st.markdown(
        """
        <div style="margin-bottom:1.5rem;">
            <h1 style="margin-bottom:0.25rem;">🔍 Graph Explorer</h1>
            <p style="color:var(--text-secondary); font-size:0.95rem;">
                Explore the code knowledge graph. Enter a symbol's qualified name to see its neighborhood.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Controls ──
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        repo_id = st.text_input(
            "🏷️ Repo ID",
            placeholder="my-app",
            key="graph_repo_id",
        )
    with col2:
        qualified_name = st.text_input(
            "🔗 Qualified Name",
            placeholder="e.g. src/auth.py::login::42",
            key="graph_qn",
            help="The qualified_name of a symbol (function or class). You can find these in query results.",
        )
    with col3:
        depth = st.number_input("Depth", min_value=1, max_value=3, value=1, key="graph_depth")

    explore_clicked = st.button("🔎 Explore Neighborhood", use_container_width=True)

    st.markdown("---")

    if explore_clicked:
        if not repo_id or not qualified_name:
            st.warning("Please provide both a **Repo ID** and a **Qualified Name**.")
            return

        with st.spinner("Querying graph..."):
            result = graph_explore(repo_id=repo_id, qualified_name=qualified_name, depth=int(depth))

        if "error" in result:
            st.error(result["error"])
            return

        nodes = result.get("nodes", [])
        edges = result.get("edges", [])

        # ── Stats ──
        c1, c2 = st.columns(2)
        c1.metric("Nodes", len(nodes))
        c2.metric("Edges", len(edges))

        # ── Nodes table ──
        if nodes:
            st.markdown("### 🟣 Nodes")
            st.dataframe(
                nodes,
                use_container_width=True,
                hide_index=True,
            )

            # ── Visual graph (Mermaid) ──
            if edges:
                st.markdown("### 🔗 Relationships")
                _render_mermaid_graph(nodes, edges)
        else:
            st.info("No nodes found. The symbol may not exist or the repo hasn't been ingested.")

        # ── Edges table ──
        if edges:
            with st.expander("📋 Raw Edge Data", expanded=False):
                st.dataframe(
                    edges,
                    use_container_width=True,
                    hide_index=True,
                )


def _render_mermaid_graph(nodes: list[dict], edges: list[dict]) -> None:
    """Render a simple Mermaid flowchart from graph data."""
    try:
        # Build node ID → label mapping
        node_labels: dict[str, str] = {}
        for i, n in enumerate(nodes):
            label = n.get("name") or n.get("qualified_name") or f"node_{i}"
            node_id = f"n{i}"
            node_labels[str(n.get("id", i))] = (node_id, str(label)[:40])

        lines = ["graph LR"]
        # Define nodes
        for raw_id, (nid, label) in node_labels.items():
            safe_label = label.replace('"', "'")
            lines.append(f'    {nid}["{safe_label}"]')

        # Define edges
        for e in edges:
            src = str(e.get("source") or e.get("from") or "")
            tgt = str(e.get("target") or e.get("to") or "")
            rel = str(e.get("type") or e.get("relationship") or "")

            src_info = node_labels.get(src)
            tgt_info = node_labels.get(tgt)
            if src_info and tgt_info:
                if rel:
                    lines.append(f"    {src_info[0]} -->|{rel}| {tgt_info[0]}")
                else:
                    lines.append(f"    {src_info[0]} --> {tgt_info[0]}")

        mermaid_src = "\n".join(lines)

        st.markdown(
            f"""
            <div class="rover-card" style="overflow-x:auto;">

            ```mermaid
            {mermaid_src}
            ```

            </div>
            """,
            unsafe_allow_html=True,
        )

        # Fallback plain text
        with st.expander("📝 Mermaid Source", expanded=False):
            st.code(mermaid_src, language="mermaid")

    except Exception as exc:
        st.caption(f"Could not render graph visualization: {exc}")
