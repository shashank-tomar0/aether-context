#!/usr/bin/env python3
"""
AETHER Universal Cognitive Context Layer & Graph Matchmaker
Claude-Grade Rich Terminal TUI & High-Velocity CLI Client
Interfaces with persistent SQLite, live Neo4j Aura Cloud, and Tavily Web Sensors.
"""

import sys
import os
import argparse
import asyncio
import time
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from rich.prompt import Prompt

from backend.database.raw_seed import RAW_USERS, RAW_OPPORTUNITIES
from backend.database.db import get_all_synthesized_profiles, log_audit, get_audit_logs
from backend.engine.synthesis import synthesizer
from backend.engine.graph_store import graph_store
from backend.engine.matchmaker import GraphMatchmaker

console = Console()

def get_profiles():
    profiles = get_all_synthesized_profiles()
    if not profiles:
        profiles = [synthesizer.synthesize_user_context(u) for u in RAW_USERS]
    return profiles

def print_banner():
    neo_status = "[bold green]* LIVE[/bold green]" if graph_store.neo4j_connected else "[bold yellow]o CACHED[/bold yellow]"
    tav_status = "[bold green]* ACTIVE[/bold green]"
    db_status = "[bold green]* PERSISTENT[/bold green]"
    
    banner_text = Text()
    banner_text.append("A E T H E R", style="bold cyan")
    banner_text.append("  //  Universal Cognitive Context Layer & Graph Matchmaker\n", style="bold white")
    banner_text.append("Engine: ", style="dim")
    banner_text.append("v1.0.0 (Claude-Grade TUI)  ", style="white")
    banner_text.append("| Neo4j Aura: ", style="dim")
    banner_text.append_text(Text.from_markup(neo_status))
    banner_text.append("  | Tavily Sensor: ", style="dim")
    banner_text.append_text(Text.from_markup(tav_status))
    banner_text.append("  | SQLite DB: ", style="dim")
    banner_text.append_text(Text.from_markup(db_status))

    console.print(Panel(banner_text, border_style="cyan", padding=(1, 2)))

def cmd_check(query_str: str):
    query = query_str.lower().strip().lstrip("@")
    profiles = get_profiles()
    
    start_t = time.time()
    matched = None
    # 1. Exact username
    for u in profiles:
        if u["username"].lower() == query:
            matched = u
            break
    # 2. Exact full name or word token
    if not matched:
        for u in profiles:
            if u["name"].lower() == query:
                matched = u
                break
            tokens = [t.lower() for t in u["name"].split() if len(t) >= 3]
            if query in tokens:
                matched = u
                break
    # 3. Substring match
    if not matched and len(query) >= 3:
        for u in profiles:
            if (query in u["username"].lower() or 
                query in u["name"].lower() or 
                query in u["email"].lower()):
                matched = u
                break
            
    latency_ms = round((time.time() - start_t) * 1000, 2)
    log_audit(f"CLI check: {query_str}", matched["username"] if matched else None, bool(matched), latency_ms)

    if matched:
        grid = Table.grid(expand=True, padding=(0, 2))
        grid.add_column(style="dim", width=20)
        grid.add_column(style="bold white")
        
        grid.add_row("Full Name", f"[bold white]{matched['name']}[/bold white] (@{matched['username']})")
        grid.add_row("Cognitive Archetype", f"[bold yellow]{matched['archetype']}[/bold yellow]")
        grid.add_row("Execution Reliability", f"[bold green]{matched['reliability_score']}/100[/bold green] (Velocity: {matched['commit_velocity']})")
        grid.add_row("Platform Win Rate", f"[bold cyan]{matched['win_rate']}%[/bold cyan]")
        grid.add_row("Primary Domain", matched['primary_domain'])
        grid.add_row("Collaboration Style", matched.get('collaboration_style', 'Adaptive'))
        grid.add_row("Core Skills", ", ".join(f"[cyan]{s}[/cyan]" for s in matched.get('skills', [])[:7]))
        
        console.print(Panel(
            grid,
            title=f"[bold green]Verified Candidate[/bold green] : {matched['name']}",
            border_style="green",
            subtitle=f"Query Latency: {latency_ms}ms"
        ))
        
        console.print(Panel(
            Markdown(matched['synthesized_narrative']),
            title="[bold cyan]Synthesized Cognitive Context[/bold cyan]",
            border_style="dim cyan"
        ))
        
        if matched.get("key_projects"):
            proj_table = Table(title="Verified Projects & Hackathon Track Record", border_style="dim")
            proj_table.add_column("Project", style="bold white")
            proj_table.add_column("Event", style="cyan")
            proj_table.add_column("Role", style="yellow")
            proj_table.add_column("Score", justify="right", style="bold green")
            proj_table.add_column("Judge Feedback", style="italic dim")
            for p in matched["key_projects"]:
                proj_table.add_row(
                    p.get("title", ""),
                    p.get("event", ""),
                    p.get("role", ""),
                    str(p.get("judge_score", "-")),
                    p.get("feedback", "")
                )
            console.print(proj_table)
    else:
        console.print(Panel(
            f"[bold red]Not Found[/bold red]: Candidate '{query_str}' was not found in the verified database.",
            border_style="red"
        ))

def cmd_ask(question: str):
    q = question.lower()
    profiles = get_profiles()
    start_t = time.time()
    
    console.print(f"[dim]User Prompt:[/dim] [bold white]\"{question}\"[/bold white]")
    
    with console.status("[bold cyan]Synthesizing Cognitive Context & Querying Tavily Web Sensors...[/bold cyan]"):
        target = None
        for u in profiles:
            if u["name"].lower() in q or u["username"].lower() in q or u["name"].split()[0].lower() in q:
                target = u
                break

        if target:
            ans = target["synthesized_narrative"]
            live = asyncio.run(synthesizer.live_ground_with_tavily(f"{target['name']} developer"))
            if live:
                ans += f"\n\n### Live Market Grounding (via Tavily Sensor)\n{live[:280]}..."
            source_user = target["username"]
        elif "frontend" in q or "design" in q or "ui" in q:
            c = next((u for u in profiles if "Frontend" in u["archetype"]), profiles[0])
            ans = f"**Top Recommendation for UI/Frontend Craftsmanship**: [{c['name']}](@{c['username']})\n\n{c['synthesized_narrative']}"
            source_user = c["username"]
        elif "system" in q or "backend" in q or "distributed" in q:
            c = next((u for u in profiles if "Systems" in u["archetype"]), profiles[1])
            ans = f"**Top Recommendation for Systems & Distributed Architecture**: [{c['name']}](@{c['username']})\n\n{c['synthesized_narrative']}"
            source_user = c["username"]
        else:
            ans = (
                f"**AETHER Context Layer** indexes {len(profiles)} verified builders in persistent SQLite and Neo4j Aura cloud. "
                "Ask existence checks (e.g. *'Is Shiv in our database?'*), query technical capabilities, or request complementary squad assemblies."
            )
            source_user = None

    latency_ms = round((time.time() - start_t) * 1000, 2)
    log_audit(f"CLI ask: {question}", source_user, True, latency_ms)

    console.print(Panel(
        Markdown(ans),
        title="[bold green]AETHER Cognitive Response[/bold green]",
        border_style="green",
        subtitle=f"Response time: {latency_ms}ms | Source: SQLite + Neo4j Aura + Tavily"
    ))

def cmd_match(size: int = 3, goal: str = "High-Velocity AI Fullstack Project"):
    profiles = get_profiles()
    matchmaker = GraphMatchmaker(profiles)
    
    start_t = time.time()
    with console.status("[bold cyan]Computing Orthogonal Complementary Squad via Graph Matchmaker...[/bold cyan]"):
        res = matchmaker.assemble_optimal_squad(target_goal=goal, squad_size=size)
    latency_ms = round((time.time() - start_t) * 1000, 2)
    
    synergy_color = "green" if res["synergy_score"] > 80 else "yellow"
    
    console.print(Panel(
        f"[bold white]Target Goal:[/bold white] {goal}\n"
        f"[bold white]Synergy Score:[/bold white] [{synergy_color}]{res['synergy_score']}%[/{synergy_color}] (Orthogonal Skill Complementarity)\n"
        f"[bold white]Graph Match Latency:[/bold white] {latency_ms}ms",
        title="[bold yellow]Autonomous Squad Assembly[/bold yellow]",
        border_style="yellow"
    ))
    
    squad_table = Table(title="Assembled Squad Lineup", border_style="dim")
    squad_table.add_column("Member", style="bold white")
    squad_table.add_column("Assigned Squad Role", style="bold yellow")
    squad_table.add_column("Archetype", style="cyan")
    squad_table.add_column("Key Skills", style="white")
    squad_table.add_column("Reliability", justify="right", style="bold green")
    
    for m in res["squad_members"]:
        squad_table.add_row(
            f"{m['name']} (@{m['username']})",
            m['role_in_squad'],
            m['archetype'],
            ", ".join(m['key_skills'][:5]),
            f"{m['reliability_score']}/100"
        )
    console.print(squad_table)
    
    console.print(Panel(
        Markdown(res["architectural_rationale"]),
        title="[bold cyan]Architectural Rationale & Synergy Analysis[/bold cyan]",
        border_style="dim cyan"
    ))

def cmd_users():
    profiles = get_profiles()
    table = Table(title=f"Verified Platform Builders ({len(profiles)} Indexed in SQLite & Neo4j)", border_style="dim")
    table.add_column("Name", style="bold white")
    table.add_column("Handle", style="cyan")
    table.add_column("Archetype", style="yellow")
    table.add_column("Domain", style="white")
    table.add_column("Reliability", justify="right", style="bold green")
    table.add_column("Win Rate", justify="right", style="magenta")
    
    for p in profiles:
        table.add_row(
            p["name"],
            f"@{p['username']}",
            p["archetype"],
            p["primary_domain"][:32] + "...",
            f"{p['reliability_score']}/100",
            f"{p['win_rate']}%"
        )
    console.print(table)

def cmd_cypher(query: str):
    console.print(f"[dim]Cypher Query:[/dim] [bold yellow]{query}[/bold yellow]")
    if not graph_store.neo4j_connected:
        console.print("[bold yellow]Notice: Neo4j Aura disconnected, using local graph cache.[/bold yellow]")
    
    start_t = time.time()
    results = graph_store.run_cypher(query)
    latency_ms = round((time.time() - start_t) * 1000, 2)
    
    if results:
        cols = list(results[0].keys())
        table = Table(title=f"Neo4j Aura Results ({len(results)} records, {latency_ms}ms)", border_style="dim")
        for c in cols:
            table.add_column(c, style="bold cyan")
        for row in results[:15]:
            table.add_row(*[str(row.get(c, "")) for c in cols])
        console.print(table)
        if len(results) > 15:
            console.print(f"[dim]... and {len(results)-15} more records[/dim]")
    else:
        console.print(f"[dim]Returned 0 records in {latency_ms}ms[/dim]")

def cmd_audit(limit: int = 20):
    logs = get_audit_logs(limit=limit)
    table = Table(title=f"AETHER Persistent SQLite Audit Trail (Last {len(logs)} queries)", border_style="dim")
    table.add_column("ID", justify="right", style="dim")
    table.add_column("Timestamp", style="cyan")
    table.add_column("Target User", style="yellow")
    table.add_column("Exists", style="green")
    table.add_column("Latency", justify="right", style="bold white")
    table.add_column("Query Summary", style="white")
    
    for l in logs:
        exists_str = "[green]TRUE[/green]" if l.get("exists_result") else "[dim red]FALSE[/dim red]"
        table.add_row(
            str(l.get("id", 0)),
            str(l.get("timestamp", "")),
            str(l.get("target_user") or "-"),
            exists_str,
            f"{l.get('latency_ms', 0)}ms",
            l.get("query", "")[:45]
        )
    console.print(table)

def cmd_stats():
    profiles = get_profiles()
    from backend.config import settings
    from backend.database.db import get_connection, get_audit_logs

    conn = get_connection()
    c = conn.cursor()
    users_n = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    projects_n = c.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    opps_n = c.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0]
    audit_n = c.execute("SELECT COUNT(*) FROM audit_logs").fetchone()[0]
    conn.close()

    archetypes = {}
    for p in profiles:
        archetypes[p["archetype"]] = archetypes.get(p["archetype"], 0) + 1

    grid = Table.grid(expand=True, padding=(0, 2))
    grid.add_column(style="dim", width=28)
    grid.add_column(style="bold white")
    grid.add_row("Indexed Builders", f"[bold]{users_n}[/bold] (synthesized profiles: {len(profiles)})")
    grid.add_row("Projects on Record", str(projects_n))
    grid.add_row("Opportunities Tracked", str(opps_n))
    grid.add_row("Audit Trail Entries", str(audit_n))
    grid.add_row("Neo4j Aura", "[green]CONNECTED[/green]" if graph_store.neo4j_connected else "[yellow]IN-MEMORY FALLBACK[/yellow]")
    grid.add_row("Tavily Web Sensor", "[green]CONFIGURED[/green]" if settings.TAVILY_API_KEY else "[red]MISSING KEY[/red]")
    grid.add_row("LLM Narrative Engine", "[green]CONFIGURED[/green]" if (settings.GEMINI_API_KEY or settings.GROQ_API_KEY or settings.OPENAI_API_KEY) else "[red]MISSING KEY[/red]")

    console.print(Panel(grid, title="[bold cyan]AETHER Context Layer Statistics[/bold cyan]", border_style="cyan"))

    arch_table = Table(title="Archetype Distribution", border_style="dim")
    arch_table.add_column("Archetype", style="yellow")
    arch_table.add_column("Builders", justify="right", style="bold white")
    for a, n in sorted(archetypes.items(), key=lambda kv: -kv[1]):
        arch_table.add_row(a, str(n))
    console.print(arch_table)

def cmd_ingest(csv_path: str):
    from backend.database.ingest_participants import ingest_csv_participants
    with console.status("[bold cyan]Ingesting participants from CSV into SQLite + synthesis pipeline...[/bold cyan]"):
        count = ingest_csv_participants(csv_path)
    if count:
        console.print(Panel(
            f"[bold green]Ingested and synthesized {count} participants.[/bold green]\n"
            f"Source: {csv_path}\nRun [cyan]aether users[/cyan] or re-open the Command Center to see the expanded index.",
            border_style="green"
        ))
    else:
        console.print(Panel(f"[bold red]Ingestion failed:[/bold red] file not found at {csv_path}", border_style="red"))

def run_interactive_tui():
    """Claude-Grade Interactive TUI REPL Session"""
    print_banner()
    console.print(Panel(
        "[bold white]Interactive Commands:[/bold white]\n"
        "  [cyan]/check <name>[/cyan]     Verify developer existence and 4D profile\n"
        "  [cyan]/ask <question>[/cyan]   Ask open-ended question to conversational context agent\n"
        "  [cyan]/match [size][/cyan]     Assemble optimal orthogonal hackathon squad\n"
        "  [cyan]/cypher <query>[/cyan]   Execute Cypher directly on live Neo4j Aura cloud\n"
        "  [cyan]/users[/cyan]            List all verified builders indexed in database\n"
        "  [cyan]/audit[/cyan]            Inspect SQLite query audit trail & latency records\n"
        "  [cyan]/clear[/cyan]            Clear terminal screen\n"
        "  [cyan]/exit[/cyan]             Exit TUI session",
        title="[bold green]AETHER Interactive Console (Claude-Grade TUI)[/bold green]",
        border_style="green"
    ))
    
    while True:
        try:
            cmd_input = Prompt.ask("[bold cyan]aether[/bold cyan]")
            if not cmd_input or not cmd_input.strip():
                continue
            
            line = cmd_input.strip()
            
            if line.lower() in ["/exit", "exit", "quit", ":q"]:
                console.print("[bold cyan]AETHER session terminated. Context layer synced.[/bold cyan]")
                break
            elif line.lower() in ["/clear", "clear"]:
                os.system("cls" if os.name == "nt" else "clear")
                print_banner()
            elif line.lower() in ["/help", "help"]:
                print_banner()
            elif line.startswith("/check"):
                parts = line.split(maxsplit=1)
                if len(parts) > 1:
                    cmd_check(parts[1])
                else:
                    console.print("[yellow]Usage: /check <username or name>[/yellow]")
            elif line.startswith("/ask"):
                parts = line.split(maxsplit=1)
                if len(parts) > 1:
                    cmd_ask(parts[1])
                else:
                    console.print("[yellow]Usage: /ask <natural language question>[/yellow]")
            elif line.startswith("/match"):
                parts = line.split()
                size = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 3
                cmd_match(size=size)
            elif line.startswith("/cypher"):
                parts = line.split(maxsplit=1)
                if len(parts) > 1:
                    cmd_cypher(parts[1])
                else:
                    console.print("[yellow]Usage: /cypher <Cypher statement>[/yellow]")
            elif line.lower() in ["/users", "users"]:
                cmd_users()
            elif line.lower() in ["/audit", "audit"]:
                cmd_audit()
            else:
                cmd_ask(line)
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold cyan]AETHER session terminated.[/bold cyan]")
            break

def main():
    if len(sys.argv) == 1:
        run_interactive_tui()
        return

    parser = argparse.ArgumentParser(description="AETHER Universal Context Layer CLI Client")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # tui / interactive
    tui_p = subparsers.add_parser("tui", help="Launch Claude-grade interactive TUI")
    tui_p.set_defaults(func=lambda args: run_interactive_tui())

    # check
    check_p = subparsers.add_parser("check", help="Run existence check on user")
    check_p.add_argument("query", help="Name or username to check")
    check_p.set_defaults(func=lambda args: cmd_check(args.query))

    # ask
    ask_p = subparsers.add_parser("ask", help="Ask conversational question to context agent")
    ask_p.add_argument("question", help="Natural language question")
    ask_p.set_defaults(func=lambda args: cmd_ask(args.question))

    # match
    match_p = subparsers.add_parser("match", help="Assemble optimal complementary squad")
    match_p.add_argument("--size", type=int, default=3, help="Squad size (default 3)")
    match_p.add_argument("--goal", default="High-Velocity AI Fullstack Project", help="Target goal")
    match_p.set_defaults(func=lambda args: cmd_match(size=args.size, goal=args.goal))

    # users
    users_p = subparsers.add_parser("users", help="List all indexed platform users from SQLite")
    users_p.set_defaults(func=lambda args: cmd_users())

    # cypher
    cypher_p = subparsers.add_parser("cypher", help="Execute Cypher query directly on Neo4j Aura cloud")
    cypher_p.add_argument("query", help="Cypher statement to execute")
    cypher_p.set_defaults(func=lambda args: cmd_cypher(args.query))

    # audit
    audit_p = subparsers.add_parser("audit", help="Inspect SQLite audit trail & query latencies")
    audit_p.add_argument("--limit", type=int, default=20, help="Number of audit rows to display")
    audit_p.set_defaults(func=lambda args: cmd_audit(limit=args.limit))

    # stats
    stats_p = subparsers.add_parser("stats", help="Live context layer statistics and integration health")
    stats_p.set_defaults(func=lambda args: cmd_stats())

    # ingest
    ingest_p = subparsers.add_parser("ingest", help="Ingest participants from a registration CSV")
    ingest_p.add_argument("--csv", default="backend/database/participants.csv", help="Path to participants CSV")
    ingest_p.set_defaults(func=lambda args: cmd_ingest(args.csv))

    args = parser.parse_args()
    if hasattr(args, "func"):
        print_banner()
        args.func(args)
    else:
        run_interactive_tui()

if __name__ == "__main__":
    main()
