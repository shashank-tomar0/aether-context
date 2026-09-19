"""
AETHER Persistent Relational & Cognitive Database Layer
Provides real SQLite storage, automatic schema migrations, and indexing.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

DB_PATH = Path(__file__).resolve().parent / "aether.db"

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        avatar TEXT,
        created_at TEXT NOT NULL
    );
    """)

    # 2. External Professional Data (GitHub & LinkedIn)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS external_profiles (
        user_id TEXT PRIMARY KEY,
        github_username TEXT,
        linkedin_headline TEXT,
        education TEXT,
        top_languages TEXT,
        total_contributions INTEGER,
        repositories TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    # 3. Platform-Native Activity Signals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS platform_activities (
        user_id TEXT PRIMARY KEY,
        hackathons_participated INTEGER DEFAULT 0,
        hackathons_won INTEGER DEFAULT 0,
        commit_velocity INTEGER DEFAULT 0,
        flake_rate REAL DEFAULT 0.0,
        average_peer_rating REAL DEFAULT 5.0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    # 4. Projects Submitted
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        event TEXT NOT NULL,
        role TEXT,
        description TEXT,
        judge_score REAL,
        feedback TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    # 5. Synthesized Context Profiles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS synthesized_context (
        user_id TEXT PRIMARY KEY,
        archetype TEXT NOT NULL,
        primary_domain TEXT NOT NULL,
        reliability_score REAL NOT NULL,
        commit_velocity INTEGER NOT NULL,
        win_rate REAL NOT NULL,
        collaboration_style TEXT NOT NULL,
        synthesized_narrative TEXT NOT NULL,
        complementary_archetypes TEXT,
        skills TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    # 6. Opportunities / Grants
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        sponsor TEXT NOT NULL,
        grant_amount TEXT NOT NULL,
        description TEXT,
        required_archetypes TEXT,
        required_skills TEXT
    );
    """)

    # 7. Query Audit Logs (Records every agent conversational query)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        target_user TEXT,
        exists_result BOOLEAN,
        latency_ms REAL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

def seed_db():
    from backend.database.raw_seed import RAW_USERS, RAW_OPPORTUNITIES
    from backend.engine.synthesis import synthesizer

    conn = get_connection()
    cursor = conn.cursor()

    for u in RAW_USERS:
        # Insert user
        cursor.execute("""
        INSERT OR REPLACE INTO users (id, username, name, email, avatar, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (u["id"], u["username"], u["name"], u["email"], u["avatar"], u["created_at"]))

        # Insert external profile
        ext = u.get("external_data", {})
        cursor.execute("""
        INSERT OR REPLACE INTO external_profiles (user_id, github_username, linkedin_headline, education, top_languages, total_contributions, repositories)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            u["id"],
            ext.get("github_username"),
            ext.get("linkedin_headline"),
            ext.get("education"),
            json.dumps(ext.get("top_languages", [])),
            ext.get("total_contributions_last_year", 0),
            json.dumps(ext.get("repositories", []))
        ))

        # Insert platform activity
        plat = u.get("platform_activity", {})
        cursor.execute("""
        INSERT OR REPLACE INTO platform_activities (user_id, hackathons_participated, hackathons_won, commit_velocity, flake_rate, average_peer_rating)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            u["id"],
            plat.get("hackathons_participated", 0),
            plat.get("hackathons_won", 0),
            plat.get("commit_velocity_score", 0),
            plat.get("flake_rate", 0.0),
            plat.get("average_peer_rating", 5.0)
        ))

        # Insert projects
        for p in plat.get("projects_submitted", []):
            proj_id = f"proj_{u['id']}_{p['title'].replace(' ', '_').lower()}"
            cursor.execute("""
            INSERT OR REPLACE INTO projects (id, user_id, title, event, role, description, judge_score, feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                proj_id,
                u["id"],
                p["title"],
                p["event"],
                p.get("role", "Engineer"),
                p.get("description", ""),
                p.get("judge_score", 9.0),
                p.get("feedback", "")
            ))

        # Synthesize and store context
        synth = synthesizer.synthesize_user_context(u)
        cursor.execute("""
        INSERT OR REPLACE INTO synthesized_context (user_id, archetype, primary_domain, reliability_score, commit_velocity, win_rate, collaboration_style, synthesized_narrative, complementary_archetypes, skills)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            u["id"],
            synth["archetype"],
            synth["primary_domain"],
            synth["reliability_score"],
            synth["commit_velocity"],
            synth["win_rate"],
            synth["collaboration_style"],
            synth["synthesized_narrative"],
            json.dumps(synth["complementary_archetypes"]),
            json.dumps(synth["skills"])
        ))

    # Insert Opportunities
    for opp in RAW_OPPORTUNITIES:
        cursor.execute("""
        INSERT OR REPLACE INTO opportunities (id, title, sponsor, grant_amount, description, required_archetypes, required_skills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            opp["id"],
            opp["title"],
            opp["sponsor"],
            opp["grant_amount"],
            opp.get("description", ""),
            json.dumps(opp.get("required_archetypes", [])),
            json.dumps(opp.get("required_skills", []))
        ))

    conn.commit()
    conn.close()

def log_audit(query: str, target_user: Optional[str], exists_result: bool, latency_ms: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO audit_logs (query, target_user, exists_result, latency_ms)
    VALUES (?, ?, ?, ?)
    """, (query, target_user, exists_result, latency_ms))
    conn.commit()
    conn.close()

def get_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, query, target_user, exists_result, latency_ms, timestamp FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_synthesized_profiles() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.id as user_id, u.username, u.name, u.email, u.avatar,
           s.archetype, s.primary_domain, s.reliability_score, s.commit_velocity,
           s.win_rate, s.collaboration_style, s.synthesized_narrative,
           s.complementary_archetypes, s.skills
    FROM users u
    JOIN synthesized_context s ON u.id = s.user_id
    ORDER BY CASE WHEN u.id LIKE 'usr_%' THEN 0 ELSE 1 END, u.id
    """)
    rows = cursor.fetchall()
    
    profiles = []
    for r in rows:
        p = dict(r)
        p["complementary_archetypes"] = json.loads(p["complementary_archetypes"]) if p["complementary_archetypes"] else []
        p["skills"] = json.loads(p["skills"]) if p["skills"] else []
        
        # Attach projects
        p_cursor = conn.cursor()
        p_cursor.execute("SELECT title, event, role, description, judge_score, feedback FROM projects WHERE user_id = ?", (p["user_id"],))
        p["key_projects"] = [dict(proj) for proj in p_cursor.fetchall()]
        
        profiles.append(p)

    conn.close()
    return profiles

# Auto-initialize on import
init_db()
seed_db()
