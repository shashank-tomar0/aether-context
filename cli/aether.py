#!/usr/bin/env python3
"""
AETHER Terminal CLI Tool
Instant high-velocity query interface for platform organizers and developers.
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.database.raw_seed import RAW_USERS, RAW_OPPORTUNITIES
from backend.engine.synthesis import synthesizer
from backend.engine.matchmaker import GraphMatchmaker

def print_banner():
    print("\033[36m" + "="*70)
    print("  AETHER // Universal Context Layer & Autonomous Matchmaker")
    print("  Production Terminal Client v1.0.0")
    print("="*70 + "\033[0m\n")

def get_profiles():
    return [synthesizer.synthesize_user_context(u) for u in RAW_USERS]

def cmd_check(args):
    print_banner()
    query = args.query.lower().strip().lstrip("@")
    profiles = get_profiles()
    
    matched = None
    for u in profiles:
        if (query in u["username"].lower() or 
            query in u["name"].lower() or 
            any(query in part for part in u["name"].lower().split())):
            matched = u
            break
            
    if matched:
        print(f"\033[32m[EXISTS]\033[0m Verified in platform database: \033[1m{matched['name']}\033[0m (@{matched['username']})")
        print(f"  \033[34mArchetype:\033[0m      {matched['archetype']}")
        print(f"  \033[34mReliability:\033[0m    {matched['reliability_score']}/100 (Velocity: {matched['commit_velocity']})")
        print(f"  \033[34mWin Rate:\033[0m       {matched['win_rate']}%")
        print(f"  \033[34mPrimary Domain:\033[0m {matched['primary_domain']}")
        print(f"\n\033[1mSynthesized Context:\033[0m\n{matched['synthesized_narrative']}\n")
    else:
        print(f"\033[31m[NOT FOUND]\033[0m User '{args.query}' does not exist in the platform database.\n")

def cmd_ask(args):
    print_banner()
    q = args.question.lower()
    profiles = get_profiles()
    
    print(f"\033[33mQuery:\033[0m \"{args.question}\"\n")
    print("\033[35m[AETHER Agent Synthesizing Response...]\033[0m\n")

    # Match user
    target = None
    for u in profiles:
        if u["name"].lower() in q or u["username"].lower() in q or u["name"].split()[0].lower() in q:
            target = u
            break

    if target:
        print(f"\033[1mResponse:\033[0m\n{target['synthesized_narrative']}\n")
        print(f"\033[32mComplementary Strategy:\033[0m {target['recommended_pairing']}\n")
    else:
        # Check if searching by skill/archetype
        if "frontend" in q or "ui" in q:
            u = next(p for p in profiles if "Frontend" in p["archetype"])
            print(f"\033[1mTop Match for Frontend & UI Craftsmanship:\033[0m")
            print(f"{u['name']} (@{u['username']})\n{u['synthesized_narrative']}\n")
        elif "systems" in q or "backend" in q or "memory" in q:
            u = next(p for p in profiles if "Systems" in p["archetype"])
            print(f"\033[1mTop Match for Systems & Low-Level Architecture:\033[0m")
            print(f"{u['name']} (@{u['username']})\n{u['synthesized_narrative']}\n")
        else:
            print("AETHER Agent indexed 5 verified builders. Ask about 'Shiv', 'Shashank', 'Elena', or search by domain.")

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
    users_p = subparsers.add_parser("users", help="List all indexed platform users")
    users_p.set_defaults(func=cmd_users)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)

if __name__ == "__main__":
    main()
