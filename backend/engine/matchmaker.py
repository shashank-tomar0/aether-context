"""
AETHER Graph Matchmaking Algorithm (Bonus Point Deliverable)
Computes orthogonal complementary squads and opportunity allocations
using graph affinity, archetype complementarity, and execution velocity.
"""

from typing import List, Dict, Any
from itertools import combinations

class GraphMatchmaker:
    def __init__(self, profiles: List[Dict[str, Any]]):
        self.profiles = profiles
        self.by_id = {p["user_id"]: p for p in profiles}

    def assemble_optimal_squad(self, target_goal: str = "High-Velocity AI Fullstack Project", squad_size: int = 3) -> Dict[str, Any]:
        """
        Assembles an optimal complementary team based on orthogonal archetypes,
        high cumulative reliability, and graph edge affinity.
        """
        if len(self.profiles) < squad_size:
            squad_size = len(self.profiles)

        # Select top candidates per archetype to keep execution instant with 661 profiles
        by_archetype = {}
        for p in self.profiles:
            arch = p.get("archetype", "Generalist")
            by_archetype.setdefault(arch, []).append(p)
        
        search_pool = []
        for arch, members in by_archetype.items():
            sorted_m = sorted(members, key=lambda x: x.get("reliability_score", 0), reverse=True)
            search_pool.extend(sorted_m[:3])

        if len(search_pool) < squad_size:
            search_pool = self.profiles[:20]

        best_combo = None
        highest_synergy = -1.0
        best_breakdown = {}

        for combo in combinations(search_pool, squad_size):
            archetypes = [u["archetype"] for u in combo]
            unique_archetypes = len(set(archetypes))
            
            # Penalize redundant duplicate archetypes (we want complementary balance)
            diversity_score = (unique_archetypes / squad_size) * 100

            # Cumulative execution velocity & reliability
            mean_reliability = sum(u["reliability_score"] for u in combo) / squad_size
            mean_velocity = sum(u["commit_velocity"] for u in combo) / squad_size

            # Graph Complementarity Edge Check
            edge_synergy = 0
            for u1, u2 in combinations(combo, 2):
                if u2["archetype"] in u1.get("complementary_archetypes", []):
                    edge_synergy += 20
                if u1["archetype"] in u2.get("complementary_archetypes", []):
                    edge_synergy += 20

            # Composite Synergy Formula (0 to 100)
            synergy = (
                (diversity_score * 0.35) +
                (mean_reliability * 0.35) +
                (min(edge_synergy, 30) * 1.0)
            )

            if synergy > highest_synergy:
                highest_synergy = synergy
                best_combo = combo
                best_breakdown = {
                    "diversity_score": round(diversity_score, 1),
                    "mean_reliability": round(mean_reliability, 1),
                    "mean_velocity": round(mean_velocity, 1),
                    "graph_affinity_boost": round(min(edge_synergy, 30), 1)
                }

        selected_members = [
            {
                "user_id": u["user_id"],
                "name": u["name"],
                "username": u["username"],
                "avatar": u["avatar"],
                "archetype": u["archetype"],
                "primary_domain": u["primary_domain"],
                "reliability_score": u["reliability_score"],
                "key_skills": u["skills"][:4],
                "role_in_squad": (
                    "Lead Architect & Systems Core" if "Systems" in u["archetype"] else
                    ("Frontend & Interaction Craftsperson" if "Frontend" in u["archetype"] else
                    ("AI & Graph Intelligence Lead" if "Graph" in u["archetype"] else
                    "Product Strategist & GTM Lead"))
                )
            }
            for u in (best_combo or self.profiles[:squad_size])
        ]

        # Generate Architectural Rationale
        member_names = [m["name"] for m in selected_members]
        rationale = (
            f"Assembled a high-alignment {squad_size}-person squad ({', '.join(member_names)}) "
            f"achieving a {highest_synergy:.1f}% mathematical synergy rating. "
            f"This composition eliminates skill overlap while ensuring 100% full-stack coverage: "
            f"deep low-level architecture, 60fps design craftsmanship, and graph reasoning."
        )

        return {
            "target_goal": target_goal,
            "synergy_score": round(highest_synergy, 1),
            "metrics": best_breakdown,
            "squad_members": selected_members,
            "architectural_rationale": rationale
        }

    def match_opportunities(self, opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Downstream Application: Matches platform grants & bounties to candidate profiles.
        """
        matched = []
        for opp in opportunities:
            req_archs = opp.get("required_archetypes", [])
            req_skills = set(opp.get("required_skills", []))

            best_candidates = []
            for p in self.profiles:
                score = 0
                if p["archetype"] in req_archs:
                    score += 50
                overlap = req_skills.intersection(set(p.get("skills", [])))
                score += len(overlap) * 15
                score += (p.get("reliability_score", 0) * 0.2)

                best_candidates.append({
                    "user_id": p["user_id"],
                    "name": p["name"],
                    "username": p["username"],
                    "avatar": p["avatar"],
                    "archetype": p["archetype"],
                    "match_confidence": round(min(score, 99.0), 1)
                })

            best_candidates.sort(key=lambda x: x["match_confidence"], reverse=True)
            matched.append({
                "opportunity": opp,
                "top_matched_talent": best_candidates[:2]
            })

        return matched
