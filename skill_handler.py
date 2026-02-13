"""
Token-Craft Skill Handler

Main entry point for the /token-craft skill.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Optional

# Add token_craft to path
sys.path.insert(0, str(Path(__file__).parent))

from token_craft.scoring_engine import TokenCraftScorer
from token_craft.rank_system import SpaceRankSystem
from token_craft.user_profile import UserProfile
from token_craft.snapshot_manager import SnapshotManager
from token_craft.delta_calculator import DeltaCalculator
from token_craft.report_generator import ReportGenerator


class TokenCraftHandler:
    """Main handler for Token-Craft skill."""

    def __init__(self):
        """Initialize handler."""
        self.claude_dir = Path.home() / ".claude"
        self.history_file = self.claude_dir / "history.jsonl"
        self.stats_file = self.claude_dir / "stats-cache.json"

        self.profile = UserProfile()
        self.snapshot_manager = SnapshotManager()
        self.report_generator = ReportGenerator()

    def load_data(self) -> tuple:
        """
        Load history and stats data.

        Returns:
            Tuple of (history_data, stats_data)
        """
        # Load history.jsonl
        history_data = []
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                history_data.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                print(f"Warning: Could not load history.jsonl: {e}")

        # Load stats-cache.json
        stats_data = {}
        if self.stats_file.exists():
            try:
                with open(self.stats_file, "r", encoding="utf-8") as f:
                    stats_data = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load stats-cache.json: {e}")

        return history_data, stats_data

    def calculate_scores(self, history_data: list, stats_data: Dict, previous_snapshot: Optional[Dict] = None) -> Dict:
        """
        Calculate user scores.

        Args:
            history_data: Parsed history.jsonl
            stats_data: Parsed stats-cache.json
            previous_snapshot: Previous snapshot for trend calculation

        Returns:
            Score data
        """
        scorer = TokenCraftScorer(history_data, stats_data)
        score_data = scorer.calculate_total_score(previous_snapshot)

        return score_data

    def run(self, mode: str = "full") -> str:
        """
        Run the Token-Craft analysis.

        Args:
            mode: 'full', 'summary', or 'quick'

        Returns:
            Formatted report
        """
        try:
            # Load data
            print("Loading your data...")
            history_data, stats_data = self.load_data()

            if not history_data:
                return "No history data found. Start using Claude Code to track your progress!"

            # Get previous snapshot for comparison
            previous_snapshot = self.snapshot_manager.get_latest_snapshot()

            # Calculate scores
            print("Calculating your scores...")
            previous_profile = None
            if previous_snapshot and isinstance(previous_snapshot, dict):
                previous_profile = previous_snapshot.get("profile")

            score_data = self.calculate_scores(
                history_data,
                stats_data,
                previous_profile
            )

            # Get rank
            rank_data = SpaceRankSystem.get_rank(score_data["total_score"])

            # Calculate delta if we have previous data
            delta_data = None
            if previous_snapshot:
                current_snapshot = {
                    "timestamp": score_data["calculated_at"],
                    "profile": self.profile.get_current_state(),
                    "scores": score_data,
                    "rank": rank_data
                }
                delta_data = DeltaCalculator.calculate_delta(current_snapshot, previous_snapshot)

            # Update profile
            self.profile.update_from_analysis(score_data, rank_data)

            # Check for achievements
            self._check_achievements(score_data, rank_data, delta_data)

            # Save profile
            self.profile.save()

            # Create snapshot
            print("Saving snapshot...")
            self.snapshot_manager.create_snapshot(
                self.profile.get_current_state(),
                score_data,
                rank_data
            )

            # Generate report
            print("Generating report...")
            if mode == "summary":
                report = self.report_generator.generate_summary(
                    self.profile.get_current_state(),
                    score_data,
                    rank_data
                )
            elif mode == "quick":
                report = self._generate_quick_status(score_data, rank_data)
            else:  # full
                report = self.report_generator.generate_full_report(
                    self.profile.get_current_state(),
                    score_data,
                    rank_data,
                    delta_data
                )

            return report

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return f"Error running Token-Craft: {e}\n\nDetails:\n{error_details}\n\nPlease report this issue."

    def _check_achievements(self, score_data: Dict, rank_data: Dict, delta_data: Optional[Dict]):
        """Check and award achievements."""
        # First rank achievement
        if rank_data["name"] == "Pilot" and not any(a["id"] == "first_pilot" for a in self.profile.get_achievements()):
            self.profile.add_achievement(
                "first_pilot",
                "First Pilot",
                "Achieved Pilot rank for the first time"
            )

        # Score milestones
        score = score_data["total_score"]
        if score >= 500 and not any(a["id"] == "halfway_there" for a in self.profile.get_achievements()):
            self.profile.add_achievement(
                "halfway_there",
                "Halfway There",
                "Reached 500 points"
            )

        if score >= 1000 and not any(a["id"] == "four_digits" for a in self.profile.get_achievements()):
            self.profile.add_achievement(
                "four_digits",
                "Four Digits",
                "Reached 1000+ points (Admiral level)"
            )

        # Efficiency achievement
        efficiency_pct = score_data["breakdown"]["token_efficiency"].get("improvement_pct", 0)
        if efficiency_pct >= 30 and not any(a["id"] == "efficiency_master" for a in self.profile.get_achievements()):
            self.profile.add_achievement(
                "efficiency_master",
                "Efficiency Master",
                "Achieved 30%+ better efficiency than baseline"
            )

        # Promotion achievement
        if delta_data and isinstance(delta_data, dict):
            rank_change = delta_data.get("rank_change")
            if rank_change and isinstance(rank_change, dict) and rank_change.get("promoted"):
                promo_id = f"promoted_to_{rank_data['name'].lower()}"
                if not any(a["id"] == promo_id for a in self.profile.get_achievements()):
                    self.profile.add_achievement(
                        promo_id,
                        f"Promoted to {rank_data['name']}",
                        f"Achieved {rank_data['name']} rank"
                    )

    def _generate_quick_status(self, score_data: Dict, rank_data: Dict) -> str:
        """Generate quick one-line status."""
        next_rank = SpaceRankSystem.get_next_rank(score_data["total_score"])

        status = f"{rank_data['icon']} {rank_data['name']} - {score_data['total_score']:.0f} points"

        if next_rank:
            status += f" ({next_rank['points_needed']} to {next_rank['name']})"

        return status


def main():
    """Main entry point."""
    import argparse
    import sys
    import io

    # Fix Windows CMD encoding issues
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description="Token-Craft: Master LLM efficiency")
    parser.add_argument(
        "--mode",
        choices=["full", "summary", "quick"],
        default="full",
        help="Report mode (default: full)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of formatted report"
    )

    args = parser.parse_args()

    handler = TokenCraftHandler()
    report = handler.run(mode=args.mode)

    if args.json and args.mode == "full":
        # Return JSON for programmatic access
        output = {
            "profile": handler.profile.get_current_state(),
            "report": report
        }
        print(json.dumps(output, indent=2))
    else:
        print(report)


if __name__ == "__main__":
    main()
