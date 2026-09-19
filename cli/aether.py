#!/usr/bin/env python3
"""
AETHER Universal Context Layer CLI Tool
Production Terminal Client interfacing directly with persistent SQLite,
live Neo4j Aura Graph Database, and Tavily Real-Time Web Sensors.
"""

import sys
import argparse
import asyncio
import time
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.database.raw_seed import RAW_USERS, RAW_OPPORTUNITIES
from backend.database.db import get_all_synthesized_profiles, log_audit, get_audit_logs
from backend.engine.synthesis import synthesizer
from backend.engine.graph_store import graph_store
from backend.engine.matchmaker import GraphMatchmaker

def print_banner():
    print("\033[36m" + "="*75)
    print("  AETHER // Universal Cognitive Context Layer & Graph Matchmaker")
    print("  Production Terminal Client v1.0.0 [SQLite + Neo4j Aura + Tavily Live]")
    print("="*75 + "\033[0m\n")

def get_profiles():
    profiles = get_all_synthesized_profiles()
    if not profiles:
        profiles = [synthesizer.synthesize_user_context(u) for u in RAW_USERS]
    return profiles

def cmd_check(args):
    print_banner()
    query = args.query.lower().strip().lstrip("@")
    profiles = get_profiles()
    
    start_t = time.time()
    matched = None
    for u in profiles:
        if (query in u["username"].lower() or 
            query in u["name"].lower() or 
            any(query in part for part in u["name"].lower().split())):
            matched = u
            break
            
    latency_ms = round((time.time() - start_t) * 1000, 2)
    log_audit(f"CLI check: {args.query}", matched["username"] if matched else None, bool(matched), latency_ms)

    if matched:
        print(f"\033[32m[EXISTS]\033[0m Verified in platform database: \033[1m{matched['name']}\033[0m (@{matched['username']})")
        print(f"  \033[34mArchetype:\033[0m      {matched['archetype']}")
        print(f"  \033[34mReliability:\033[0m    {matched['reliability_score']}/100 (Velocity: {matched['commit_velocity']})")
        print(f"  \033[34mWin Rate:\033[0m       {matched['win_rate']}%")
        print(f"  \033[34mPrimary Domain:\033[0m {matched['primary_domain']}")
        print(f"  \033[34mSkills:\033[0m         {', '.join(matched.get('skills', [])[:6])}")
        print(f"\n\033[1mSynthesized Context:\033[0m\n{matched['synthesized_narrative']}\n")
    else:
        print(f"\033[31m[NOT FOUND]\033[0m User '{args.query}' was not found in the platform database.\n")

def cmd_ask(args):
    print_banner()
    q = args.question.lower()
    profiles = get_profiles()
    start_t = time.time()
    
    print(f"\033[33mQuestion:\033[0m \"{args.question}\"")
    print("\033[35m[AETHER Agent Synthesizing Cognitive Context via Cognee Engine...]\033[0m\n")

    # Match user
    target = None
    for u in profiles:
        if u["name"].lower() in q or u["username"].lower() in q or u["name"].split()[0].lower() in q:
            target = u
            break

    if target:
        ans = target["synthesized_narrative"]
        # Live Tavily ground
        live = asyncio.run(synthesizer.live_ground_with_tavily(f"{target['name']} developer"))
        if live:
            ans += f"\n\n\033[32m[Tavily Live Sensor Grounding]:\033[0m {live[:200]}..."

        print(f"\033[1mResponse for {target['name']} (@{target['username']}):\033[0m\n{ans}\n")
        print(f"\033[32mComplementary Pairing Strategy:\033[0m {target['recommended_pairing']}\n")
        target_name = target["username"]
    else:
        if "frontend" in q or "ui" in q or "design" in q:
            u = next(p for p in profiles if "Frontend" in p["archetype"])
            print(f"\033[1mTop Match for Frontend & UI Craftsmanship:\033[0m")
            print(f"{u['name']} (@{u['username']})\n{u['synthesized_narrative']}\n")
            target_name = u["username"]
        elif "systems" in q or "backend" in q or "memory" in q:
            u = next(p for p in profiles if "Systems" in p["archetype"])
            print(f"\033[1mTop Match for Systems & Low-Level Architecture:\033[0m")
            print(f"{u['name']} (@{u['username']})\n{u['synthesized_narrative']}\n")
            target_name = u["username"]
        else:
            print(f"AETHER Context Layer is indexing {len(profiles)} verified platform users from persistent SQLite store.")
            print("Try asking: 'Is Shiv in our database?' or 'Who is best for high-taste frontend?'\n")
            target_name = None

    latency_ms = round((time.time() - start_t) * 1000, 2)
    log_audit(f"CLI ask: {args.question}", target_name, True, latency_ms)

def cmd_match(args):
    print_banner()
    profiles = get_profiles()
    mm = GraphMatchmaker(profiles)
    res = mm.assemble_optimal_squad(target_goal=args.goal, squad_size=args.size)

    print(f"\033[1;36mAutonomous Squad Assembly: \"{res['target_goal']}\"\033[0m")
    print(f"Overall Mathematical Synergy: \033[1;32m{res['synergy_score']}%\033[0m")
    print(f"Metrics: Diversity {res['metrics']['diversity_score']} | Mean Reliability {res['metrics']['mean_reliability']}/100\n")
    
    print("\033[1mSelected Squad Members:\033[0m")
    for m in res["squad_members"]:
        print(f"  - \033[1;37m{m['name']}\033[0m (@{m['username']}) -> \033[33m{m['role_in_squad']}\033[0m")
        print(f"    Archetype: {m['archetype']} | Skills: {', '.join(m['key_skills'])}")
    
    print(f"\n\033[35mArchitectural Rationale:\033[0m\n{res['architectural_rationale']}\n")

def cmd_users(args):
    print_banner()
    profiles = get_profiles()
    print(f"{'NAME':<20} {'USERNAME':<16} {'ARCHETYPE':<35} {'RELIABILITY':<12}")
    print("-" * 85)
    for p in profiles:
        print(f"{p['name']:<20} @{p['username']:<15} {p['archetype']:<35} {p['reliability_score']}/100")
    print(f"\nTotal Indexed: {len(profiles)} verified profiles in SQLite database.\n")

def cmd_cypher(args):
    print_banner()
    print(f"\033[33mExecuting Cypher on Neo4j Aura Cloud:\033[0m {args.query}\n")
    if not graph_store.neo4j_connected:
        print("\033[31mNeo4j Aura not connected. Using local in-memory graph cache.\033[0m")
    results = graph_store.run_cypher(args.query)
    print(f"\033[32mReturned {len(results)} records:\033[0m")
    for i, row in enumerate(results[:10]):
        print(f"[{i+1}] {row}")
    if len(results) > 10:
        print(f"... and {len(results)-10} more rows")
    print()

def cmd_audit(args):
    print_banner()
    logs = get_audit_logs(limit=args.limit)
    print(f"{'ID':<6} {'TIMESTAMP':<20} {'TARGET':<16} {'EXISTS':<8} {'LATENCY':<10} {'QUERY'}")
    print("-" * 90)
    for l in logs:
        print(f"{l.get('id', 0):<6} {str(l.get('timestamp', '')):<20} {str(l.get('target_user') or '-'):<16} {str(bool(l.get('exists_result'))):<8} {str(l.get('latency_ms', 0))+'ms':<10} {l.get('query', '')[:30]}")
    print()

def main():
    parser = argparse.ArgumentParser(description="AETHER Universal Context Layer CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # check
    check_p = subparsers.add_parser("check", help="Run existence check on user")
    check_p.add_argument("query", help="Name or username to check")
    check_p.set_defaults(func=cmd_check)

    # ask
    ask_p = subparsers.add_parser("ask", help="Ask conversational question to context agent")
    ask_p.add_argument("question", help="Natural language question")
    ask_p.set_defaults(func=cmd_ask)

    # match
    match_p = subparsers.add_parser("match", help="Assemble optimal complementary squad")
    match_p.add_argument("--size", type=int, default=3, help="Squad size (default 3)")
    match_p.add_argument("--goal", default="High-Velocity AI Fullstack Project", help="Target goal")
    match_p.set_defaults(func=cmd_match)

    # users
    users_p = subparsers.add_parser("users", help="List all indexed platform users from SQLite")
    users_p.set_defaults(func=cmd_users)

    # cypher
    cypher_p = subparsers.add_parser("cypher", help="Run Cypher query on live Neo4j Aura")
    cypher_p.add_argument("query", default="MATCH (u:User) RETURN u.name, u.archetype", nargs="?", help="Cypher query string")
    cypher_p.set_defaults(func=cmd_cypher)

    # audit
    audit_p = subparsers.add_parser("audit", help="Inspect query audit logs from SQLite")
    audit_p.add_argument("--limit", type=int, default=20, help="Max logs to show")
    audit_p.set_defaults(func=cmd_audit)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)

if __name__ == "__main__":
    main()
