"""
Token-Craft Scoring Engine

Calculates scores across 5 categories:
1. Token Efficiency (35%) - Performance vs baseline
2. Optimization Adoption (25%) - Usage of best practices
3. Self-Sufficiency (20%) - Direct command usage
4. Improvement Trend (15%) - Progress over time
5. Best Practices (5%) - Setup and configuration
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import statistics


class TokenCraftScorer:
    """Calculate token optimization scores."""

    # Scoring weights (total = 1000 points)
    # Updated to 100% Anthropic best practices alignment
    WEIGHTS = {
        "token_efficiency": 300,       # 30%
        "optimization_adoption": 325,  # 32.5% (increased - includes Anthropic best practices)
        "self_sufficiency": 200,       # 20%
        "improvement_trend": 125,      # 12.5%
        "best_practices": 50           # 5%
    }

    # Company baseline (can be updated from real data)
    # Updated to reflect real coding session usage (2026-02-12)
    DEFAULT_BASELINE = {
        "tokens_per_session": 30000,  # Realistic for coding sessions
        "tokens_per_message": 1500,
        "self_sufficiency_rate": 0.40,
        "optimization_adoption_rate": 0.30
    }

    def __init__(self, history_data: List[Dict], stats_data: Dict, baseline: Optional[Dict] = None):
        """
        Initialize scorer with user data.

        Args:
            history_data: Parsed history.jsonl data
            stats_data: Parsed stats-cache.json data
            baseline: Company baseline metrics (optional)
        """
        self.history_data = history_data
        self.stats_data = stats_data
        self.baseline = baseline or self.DEFAULT_BASELINE

        # Parse and prepare data
        self._prepare_data()

    def _prepare_data(self):
        """Parse history and stats into usable format."""
        # Calculate basic metrics
        self.sessions = self._group_by_sessions()
        self.total_sessions = len(self.sessions)
        self.total_messages = sum(len(s["messages"]) for s in self.sessions)

        # Calculate tokens
        self.total_tokens = self._calculate_total_tokens()
        self.avg_tokens_per_session = self.total_tokens / self.total_sessions if self.total_sessions > 0 else 0

        # Calculate dynamic baseline
        self.dynamic_baseline = self._calculate_dynamic_baseline()

    def _group_by_sessions(self) -> List[Dict]:
        """Group history data by session."""
        sessions = {}

        for entry in self.history_data:
            session_id = entry.get("sessionId", "unknown")

            if session_id not in sessions:
                sessions[session_id] = {
                    "session_id": session_id,
                    "messages": [],
                    "project": entry.get("project", "unknown"),
                    "timestamp": entry.get("timestamp")
                }

            sessions[session_id]["messages"].append(entry)

        return list(sessions.values())

    def _calculate_total_tokens(self) -> int:
        """Calculate total tokens from stats data."""
        total = 0

        # Support both old format ("models") and new format ("modelUsage")
        models_data = self.stats_data.get("models") or self.stats_data.get("modelUsage")

        if models_data:
            for model, data in models_data.items():
                if isinstance(data, dict):
                    total += data.get("inputTokens", 0)
                    total += data.get("outputTokens", 0)

        return total

    def _calculate_dynamic_baseline(self) -> float:
        """
        Calculate dynamic baseline from user's best performing sessions.

        Uses the best 25% of sessions (P25) and reduces by 10% as target.
        Falls back to fixed baseline if insufficient data (<10 sessions).

        Returns:
            Dynamic baseline in tokens per session
        """
        # Need at least 10 sessions for meaningful dynamic baseline
        if self.total_sessions < 10:
            return self.baseline["tokens_per_session"]

        # Calculate tokens per session for each session
        # We need to distribute total tokens across sessions proportionally
        if self.total_sessions == 0:
            return self.baseline["tokens_per_session"]

        # For now, use average as approximation
        # TODO: Track per-session tokens in history.jsonl for more accuracy
        session_tokens = []
        tokens_per_session_avg = self.avg_tokens_per_session

        # Simple model: assume roughly similar distribution
        # In future, enhance history.jsonl to track per-session tokens
        for session in self.sessions:
            # Estimate: distribute total tokens proportionally by message count
            if self.total_messages > 0:
                session_msg_count = len(session["messages"])
                estimated_tokens = (session_msg_count / self.total_messages) * self.total_tokens
                session_tokens.append(estimated_tokens)

        if not session_tokens:
            return self.baseline["tokens_per_session"]

        # Sort to find best performing sessions (lowest tokens)
        session_tokens_sorted = sorted(session_tokens)

        # Get P25 (best 25%)
        p25_index = len(session_tokens_sorted) // 4
        if p25_index == 0:
            p25_index = 1

        best_sessions = session_tokens_sorted[:p25_index]
        best_avg = statistics.mean(best_sessions)

        # Set baseline as 90% of best quartile (10% improvement target)
        dynamic_baseline = best_avg * 0.90

        # Don't set impossibly low baseline (min 15000 tokens - reasonable for any session)
        dynamic_baseline = max(15000, dynamic_baseline)

        # If dynamic baseline is unreasonably low compared to user average,
        # it means our estimation failed - use fixed baseline instead
        if dynamic_baseline < self.avg_tokens_per_session * 0.5:
            # Estimation failed, use fixed baseline
            return self.baseline["tokens_per_session"]

        # Don't set higher than fixed baseline (defeats purpose)
        dynamic_baseline = min(dynamic_baseline, self.baseline["tokens_per_session"])

        return round(dynamic_baseline, 0)

    def calculate_token_efficiency_score(self) -> Dict:
        """
        Calculate Token Efficiency score (30%, 300 points max).

        Compares user's average tokens/session against dynamic baseline.
        Uses tiered scoring for fairness:
        - < baseline: 300 pts (Excellent)
        - baseline - 1.5x: 200 pts (Good)
        - 1.5x - 2x: 100 pts (Average)
        - 2x - 3x: 50 pts (Needs Work)
        - > 3x: 0 pts (Poor)

        Returns:
            Dict with score details
        """
        # Use dynamic baseline (falls back to fixed if <10 sessions)
        baseline_avg = self.dynamic_baseline
        user_avg = self.avg_tokens_per_session
        using_dynamic = self.total_sessions >= 10

        if baseline_avg == 0 or user_avg == 0:
            # No data yet
            return {
                "score": 150,  # Neutral score
                "max_score": self.WEIGHTS["token_efficiency"],
                "percentage": 50.0,
                "user_avg": round(user_avg, 0),
                "baseline_avg": round(baseline_avg, 0),
                "baseline_type": "none",
                "tier": "no_data",
                "details": {
                    "total_sessions": self.total_sessions,
                    "total_tokens": self.total_tokens,
                    "avg_tokens_per_session": round(user_avg, 0)
                }
            }

        # Calculate ratio
        ratio = user_avg / baseline_avg

        # Tiered scoring
        if ratio <= 1.0:
            # At or below baseline - excellent!
            score = 300
            tier = "excellent"
        elif ratio <= 1.5:
            # Up to 1.5x baseline - good
            score = 200
            tier = "good"
        elif ratio <= 2.0:
            # Up to 2x baseline - average
            score = 100
            tier = "average"
        elif ratio <= 3.0:
            # Up to 3x baseline - needs work
            score = 50
            tier = "needs_work"
        else:
            # Over 3x baseline - poor
            score = 0
            tier = "poor"

        # Calculate improvement percentage
        improvement_pct = ((baseline_avg - user_avg) / baseline_avg) * 100

        return {
            "score": round(score, 1),
            "max_score": self.WEIGHTS["token_efficiency"],
            "percentage": round((score / self.WEIGHTS["token_efficiency"]) * 100, 1),
            "user_avg": round(user_avg, 0),
            "baseline_avg": round(baseline_avg, 0),
            "baseline_type": "dynamic" if using_dynamic else "fixed",
            "ratio": round(ratio, 2),
            "tier": tier,
            "improvement_pct": round(improvement_pct, 1),
            "details": {
                "total_sessions": self.total_sessions,
                "total_tokens": self.total_tokens,
                "avg_tokens_per_session": round(user_avg, 0)
            }
        }

    def calculate_optimization_adoption_score(self) -> Dict:
        """
        Calculate Optimization Adoption score (32.5%, 325 points max).

        Tracks usage of 8 Anthropic best practices over 90-day window:
        1. Defer documentation (50 points)
        2. Use CLAUDE.md (50 points)
        3. Concise response mode (40 points)
        4. Direct commands (60 points)
        5. Context management (50 points)
        6. XML tags usage (20 points) - Anthropic validated
        7. Chain of Thought (30 points) - Anthropic validated
        8. Examples usage (25 points) - Anthropic validated

        Returns:
            Dict with score breakdown
        """
        scores = {}
        total_score = 0

        # 1. Defer Documentation (50 points)
        defer_score = self._check_defer_documentation()
        scores["defer_docs"] = defer_score
        total_score += defer_score["score"]

        # 2. CLAUDE.md Usage (50 points)
        claude_md_score = self._check_claude_md_usage()
        scores["claude_md"] = claude_md_score
        total_score += claude_md_score["score"]

        # 3. Concise Response Mode (40 points)
        concise_score = self._check_concise_mode()
        scores["concise_mode"] = concise_score
        total_score += concise_score["score"]

        # 4. Direct Commands (60 points)
        direct_cmd_score = self._check_direct_commands()
        scores["direct_commands"] = direct_cmd_score
        total_score += direct_cmd_score["score"]

        # 5. Context Management (50 points)
        context_score = self._check_context_management()
        scores["context_mgmt"] = context_score
        total_score += context_score["score"]

        # 6. XML Tags Usage (20 points) - NEW
        xml_score = self._check_xml_usage()
        scores["xml_tags"] = xml_score
        total_score += xml_score["score"]

        # 7. Chain of Thought (30 points) - NEW
        cot_score = self._check_chain_of_thought()
        scores["chain_of_thought"] = cot_score
        total_score += cot_score["score"]

        # 8. Examples Usage (25 points) - NEW
        examples_score = self._check_examples_usage()
        scores["examples"] = examples_score
        total_score += examples_score["score"]

        return {
            "score": round(total_score, 1),
            "max_score": self.WEIGHTS["optimization_adoption"],
            "percentage": round((total_score / self.WEIGHTS["optimization_adoption"]) * 100, 1),
            "breakdown": scores
        }

    def _check_defer_documentation(self) -> Dict:
        """Check if user defers documentation until ready to push."""
        # Heuristic: Look for documentation keywords in messages
        doc_keywords = ["readme", "documentation", "comment", "docstring", "docs"]
        defer_keywords = ["defer", "later", "skip", "wait", "after"]

        doc_sessions = 0
        deferred_sessions = 0

        for session in self.sessions:
            has_doc_request = False
            has_defer = False

            for msg in session["messages"]:
                content = msg.get("message", "").lower()

                if any(kw in content for kw in doc_keywords):
                    has_doc_request = True

                if any(kw in content for kw in defer_keywords):
                    has_defer = True

            if has_doc_request:
                doc_sessions += 1
                if has_defer:
                    deferred_sessions += 1

        consistency = deferred_sessions / doc_sessions if doc_sessions > 0 else 0.5
        score = self._calculate_tier_score(consistency, max_points=50)

        return {
            "score": score,
            "max_score": 50,
            "consistency": round(consistency * 100, 1),
            "opportunities": doc_sessions,
            "used": deferred_sessions
        }

    def _check_claude_md_usage(self) -> Dict:
        """Check if CLAUDE.md exists in top projects."""
        # Get top 3 projects by usage
        project_counts = {}
        for session in self.sessions:
            project = session["project"]
            project_counts[project] = project_counts.get(project, 0) + 1

        top_projects = sorted(project_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        # Check for CLAUDE.md in each project
        projects_with_claude_md = 0
        for project, _ in top_projects:
            claude_md_path = Path(project) / "CLAUDE.md"
            if claude_md_path.exists():
                projects_with_claude_md += 1

        consistency = projects_with_claude_md / len(top_projects) if top_projects else 0
        score = self._calculate_tier_score(consistency, max_points=50)

        return {
            "score": score,
            "max_score": 50,
            "consistency": round(consistency * 100, 1),
            "top_projects": len(top_projects),
            "with_claude_md": projects_with_claude_md
        }

    def _check_concise_mode(self) -> Dict:
        """Check for concise response preference."""
        # Heuristic: Check MEMORY.md or CLAUDE.md for concise preference
        memory_md_path = Path.home() / ".claude" / "memory" / "MEMORY.md"

        has_concise_preference = False
        if memory_md_path.exists():
            content = memory_md_path.read_text().lower()
            if "concise" in content or "brief" in content or "short" in content:
                has_concise_preference = True

        # Also check average message length
        if self.total_messages > 0:
            avg_msg_length = sum(
                len(msg.get("message", ""))
                for session in self.sessions
                for msg in session["messages"]
            ) / self.total_messages

            # If average message is under 200 chars, consider concise
            if avg_msg_length < 200:
                has_concise_preference = True

        consistency = 1.0 if has_concise_preference else 0.3
        score = self._calculate_tier_score(consistency, max_points=40)

        return {
            "score": score,
            "max_score": 40,
            "consistency": round(consistency * 100, 1),
            "preference_set": has_concise_preference
        }

    def _check_direct_commands(self) -> Dict:
        """Check how often user runs commands directly vs asking AI."""
        # Heuristic: Count tool calls vs opportunities
        # This is simplified - in production, track actual command opportunities

        # Count Read/Bash tool calls (these could be done directly)
        ai_command_count = 0
        for session in self.sessions:
            for msg in session["messages"]:
                # Check if AI was asked to run simple commands
                content = msg.get("message", "").lower()
                simple_cmds = ["git log", "git status", "cat ", "ls ", "grep ", "show me"]

                if any(cmd in content for cmd in simple_cmds):
                    ai_command_count += 1

        # Estimate opportunities (rough heuristic)
        total_opportunities = self.total_sessions * 2  # Assume 2 opportunities per session
        direct_commands = max(0, total_opportunities - ai_command_count)

        consistency = direct_commands / total_opportunities if total_opportunities > 0 else 0.5
        score = self._calculate_tier_score(consistency, max_points=60)

        return {
            "score": score,
            "max_score": 60,
            "consistency": round(consistency * 100, 1),
            "opportunities": total_opportunities,
            "direct_commands": direct_commands,
            "ai_commands": ai_command_count
        }

    def _check_context_management(self) -> Dict:
        """Check for good context management practices."""
        # Heuristic: Check session length and message count
        if self.total_sessions == 0:
            return {"score": 25, "max_score": 50, "consistency": 50.0}

        avg_messages_per_session = self.total_messages / self.total_sessions

        # Good: 5-15 messages per session (focused)
        # Too short (<5): Not using AI effectively
        # Too long (>20): Context bloat

        if 5 <= avg_messages_per_session <= 15:
            consistency = 1.0
        elif avg_messages_per_session < 5:
            consistency = 0.6
        else:  # > 15
            consistency = max(0.3, 1.0 - ((avg_messages_per_session - 15) / 50))

        score = self._calculate_tier_score(consistency, max_points=50)

        return {
            "score": score,
            "max_score": 50,
            "consistency": round(consistency * 100, 1),
            "avg_messages_per_session": round(avg_messages_per_session, 1)
        }

    def _check_xml_usage(self) -> Dict:
        """
        Check for XML tag usage in prompts (Anthropic best practice).

        Anthropic recommends structuring prompts with XML tags like:
        <document>, <task>, <context>, <example>, etc.
        """
        xml_keywords = ["<document>", "<task>", "<context>", "<example>", "<input>", "<output>", "</"]

        xml_sessions = 0
        for session in self.sessions:
            for msg in session["messages"]:
                content = msg.get("message", "")
                if any(kw in content for kw in xml_keywords):
                    xml_sessions += 1
                    break  # Count session once

        consistency = xml_sessions / self.total_sessions if self.total_sessions > 0 else 0
        score = self._calculate_tier_score(consistency, max_points=20)

        return {
            "score": score,
            "max_score": 20,
            "consistency": round(consistency * 100, 1),
            "sessions_with_xml": xml_sessions,
            "total_sessions": self.total_sessions,
            "benefit": "XML tags improve prompt structure and clarity"
        }

    def _check_chain_of_thought(self) -> Dict:
        """
        Check for Chain of Thought usage (Anthropic best practice).

        Anthropic recommends using CoT prompts like:
        "let's think step by step", "reasoning:", "because", etc.
        """
        cot_keywords = ["let's think", "step by step", "reasoning:", "because", "first", "then", "therefore", "analyze"]

        cot_sessions = 0
        for session in self.sessions:
            for msg in session["messages"]:
                content = msg.get("message", "").lower()
                if any(kw in content for kw in cot_keywords):
                    cot_sessions += 1
                    break  # Count session once

        consistency = cot_sessions / self.total_sessions if self.total_sessions > 0 else 0
        score = self._calculate_tier_score(consistency, max_points=30)

        return {
            "score": score,
            "max_score": 30,
            "consistency": round(consistency * 100, 1),
            "sessions_with_cot": cot_sessions,
            "total_sessions": self.total_sessions,
            "benefit": "Chain of Thought improves reasoning quality and accuracy"
        }

    def _check_examples_usage(self) -> Dict:
        """
        Check for examples/few-shot prompting (Anthropic best practice).

        Anthropic recommends providing examples like:
        "for example", "e.g.", "such as", "like this:", etc.
        """
        example_keywords = ["for example", "e.g.", "such as", "like this:", "here's an example", "example:"]

        example_sessions = 0
        for session in self.sessions:
            for msg in session["messages"]:
                content = msg.get("message", "").lower()
                if any(kw in content for kw in example_keywords):
                    example_sessions += 1
                    break  # Count session once

        consistency = example_sessions / self.total_sessions if self.total_sessions > 0 else 0
        score = self._calculate_tier_score(consistency, max_points=25)

        return {
            "score": score,
            "max_score": 25,
            "consistency": round(consistency * 100, 1),
            "sessions_with_examples": example_sessions,
            "total_sessions": self.total_sessions,
            "benefit": "Examples improve output quality and reduce iterations"
        }

    def _calculate_tier_score(self, consistency: float, max_points: int) -> float:
        """
        Calculate smooth sliding scale score based on consistency rate.

        Provides gradual increases for better progress visibility.
        Users see improvement every 5-10% instead of big jumps.

        Scoring curves:
        - 90-100%: Full points (100%)
        - 70-89%: Interpolated 85-100%
        - 50-69%: Interpolated 65-85%
        - 30-49%: Interpolated 40-65%
        - 0-29%: Linear from 0%
        """
        if consistency >= 0.90:
            # Excellent - full points
            return max_points
        elif consistency >= 0.70:
            # Good - interpolate between 85% and 100%
            ratio = (consistency - 0.70) / 0.20
            return max_points * (0.85 + (0.15 * ratio))
        elif consistency >= 0.50:
            # Average - interpolate between 65% and 85%
            ratio = (consistency - 0.50) / 0.20
            return max_points * (0.65 + (0.20 * ratio))
        elif consistency >= 0.30:
            # Below average - interpolate between 40% and 65%
            ratio = (consistency - 0.30) / 0.20
            return max_points * (0.40 + (0.25 * ratio))
        else:
            # Poor - linear from 0 to 40%
            return max_points * (consistency / 0.30) * 0.40

    def calculate_self_sufficiency_score(self) -> Dict:
        """
        Calculate Self-Sufficiency score (20%, 200 points max).

        Measures how often user runs commands directly vs asking AI.

        Returns:
            Dict with score details
        """
        # This overlaps with direct_commands check in optimization_adoption
        # Use that data
        direct_cmd_data = self._check_direct_commands()

        consistency = direct_cmd_data["consistency"] / 100
        score = consistency * self.WEIGHTS["self_sufficiency"]

        return {
            "score": round(score, 1),
            "max_score": self.WEIGHTS["self_sufficiency"],
            "percentage": round((score / self.WEIGHTS["self_sufficiency"]) * 100, 1),
            "rate": round(consistency, 2),
            "details": direct_cmd_data
        }

    def calculate_improvement_trend_score(self, previous_snapshot: Optional[Dict] = None) -> Dict:
        """
        Calculate Improvement Trend score (12.5%, 125 points max).

        Includes warm-up period for new users (<10 sessions).
        Compares rolling windows for established users.

        Args:
            previous_snapshot: Previous snapshot data for comparison

        Returns:
            Dict with score details
        """
        # Warm-up period for new users (<10 sessions)
        if self.total_sessions < 10:
            return {
                "score": 50,
                "max_score": self.WEIGHTS["improvement_trend"],
                "percentage": 40.0,
                "improvement_pct": 0,
                "status": "warming_up",
                "message": f"Session {self.total_sessions}/10 - Establishing baseline"
            }

        if not previous_snapshot:
            # No previous data, give baseline score
            return {
                "score": 50,
                "max_score": self.WEIGHTS["improvement_trend"],
                "percentage": 40.0,
                "improvement_pct": 0,
                "status": "baseline",
                "message": "No previous snapshot for comparison"
            }

        # Compare token efficiency
        prev_avg = previous_snapshot.get("avg_tokens_per_session", self.baseline["tokens_per_session"])
        current_avg = self.avg_tokens_per_session

        if prev_avg == 0:
            improvement_pct = 0
        else:
            improvement_pct = ((prev_avg - current_avg) / prev_avg) * 100

        # Score based on improvement
        if improvement_pct >= 10:
            score = 150
            status = "excellent"
        elif improvement_pct >= 5:
            score = 100
            status = "good"
        elif improvement_pct >= 2:
            score = 50
            status = "modest"
        elif improvement_pct >= 0:
            score = 20
            status = "maintaining"
        elif improvement_pct >= -5:
            score = 0
            status = "slight_degradation"
        else:
            score = 0
            status = "significant_degradation"

        return {
            "score": score,
            "max_score": self.WEIGHTS["improvement_trend"],
            "percentage": round((score / self.WEIGHTS["improvement_trend"]) * 100, 1),
            "improvement_pct": round(improvement_pct, 1),
            "status": status,
            "prev_avg": round(prev_avg, 0),
            "current_avg": round(current_avg, 0)
        }

    def calculate_best_practices_score(self) -> Dict:
        """
        Calculate Best Practices score (5%, 50 points max).

        Checks:
        - CLAUDE.md in top 3 projects (30 points)
        - Memory.md has optimizations (10 points)
        - Uses appropriate tooling (10 points)

        Returns:
            Dict with score details
        """
        checks = {}
        total_score = 0

        # 1. CLAUDE.md in top projects
        claude_md_data = self._check_claude_md_usage()
        claude_md_score = (claude_md_data["with_claude_md"] / max(1, claude_md_data["top_projects"])) * 30
        checks["claude_md_setup"] = {
            "score": round(claude_md_score, 1),
            "max_score": 30,
            "projects_with_setup": claude_md_data["with_claude_md"],
            "top_projects": claude_md_data["top_projects"]
        }
        total_score += claude_md_score

        # 2. Memory.md optimizations
        memory_md_path = Path.home() / ".claude" / "memory" / "MEMORY.md"
        has_optimizations = False

        if memory_md_path.exists():
            content = memory_md_path.read_text().lower()
            opt_keywords = ["optimization", "defer", "efficiency", "token", "concise"]
            if any(kw in content for kw in opt_keywords):
                has_optimizations = True

        memory_score = 10 if has_optimizations else 0
        checks["memory_md_optimizations"] = {
            "score": memory_score,
            "max_score": 10,
            "has_optimizations": has_optimizations
        }
        total_score += memory_score

        # 3. Appropriate tooling
        # Give 10 points as baseline (assumes using token-craft tool)
        checks["tooling"] = {
            "score": 10,
            "max_score": 10,
            "using_token_craft": True
        }
        total_score += 10

        return {
            "score": round(total_score, 1),
            "max_score": self.WEIGHTS["best_practices"],
            "percentage": round((total_score / self.WEIGHTS["best_practices"]) * 100, 1),
            "checks": checks
        }

    def calculate_total_score(self, previous_snapshot: Optional[Dict] = None) -> Dict:
        """
        Calculate total score across all categories.

        Args:
            previous_snapshot: Previous snapshot for trend calculation

        Returns:
            Complete score breakdown
        """
        # Calculate each category
        token_efficiency = self.calculate_token_efficiency_score()
        optimization_adoption = self.calculate_optimization_adoption_score()
        self_sufficiency = self.calculate_self_sufficiency_score()
        improvement_trend = self.calculate_improvement_trend_score(previous_snapshot)
        best_practices = self.calculate_best_practices_score()

        # Sum total score
        total_score = (
            token_efficiency["score"] +
            optimization_adoption["score"] +
            self_sufficiency["score"] +
            improvement_trend["score"] +
            best_practices["score"]
        )

        return {
            "total_score": round(total_score, 1),
            "max_possible": 1000,
            "percentage": round((total_score / 1000) * 100, 1),
            "breakdown": {
                "token_efficiency": token_efficiency,
                "optimization_adoption": optimization_adoption,
                "self_sufficiency": self_sufficiency,
                "improvement_trend": improvement_trend,
                "best_practices": best_practices
            },
            "calculated_at": datetime.now().isoformat()
        }
