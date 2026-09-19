"""
AETHER Platform Raw Database Seed
Simulates platform-native activity logs + external profiles (GitHub/LinkedIn)
for a high-stakes developer & hackathon ecosystem platform.
"""

from typing import List, Dict, Any

RAW_USERS: List[Dict[str, Any]] = [
    {
        "id": "usr_001",
        "username": "shiv_dev",
        "name": "Shiv Sharma",
        "email": "shiv@nexus.dev",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
        "created_at": "2024-03-15T09:12:00Z",
        # External Footprint (GitHub & LinkedIn)
        "external_data": {
            "github_username": "shiv-sharma",
            "linkedin_headline": "Senior Full-Stack Engineer | Distributed Systems & Web3",
            "education": "B.Tech Computer Science, IIT Delhi",
            "work_history": [
                {"role": "Backend Engineer", "company": "Razorpay", "duration": "2022-2024"},
                {"role": "SWE Intern", "company": "Directi", "duration": "2021-2022"}
            ],
            "repositories": [
                {"name": "raft-consensus-go", "language": "Go", "stars": 342, "description": "Lightweight Raft consensus implementation"},
                {"name": "hyper-relay", "language": "Rust", "stars": 189, "description": "High-throughput p2p state sync relay"},
                {"name": "defi-zk-rollups", "language": "Solidity", "stars": 95, "description": "Zero-knowledge proofs for batch settlement"}
            ],
            "top_languages": ["Go", "Rust", "TypeScript", "Python"],
            "total_contributions_last_year": 1420
        },
        # Platform-Native Activity Signals
        "platform_activity": {
            "hackathons_participated": 6,
            "hackathons_won": 2,
            "projects_submitted": [
                {
                    "title": "AegisPay",
                    "event": "Solana Global Hackathon 2024",
                    "role": "Lead Architect",
                    "description": "Zero-slippage cross-chain payment orchestrator",
                    "judge_score": 9.4,
                    "feedback": "Architectural execution was flawless; UI was minimal."
                },
                {
                    "title": "ChronosQueue",
                    "event": "Render Hackathon 2024",
                    "role": "Backend Core",
                    "description": "Distributed cron scheduling engine on top of Redis Streams",
                    "judge_score": 9.1,
                    "feedback": "Extremely resilient fault-tolerant queue."
                }
            ],
            "mentoring_sessions_conducted": 8,
            "peer_reviews_given": 24,
            "average_peer_rating": 4.9,
            "commit_velocity_score": 94,
            "flake_rate": 0.0,
            "recent_comments": [
                "Profiling memory leaks in Rust async runtimes under cgroup constraints.",
                "Better to decouple the state transition logic from network transport."
            ]
        }
    },
    {
        "id": "usr_002",
        "username": "shashank-tomar0",
        "name": "Shashank Tomar",
        "email": "shashank@shashanktomar.dev",
        "avatar": "https://avatars.githubusercontent.com/u/102830386?v=4",
        "created_at": "2024-01-10T14:22:00Z",
        "external_data": {
            "github_username": "shashank-tomar0",
            "linkedin_headline": "Systems & AI Memory Engineer | Creator of oneMEM & HydraDB",
            "education": "Computer Science Engineering",
            "work_history": [
                {"role": "Core Maintainer", "company": "oneMEM Open Source", "duration": "2024-Present"},
                {"role": "Autonomous Systems Fellow", "company": "Independent Lab", "duration": "2023-2024"}
            ],
            "repositories": [
                {"name": "onemem", "language": "Python", "stars": 520, "description": "One memory. Every AI. You own it. Local structured memory for AI agents"},
                {"name": "hydradb", "language": "Rust", "stars": 310, "description": "Fast graph database on object storage"},
                {"name": "super-agent-v2", "language": "TypeScript", "stars": 140, "description": "Autonomous browser perception agent"}
            ],
            "top_languages": ["Python", "Rust", "TypeScript", "C++"],
            "total_contributions_last_year": 2180
        },
        "platform_activity": {
            "hackathons_participated": 8,
            "hackathons_won": 4,
            "projects_submitted": [
                {
                    "title": "oneMEM Engine",
                    "event": "Global AI Agents Hackathon",
                    "role": "Creator & Solo Architect",
                    "description": "Deterministic hybrid recall & local embedding memory store",
                    "judge_score": 9.8,
                    "feedback": "Jaw-dropping technical depth. Production standards, zero mocks."
                },
                {
                    "title": "HydraDB Graph",
                    "event": "Next-Gen Data Systems 2024",
                    "role": "Systems Lead",
                    "description": "Graph topology on distributed object storage",
                    "judge_score": 9.5,
                    "feedback": "Deep low-level understanding of graph storage engines."
                }
            ],
            "mentoring_sessions_conducted": 12,
            "peer_reviews_given": 38,
            "average_peer_rating": 5.0,
            "commit_velocity_score": 98,
            "flake_rate": 0.0,
            "recent_comments": [
                "No fake mocks. Verify deterministic retrieval with zero LLM in read path.",
                "Cypher queries must run sub-20ms under index constraints."
            ]
        }
    },
    {
        "id": "usr_003",
        "username": "elena_craft",
        "name": "Elena Rostova",
        "email": "elena@designcraft.io",
        "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150",
        "created_at": "2024-02-18T11:05:00Z",
        "external_data": {
            "github_username": "elena-ui",
            "linkedin_headline": "Staff Frontend & Motion Architect | Design Systems & WebGL",
            "education": "Design & Human-Computer Interaction, Parsons",
            "work_history": [
                {"role": "Lead Design Technologist", "company": "Linear", "duration": "2023-2024"},
                {"role": "Senior Frontend Engineer", "company": "Vercel", "duration": "2021-2023"}
            ],
            "repositories": [
                {"name": "fluid-motion-canvas", "language": "TypeScript", "stars": 890, "description": "60fps physics-based interaction system for React"},
                {"name": "obsidian-tokens", "language": "CSS", "stars": 412, "description": "High-contrast dark design system tokens"},
                {"name": "refero-components", "language": "TypeScript", "stars": 650, "description": "Unstyled accessible primitive components"}
            ],
            "top_languages": ["TypeScript", "React", "GLSL", "TailwindCSS"],
            "total_contributions_last_year": 1780
        },
        "platform_activity": {
            "hackathons_participated": 7,
            "hackathons_won": 3,
            "projects_submitted": [
                {
                    "title": "Aura Canvas",
                    "event": "Design Tooling Hack 2024",
                    "role": "Frontend Craftsperson",
                    "description": "Infinite spatial canvas with fluid gesture control",
                    "judge_score": 9.7,
                    "feedback": "The most polished UI seen all weekend. Feels like an Apple native app."
                }
            ],
            "mentoring_sessions_conducted": 15,
            "peer_reviews_given": 42,
            "average_peer_rating": 4.9,
            "commit_velocity_score": 95,
            "flake_rate": 0.0,
            "recent_comments": [
                "Zero layout shift. Use strict bounding containers and skeleton states.",
                "Borders should be 1px at rgba(255,255,255,0.08) - no harsh outlines."
            ]
        }
    },
    {
        "id": "usr_004",
        "username": "priya_strat",
        "name": "Priya Nair",
        "email": "priya@founderseed.vc",
        "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150",
        "created_at": "2024-04-01T08:30:00Z",
        "external_data": {
            "github_username": "priya-product",
            "linkedin_headline": "Product Strategy & Growth Lead | Ex-Stripe, Seed Founder",
            "education": "Economics & Management, Stanford University",
            "work_history": [
                {"role": "Product Lead", "company": "Stripe", "duration": "2022-2024"},
                {"role": "Growth PM", "company": "Notion", "duration": "2020-2022"}
            ],
            "repositories": [
                {"name": "product-metrics-agent", "language": "Python", "stars": 110, "description": "Automated cohort retention analysis for SaaS"}
            ],
            "top_languages": ["Python", "SQL", "TypeScript"],
            "total_contributions_last_year": 520
        },
        "platform_activity": {
            "hackathons_participated": 5,
            "hackathons_won": 2,
            "projects_submitted": [
                {
                    "title": "LedgerSense",
                    "event": "Fintech Disrupt 2024",
                    "role": "Product & Pitch Lead",
                    "description": "Real-time treasury orchestration for startups",
                    "judge_score": 9.6,
                    "feedback": "Storytelling and product narrative was compelling; clear $10M TAM."
                }
            ],
            "mentoring_sessions_conducted": 20,
            "peer_reviews_given": 30,
            "average_peer_rating": 4.8,
            "commit_velocity_score": 86,
            "flake_rate": 0.0,
            "recent_comments": [
                "Focus on the single sharpest use-case before expanding scope.",
                "Pitch in 60 seconds: Problem, Unfair Advantage, Proof of Live Traction."
            ]
        }
    },
    {
        "id": "usr_005",
        "username": "marcus_ai",
        "name": "Marcus Vance",
        "email": "marcus@neurograph.ai",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150",
        "created_at": "2024-03-20T16:45:00Z",
        "external_data": {
            "github_username": "marcus-vance",
            "linkedin_headline": "Graph AI & Knowledge Retrieval Researcher | Ex-Meta AI",
            "education": "Ph.D. in Graph Machine Learning, Carnegie Mellon",
            "work_history": [
                {"role": "Research Scientist", "company": "Meta AI", "duration": "2021-2023"}
            ],
            "repositories": [
                {"name": "graph-rag-cypher", "language": "Python", "stars": 620, "description": "Multi-hop GraphRAG with Neo4j & Cypher"},
                {"name": "gnn-fraud-detector", "language": "Python", "stars": 340, "description": "Graph Neural Networks for transaction topologies"}
            ],
            "top_languages": ["Python", "Cypher", "C++"],
            "total_contributions_last_year": 1290
        },
        "platform_activity": {
            "hackathons_participated": 4,
            "hackathons_won": 1,
            "projects_submitted": [
                {
                    "title": "GraphSentinel",
                    "event": "Neo4j Knowledge Graph Hack 2024",
                    "role": "Graph AI Lead",
                    "description": "Autonomous entity linking and temporal graph reasoning",
                    "judge_score": 9.3,
                    "feedback": "Brilliant graph algorithm implementation; needs friendlier frontend."
                }
            ],
            "mentoring_sessions_conducted": 6,
            "peer_reviews_given": 18,
            "average_peer_rating": 4.7,
            "commit_velocity_score": 91,
            "flake_rate": 0.0,
            "recent_comments": [
                "Vector search alone misses relational structure. Always enforce graph topology.",
                "Betweenness centrality identifies bottleneck entities instantly."
            ]
        }
    }
]

RAW_OPPORTUNITIES = [
    {
        "id": "opp_001",
        "title": "Autonomous AI Memory & Graph RAG Bounty",
        "sponsor": "Neo4j & Cognee",
        "grant_amount": "$10,000",
        "required_archetypes": ["Systems Architect", "Graph AI Engineer"],
        "required_skills": ["Python", "Neo4j", "Cognee", "Graph Algorithms"],
        "description": "Build an open-source autonomous memory engine with multi-hop Cypher traversal for AI agent fleets."
    },
    {
        "id": "opp_002",
        "title": "High-Taste Web3 & Financial Command Center",
        "sponsor": "Render & Solana Foundation",
        "grant_amount": "$7,500",
        "required_archetypes": ["Frontend Craftsperson", "Product Strategist"],
        "required_skills": ["TypeScript", "Next.js", "Framer Motion", "TailwindCSS"],
        "description": "Create an institutional-grade treasury dashboard deployed on Render with sub-second websocket streaming."
    }
]
