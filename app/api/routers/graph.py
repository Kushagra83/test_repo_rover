"""Graph exploration router."""
from __future__ import annotations

from fastapi import APIRouter, Request

from app.api.schemas import GraphExploreRequest, GraphExploreResponse


router = APIRouter()


@router.post("/graph/explore", response_model=GraphExploreResponse)
def graph_explore(req: GraphExploreRequest, request: Request):
    """Return the neighborhood of a symbol in the code graph."""
    neo4j = request.app.state.neo4j
    d = max(1, min(req.depth, 3))

    # Query for neighborhood nodes + edges
    q = f"""
    MATCH (s {{repo_id: $repo_id, qualified_name: $qn}})
    CALL (s) {{
        MATCH path = (s)-[r*1..{d}]-(n)
        UNWIND relationships(path) AS rel
        WITH DISTINCT n, rel, startNode(rel) AS src, endNode(rel) AS tgt
        RETURN
            collect(DISTINCT {{
                id: elementId(n),
                name: n.name,
                qualified_name: n.qualified_name,
                labels: labels(n)
            }}) AS neighbor_nodes,
            collect(DISTINCT {{
                source: elementId(src),
                target: elementId(tgt),
                type: type(rel)
            }}) AS neighbor_edges
    }}
    WITH neighbor_nodes, neighbor_edges, s
    RETURN
        [{{id: elementId(s), name: s.name, qualified_name: s.qualified_name, labels: labels(s)}}] + neighbor_nodes AS nodes,
        neighbor_edges AS edges
    """
    with neo4j.driver.session() as sess:
        result = sess.run(q, repo_id=req.repo_id, qn=req.qualified_name)
        record = result.single()

    if record is None:
        return GraphExploreResponse(nodes=[], edges=[])

    return GraphExploreResponse(
        nodes=record["nodes"] or [],
        edges=record["edges"] or [],
    )
