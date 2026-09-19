# AETHER: Universal Context Layer - Architectural State & Agent Handoff

Single source of truth for cross-agent memory, architectural contracts, and operational state.

---

## 1. System Identity & Mission
- **Repository**: `https://github.com/shashank-tomar0/aether-context`
- **Target Subdomain**: `shashanktomar.dev`
- **Problem Statement Track**: **PS-3: Universal Context Layer for Platform Users**
- **Sponsors & Technology Matrix**:
  - **Neo4j**: Relational context graph & graph matchmaking algorithm (Jaccard complementarity + vector affinity).
  - **Cognee**: Cognitive memory engine for 4D profile synthesis (Archetype, Velocity, Collaboration, Gaps).
  - **Tavily**: Live external web & GitHub repo verification sensor.
  - **Render**: Production container hosting with automated continuous deployment.

---

## 2. Active Technical Stack & Directory Layout
```
ai-hack/
├── .agents/skills/              # Installed agent skills (caveman, ponytail, taste-skill, impeccable, context7)
├── backend/
│   ├── api.py                   # FastAPI application & REST endpoints
│   ├── config.py                # Environment configuration
│   ├── requirements.txt         # Production Python dependencies
│   ├── database/
│   │   └── raw_seed.py          # Platform database seed with rich user activity logs & projects
│   ├── engine/
│   │   ├── synthesis.py         # Cognee cognitive extraction & 4D profile synthesizer
│   │   ├── graph_store.py       # Neo4j driver + in-memory topological graph engine
│   │   └── matchmaker.py        # Graph squad assembly & opportunity allocation algorithms
│   └── static/
│       └── index.html           # Refero-grade Web Command Center with 60fps graph canvas
├── cli/
│   └── aether.py                # High-velocity terminal client (check, ask, match, users)
├── tests/
│   └── test_api.py              # Automated test suite (all 7 tests passing)
├── Dockerfile                   # Multi-stage production container
├── render.yaml                  # Infrastructure-as-Code for Render Cloud
├── ai.md                        # Context preservation & handoff document
└── README.md                    # Production documentation (no emojis, complete specs)
```

---

## 3. Verified Endpoints & Test Status
All tests passing in `tests/test_api.py`:
- `GET /`: Serves production Web Command Center.
- `GET /api/health`: Status check, version, and user indexing telemetry.
- `GET /api/users/check?q={name}`: Instant existence verification.
- `POST /api/agent/query`: Conversational AI agent synthesizing open-ended context.
- `GET /api/graph/topology`: Node and edge payload for graph visualization.
- `POST /api/matchmaking/squad`: Assembles orthogonal complementary squads (Bonus Point #1).
- `GET /api/opportunities/match`: Downstream opportunity matching (Bonus Point #2).

---

## 4. Immediate Handoff Instructions for Subsequent AI / Agents
1. **To start the local server**:
   ```bash
   uvicorn backend.api.app --reload --port 8000
   ```
2. **To run the CLI**:
   ```bash
   python cli/aether.py check "Shiv"
   python cli/aether.py match --size 3
   ```
3. **To run automated tests**:
   ```bash
   python tests/test_api.py
   ```
4. **To deploy to Render**:
   - Link GitHub repository `shashank-tomar0/aether-context` to Render as a Web Service.
   - Set build command: `pip install -r backend/requirements.txt`
   - Set start command: `uvicorn backend.api:app --host 0.0.0.0 --port $PORT`
   - Bind custom domain CNAME in DNS to `shashanktomar.dev`.
