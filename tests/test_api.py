"""
AETHER Automated Integration & Verification Suite
Covers: auth flow, existence check, conversational agent, graph topology + live Cypher,
matchmaking, opportunities, bots, webhooks, audit trail, and route protection.
"""

import os
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

os.environ.setdefault("AETHER_ADMIN_EMAIL", "admin@nexus.dev")
os.environ.setdefault("AETHER_ADMIN_PASSWORD", "admin123")

from fastapi.testclient import TestClient
from backend.api import app

client = TestClient(app)
ADMIN_EMAIL = os.environ["AETHER_ADMIN_EMAIL"]
ADMIN_PASSWORD = os.environ["AETHER_ADMIN_PASSWORD"]


def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["users_indexed"] >= 5


def test_landing_serves_pixel_clone():
    res = client.get("/")
    assert res.status_code == 200
    assert "AETHER" in res.text
    assert "<script" not in res.text.lower() or res.text.count("<script") <= 1
    assert "Cofounder" not in res.text


def test_public_stats():
    res = client.get("/api/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["users_indexed"] >= 5
    assert "top_builders" in data


def test_protected_api_rejects_anonymous():
    res = client.get("/api/users")
    assert res.status_code == 401


def test_command_page_redirects_anonymous():
    res = client.get("/command", follow_redirects=False)
    assert res.status_code == 307
    assert "/login" in res.headers["location"]


def test_login_flow_sets_cookie():
    res = client.post("/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert res.status_code == 200
    assert res.json()["authenticated"] is True
    assert "aether_session" in res.cookies

    me = client.get("/api/auth/me").json()
    assert me["authenticated"] is True
    assert me["email"] == ADMIN_EMAIL.lower()


def test_login_rejects_bad_credentials():
    res = client.post("/api/auth/login", json={"email": ADMIN_EMAIL, "password": "wrong"})
    assert res.status_code == 401


def test_user_existence_check_found():
    res = client.get("/api/users/check?q=Shiv")
    assert res.status_code == 200
    data = res.json()
    assert data["exists"] is True
    assert data["user"]["username"] == "shiv_dev"


def test_user_existence_check_not_found():
    res = client.get("/api/users/check?q=NonExistentDeveloper404")
    assert res.status_code == 200
    data = res.json()
    assert data["exists"] is False


def test_agent_conversational_query():
    res = client.post("/api/agent/query", json={"query": "Is Shiv in our database? What has he built?"})
    assert res.status_code == 200
    data = res.json()
    assert data["exists"] is True
    assert data["target_user"] == "shiv_dev"
    assert "latency_ms" in data


def test_agent_open_search_query():
    res = client.post("/api/agent/query", json={"query": "Who is our best frontend engineer with high design taste?"})
    assert res.status_code == 200
    data = res.json()
    assert data["exists"] is True


def test_users_index_includes_real_participants():
    res = client.get("/api/users")
    assert res.status_code == 200
    users = res.json()["users"]
    assert len(users) >= 600
    sample = users[10]
    for key in ("username", "name", "archetype", "reliability_score", "synthesized_narrative"):
        assert key in sample


def test_graph_topology():
    res = client.get("/api/graph/topology")
    assert res.status_code == 200
    data = res.json()
    assert len(data["nodes"]) > 0
    assert len(data["edges"]) > 0


def test_live_cypher():
    res = client.post("/api/graph/cypher", json={"query": "MATCH (u:User) RETURN u.name LIMIT 5"})
    assert res.status_code == 200
    data = res.json()
    assert "count" in data
    assert "neo4j_connected" in data


def test_matchmaking_squad_assembly():
    import time as _t
    start = _t.time()
    res = client.post("/api/matchmaking/squad", json={"target_goal": "AI Systems & Web3", "squad_size": 3})
    elapsed = _t.time() - start
    assert res.status_code == 200
    data = res.json()
    assert len(data["squad_members"]) == 3
    assert "architectural_rationale" in data
    assert elapsed < 10.0, f"Matchmaker took {elapsed:.1f}s - pool cap regression"


def test_downstream_opportunities():
    res = client.get("/api/opportunities/match")
    assert res.status_code == 200
    data = res.json()
    assert len(data["matches"]) > 0


def test_telegram_simulate():
    res = client.get("/api/integrations/telegram/simulate?command=/check Shiv")
    assert res.status_code == 200
    assert "bot_response" in res.json()


def test_slack_simulate():
    res = client.get("/api/integrations/slack/simulate?text=check Shiv")
    assert res.status_code == 200
    assert "blocks" in res.json()


def test_github_webhook_ingestion():
    res = client.post(
        "/webhooks/github",
        json={
            "sender": {"login": "CxashxG"},
            "repository": {"full_name": "CxashxG/aether-core"},
            "commits": [{"message": "feat: pipeline"}, {"message": "fix: graph"}]
        },
        headers={"X-GitHub-Event": "push"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["commit_count"] == 2
    assert data["status"] == "ingested"


def test_audit_logs_populated():
    res = client.get("/api/audit/logs?limit=25")
    assert res.status_code == 200
    assert len(res.json()["audit_logs"]) > 0


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    sys.exit(1 if failed else 0)
