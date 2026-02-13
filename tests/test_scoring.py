"""
Unit tests for Token-Craft scoring engine.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from token_craft.scoring_engine import TokenCraftScorer
from token_craft.rank_system import SpaceRankSystem


class TestSpaceRankSystem(unittest.TestCase):
    """Test rank system."""

    def test_get_rank_cadet(self):
        """Test Cadet rank."""
        rank = SpaceRankSystem.get_rank(100)
        self.assertEqual(rank["name"], "Cadet")
        self.assertEqual(rank["min"], 0)
        self.assertEqual(rank["max"], 199)

    def test_get_rank_pilot(self):
        """Test Pilot rank."""
        rank = SpaceRankSystem.get_rank(250)
        self.assertEqual(rank["name"], "Pilot")

    def test_get_rank_legend(self):
        """Test Galactic Legend rank."""
        rank = SpaceRankSystem.get_rank(1500)
        self.assertEqual(rank["name"], "Galactic Legend")

    def test_get_next_rank(self):
        """Test next rank calculation."""
        next_rank = SpaceRankSystem.get_next_rank(150)
        self.assertEqual(next_rank["name"], "Pilot")
        self.assertEqual(next_rank["points_needed"], 50)

    def test_get_next_rank_max(self):
        """Test next rank at max level."""
        next_rank = SpaceRankSystem.get_next_rank(1500)
        self.assertIsNone(next_rank)

    def test_progress_bar(self):
        """Test progress bar generation."""
        bar = SpaceRankSystem.get_progress_bar(100, width=10)
        self.assertEqual(len(bar), 10)
        self.assertIn("█", bar)
        self.assertIn("░", bar)

    def test_rank_level(self):
        """Test numeric rank level."""
        level = SpaceRankSystem.calculate_rank_level(100)
        self.assertEqual(level, 1)  # Cadet

        level = SpaceRankSystem.calculate_rank_level(500)
        self.assertEqual(level, 3)  # Navigator


class TestTokenCraftScorer(unittest.TestCase):
    """Test scoring engine."""

    def setUp(self):
        """Set up test data."""
        self.history_data = [
            {
                "sessionId": "session1",
                "project": "/test/project",
                "message": "test message",
                "timestamp": "2026-02-12T10:00:00Z"
            },
            {
                "sessionId": "session1",
                "project": "/test/project",
                "message": "another message",
                "timestamp": "2026-02-12T10:05:00Z"
            }
        ]

        self.stats_data = {
            "models": {
                "claude-sonnet-4.5": {
                    "inputTokens": 50000,
                    "outputTokens": 30000
                }
            }
        }

    def test_scorer_initialization(self):
        """Test scorer initialization."""
        scorer = TokenCraftScorer(self.history_data, self.stats_data)
        self.assertIsNotNone(scorer)
        self.assertEqual(scorer.total_sessions, 1)
        self.assertEqual(scorer.total_tokens, 80000)

    def test_token_efficiency_score(self):
        """Test token efficiency calculation."""
        scorer = TokenCraftScorer(self.history_data, self.stats_data)
        score_data = scorer.calculate_token_efficiency_score()

        self.assertIn("score", score_data)
        self.assertIn("max_score", score_data)
        self.assertIn("percentage", score_data)
        self.assertEqual(score_data["max_score"], 350)

    def test_optimization_adoption_score(self):
        """Test optimization adoption calculation."""
        scorer = TokenCraftScorer(self.history_data, self.stats_data)
        score_data = scorer.calculate_optimization_adoption_score()

        self.assertIn("score", score_data)
        self.assertEqual(score_data["max_score"], 250)
        self.assertIn("breakdown", score_data)

    def test_self_sufficiency_score(self):
        """Test self-sufficiency calculation."""
        scorer = TokenCraftScorer(self.history_data, self.stats_data)
        score_data = scorer.calculate_self_sufficiency_score()

        self.assertIn("score", score_data)
        self.assertEqual(score_data["max_score"], 200)

    def test_best_practices_score(self):
        """Test best practices calculation."""
        scorer = TokenCraftScorer(self.history_data, self.stats_data)
        score_data = scorer.calculate_best_practices_score()

        self.assertIn("score", score_data)
        self.assertEqual(score_data["max_score"], 50)

    def test_total_score(self):
        """Test total score calculation."""
        scorer = TokenCraftScorer(self.history_data, self.stats_data)
        score_data = scorer.calculate_total_score()

        self.assertIn("total_score", score_data)
        self.assertIn("max_possible", score_data)
        self.assertEqual(score_data["max_possible"], 1000)
        self.assertIn("breakdown", score_data)

        # Check all categories present
        self.assertIn("token_efficiency", score_data["breakdown"])
        self.assertIn("optimization_adoption", score_data["breakdown"])
        self.assertIn("self_sufficiency", score_data["breakdown"])
        self.assertIn("improvement_trend", score_data["breakdown"])
        self.assertIn("best_practices", score_data["breakdown"])


if __name__ == "__main__":
    unittest.main()
