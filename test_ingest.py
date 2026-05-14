import sys
import traceback

try:
    from app.core.settings import settings
    from app.infrastructure.neo4j_client import Neo4jClient
    from app.services.ingest_service import ingest_repo

    neo4j = Neo4jClient.from_settings()
    res = ingest_repo(neo4j=neo4j, repo_id="test", source="https://github.com/Kushagra83/test_repo_rover", branch="main")
    print("Success:", res)
except Exception as e:
    print("ERROR CAUGHT:")
    traceback.print_exc()
