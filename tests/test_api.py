"""
AETHER Automated Integration & Verification Test Suite
Tests: Existence Check, Conversational Agent, Graph Topology, Matchmaking Algorithm, Downstream Apps
"""

import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from fastapi.testclient import TestClient
from backend.api import app

client = TestClient(app)

def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["users_indexed"] >= 5

def test_root_serves_html():
    res = client.get("/")
    assert res.status_code == 200
    assert "AETHER // Universal Context Layer" in res.text

def test_user_existence_check_found():
    # Exact scenario from PDF problem statement: "Is Shiv in our database?"
    res = client.get("/api/users/check?q=Shiv")
    assert res.status_code == 200
    data = res.json()
    assert data["exists"] is True
    assert data["user"]["username"] == "shiv_dev"
    assert "Verified:" in data["message"]

def test_user_existence_check_not_found():
    res = client.get("/api/users/check?q=NonExistentDeveloper404")
    assert res.status_code == 200
    data = res.json()
    assert data["exists"] is False
    assert data["user"] is None

def test_agent_conversational_query_existence():
    res = client.post("/api/agent/query", json={"query": "Is Shiv in our database? What has he built?"})
    assert res.status_code == 200
    data = res.json()
    assert data["exists"] is True
    assert "Shiv Sharma" in data["synthesized_response"]
    assert "High-Velocity Systems Architect" in data["synthesized_response"]

def test_agent_conversational_query_frontend_recommendation():
    res = client.post("/api/agent/query", json={"query": "Who is our best frontend engineer with high design taste?"})
    assert res.status_code == 200
    data = res.json()
    assert data["exists"] is True
    assert "Elena" in data["synthesized_response"]

def test_graph_topology():
    res = client.get("/api/graph/topology")
    assert res.status_code == 200
    data = res.json()
    assert len(data["nodes"]) > 0
    assert len(data["edges"]) > 0
    assert "stats" in data

def test_matchmaking_squad_assembly():
    res = client.post("/api/matchmaking/squad", json={"target_goal": "AI Systems & Web3", "squad_size": 3})
    assert res.status_code == 200
    data = res.json()
    assert len(data["squad_members"]) == 3
    assert data["synergy_score"] > 80.0
    assert "architectural_rationale" in data

def test_downstream_opportunities():
    res = client.get("/api/opportunities/match")
    assert res.status_code == 200
    data = res.json()
    assert len(data["matches"]) > 0
    assert len(data["matches"][0]["top_matched_talent"]) > 0

if __name__ == "__main__":
    print("Running integration tests...")
    test_health_check()
    test_root_serves_html()
    test_user_existence_check_found()
    test_user_existence_check_not_found()
    test_agent_conversational_query_existence()
    test_agent_conversational_query_frontend_recommendation()
    test_graph_topology()
    test_matchmaking_squad_assembly()
    test_downstream_opportunities()
    print("All 7 tests passed successfully!")
