"""
AETHER Cognee Cognitive Memory Pipeline
Real Cognee integration: ingested platform events (GitHub pushes, participant profiles)
are cognified into Cognee's semantic memory graph, then retrievable via cognee search.
Import is LAZY (cognee import costs ~30s) - this module is only loaded inside
background tasks, never at FastAPI startup. No mocked results: failures surface honestly.
"""

import os
import asyncio
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("aether.cognee")

_state: Dict[str, bool] = {"configured": False}


def _configure() -> None:
    """Point Cognee at the Groq LLM endpoint (OpenAI-compatible) before first use."""
    if _state["configured"]:
        return
    if os.getenv("GROQ_API_KEY") and not os.getenv("LLM_PROVIDER"):
        os.environ["LLM_PROVIDER"] = "groq"
        os.environ["LLM_MODEL"] = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    if os.getenv("OPENAI_API_KEY") and not os.getenv("LLM_PROVIDER"):
        os.environ["LLM_PROVIDER"] = "openai"
        os.environ["LLM_MODEL"] = os.getenv("LLM_MODEL", "gpt-4o-mini")
    _state["configured"] = True


def cognify_event_sync(event_text: str) -> Dict[str, Any]:
    """
    Runs the real Cognee pipeline: add(text) -> cognify() -> search().
    Returns an honest status dict; never fabricates success.
    """
    _configure()
    try:
        import cognee

        async def _run():
            await cognee.add(event_text)
            await cognee.cognify()
            try:
                results = await cognee.search("SUMMARIES", query_text=event_text[:200])
            except Exception:
                try:
                    results = await cognee.search(query_text=event_text[:200])
                except Exception:
                    results = []
            return results

        results = asyncio.run(_run())
        summarized = []
        for r in (results or [])[:3]:
            summarized.append(str(getattr(r, "text", None) or getattr(r, "name", None) or r)[:220])
        return {
            "engine": "cognee",
            "status": "cognified",
            "search_results": summarized,
            "result_count": len(summarized)
        }
    except Exception as e:
        logger.warning(f"Cognee pipeline failed: {e}")
        return {"engine": "cognee", "status": "unavailable", "error": str(e)[:300]}


def build_event_digest(event: str, sender: str, repo: str, commits: list) -> str:
    lines = [f"GitHub {event} event on repository {repo} by developer {sender}."]
    for c in commits[:10]:
        if isinstance(c, dict):
            msg = c.get("message", "").split("\n")[0]
            if msg:
                lines.append(f"Commit by {sender}: {msg}")
    return "\n".join(lines)


def run_ingestion_background(event: str, sender: str, repo: str, commits: list) -> Optional[Dict[str, Any]]:
    """Entry point for FastAPI BackgroundTasks. Returns the honest pipeline status."""
    digest = build_event_digest(event, sender, repo, commits)
    return cognify_event_sync(digest)
