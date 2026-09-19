# AETHER: Universal Context Layer - Architectural State & Agent Handoff

Single source of truth for cross-agent memory, architectural contracts, and operational state.

---

## 1. System Identity & Mission
- **Repository**: `https://github.com/shashank-tomar0/aether-context`
- **Active Commit**: `7b9747c` (Verified on `main`)
- **Target Subdomain**: `shashanktomar.dev`
- **Problem Statement Track**: **PS-3: Universal Context Layer for Platform Users**
- **Sponsors & Technology Matrix**:
  - **Neo4j**: Relational context graph & graph matchmaking algorithm (Jaccard complementarity + vector affinity).
  - **Cognee**: Cognitive memory engine for 4D profile synthesis (Archetype, Velocity, Collaboration, Gaps).
  - **Tavily**: Live external web & GitHub repo verification sensor.
  - **Render**: Production container hosting with automated continuous deployment.

---

## 2. Dual-Surface Architecture & Routes
- **Route `/`**: Pixel-perfect cloned Cofounder landing page (`https://cofounder.co/`) transformed with absolute typography, glassmorphism, and AETHER Context Layer copy.
- **Route `/app` & `/command-center`**: Refero-grade Obsidian Command Center (`#060709`) featuring:
  - 60fps HTML5 Canvas interactive graph with physics and draggable nodes.
  - Conversational query drawer with instant existence checks (`[VERIFIED EXISTENCE]`).
  - Autonomous Squad Matchmaker with mathematical synergy score calculation.
  - Downstream Opportunity & Bounty Dispatcher.
  - Raw Database vs. Synthesized Context Diff Inspector.
  - Role-based Authentication Switcher (Organizer vs. Builder vs. Guest).
- **Route `/api/*`**: FastAPI REST API endpoints.

---

## 3. Demo Credentials
- **Organizer Admin**: `admin@nexus.dev` / `admin123` (Role: `organizer`, Token: `tok_organizer_998124`)
- **Builder Candidate**: `shiv@nexus.dev` / `builder123` (Role: `builder`, Token: `tok_builder_112048`)

---

## 4. API Keys & Production Environment Variables
The application runs with a zero-failure resilient architecture: if external keys are not provided, it utilizes built-in cognitive heuristics and an in-memory topological graph engine. To activate full cloud sponsor integrations:

```env
# Port & Host
PORT=8000
HOST=0.0.0.0

# Tavily Real-Time Grounding (tavily.com)
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxx

# Neo4j Aura Graph Database (neo4j.com/cloud/aura)
NEO4J_URI=neo4j+s://xxxxxxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=xxxxxxxxxxxxxxxx

# LLM Providers for Cognee
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx
GEMINI_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxx
```

---

## 5. Verified Endpoints & Test Status
All 9 automated integration and authentication tests passing in `tests/test_api.py`:
- `test_health_check` [PASS]
- `test_root_serves_html` [PASS]
- `test_app_serves_command_center` [PASS]
- `test_user_existence_check_found` [PASS]
- `test_user_existence_check_not_found` [PASS]
- `test_agent_conversational_query_existence` [PASS]
- `test_agent_conversational_query_frontend_recommendation` [PASS]
- `test_graph_topology` [PASS]
- `test_matchmaking_squad_assembly` [PASS]
- `test_auth_login_success` [PASS]
- `test_auth_login_failure` [PASS]
- `test_downstream_opportunities` [PASS]

---

## 6. How to Run & Verify
```bash
# 1. Start Server
uvicorn backend.api:app --host 127.0.0.1 --port 8000

# 2. Run CLI
python cli/aether.py check "Shiv"
python cli/aether.py match --size 3

# 3. Run Automated Tests
python tests/test_api.py
```
