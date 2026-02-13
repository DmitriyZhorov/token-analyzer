# Token-Craft Implementation Plan

## Final Spec Summary

**Theme:** Space Exploration
**Ranks:** Cadet → Pilot → Navigator → Commander → Captain → Admiral → Galactic Legend
**Levels:** 7 (score ranges: 0-199, 200-399, 400-599, 600-799, 800-999, 1000-1199, 1200+)

**Scoring:**
- Token Efficiency: 35% (350 points)
- Optimization Adoption: 25% (250 points)
- Self-Sufficiency: 20% (200 points)
- Improvement Trend: 15% (150 points)
- Best Practices: 5% (50 points)
- **Total: 1000 points base + 200 bonus**

**Gamification:**
- Badges (no cash bonuses)
- Leaderboards (company/project/department)
- hero.epam.com integration
- Certifications

---

## Implementation Phases

### Phase 1: Core Scoring Engine ✅ START HERE
**Goal:** Calculate scores from existing data

**Files to create:**
1. `scoring_engine.py` - Core scoring calculations
2. `rank_system.py` - Rank determination and progression
3. `user_profile.py` - User state management
4. `test_scoring.py` - Unit tests for scoring

**Dependencies:**
- Uses existing `analyze_tokens_v2.py` data structures
- Reads from `~/.claude/history.jsonl` and `stats-cache.json`

**Timeline:** 2-3 hours

---

### Phase 2: Data Storage & Snapshots
**Goal:** Track progress over time

**Files to create:**
1. `snapshot_manager.py` - Save/load snapshots
2. `delta_calculator.py` - Compare snapshots for trends
3. Setup `~/.claude/token-craft/` directory structure

**Directory structure:**
```
~/.claude/token-craft/
├── snapshots/
│   ├── snapshot_20260212_120000.json
│   └── ...
├── user_profile.json
├── achievements.json
└── config.json
```

**Timeline:** 1-2 hours

---

### Phase 3: Visualization & Reporting
**Goal:** Show user their stats and progress

**Files to create:**
1. `report_generator.py` - Format output beautifully
2. `progress_visualizer.py` - ASCII progress bars, charts
3. `recommendation_engine.py` - Personalized suggestions

**Output example:**
```
========================================================
TOKEN-CRAFT: YOUR SPACE MISSION REPORT
========================================================

Current Rank: [COMMANDER] ████████████░░░ 685/800
Next Rank:    [CAPTAIN] in 115 points

Token Efficiency:     [████████░░] 177/350 (51%)
Optimization Adoption: [████████░░] 218/250 (87%)
Self-Sufficiency:     [██████░░░░] 128/200 (64%)
Improvement Trend:    [██████████] 150/150 (100%)
Best Practices:       [████████░░] 40/50 (80%)

Your Mission Stats:
- Sessions this month: 45
- Avg tokens/session: 11,200 (25% better than baseline!)
- Estimated cost: $35.50 (29% under budget)
- Rank achieved: 2026-01-15

Top Optimization Opportunity:
► Increase self-sufficiency to 75% → +50 points
  Run commands directly: git status, ls, cat
  Estimated impact: Captain rank in 2 months

Leaderboard Position:
- Company-wide: #47 of 256 (top 18%)
- Project (managed-services-dashboard): #2 of 8
- Department (Engineering): #12 of 89
```

**Timeline:** 2-3 hours

---

### Phase 4: Claude Skill Integration
**Goal:** Make it a `/token-craft` command

**Files to create:**
1. `token-craft.md` - Skill definition (YAML + markdown)
2. `skill_handler.py` - Entry point for skill
3. Update existing scripts to be callable by skill

**Skill structure:**
```markdown
---
name: token-craft
description: Master LLM efficiency through space exploration ranks
version: 1.0.0
triggers:
  - /token-craft
  - /tc
permissions:
  - read: ~/.claude/history.jsonl
  - read: ~/.claude/stats-cache.json
  - write: ~/.claude/token-craft/
  - execute: python
---

# Token-Craft Skill

[Instructions for Claude on how to use the skill...]
```

**Timeline:** 2-3 hours

---

### Phase 5: Team Features
**Goal:** Leaderboards and collaboration

**Files to create:**
1. `leaderboard_generator.py` - Create rankings
2. `team_export.py` - Export for team repo (enhance existing)
3. `team_aggregator_v2.py` - Aggregate with new scoring

**Features:**
- Company-wide anonymous leaderboard
- Project-level leaderboards
- Department leaderboards
- Export snapshots to git repo
- Privacy controls

**Timeline:** 3-4 hours

---

### Phase 6: hero.epam.com Integration
**Goal:** Badge issuance and certification

**Files to create:**
1. `hero_api_client.py` - API integration
2. `badge_issuer.py` - Issue badges based on rank
3. `certification_generator.py` - Generate cert files

**API endpoints (to be defined with EPAM):**
```python
POST /api/badges/issue
{
  "user_email": "dmitriy_zhorov@epam.com",
  "badge_id": "token_craft_commander",
  "issued_date": "2026-02-12",
  "evidence": {...}
}
```

**Timeline:** 2-3 hours (+ EPAM API setup time)

---

### Phase 7: Advanced Features
**Goal:** Polish and enhancement

**Features:**
1. Achievement system (first optimization, 100 sessions, etc.)
2. Mentorship matching (connect Admirals with Cadets)
3. Challenge system (monthly efficiency challenges)
4. Integration with `/insights` command
5. Automated weekly reports
6. Degradation warnings (rank about to drop)

**Timeline:** 4-6 hours

---

## Total Implementation Timeline

| Phase | Time Estimate | Priority |
|-------|---------------|----------|
| Phase 1: Core Scoring | 2-3 hours | 🔴 Critical |
| Phase 2: Snapshots | 1-2 hours | 🔴 Critical |
| Phase 3: Visualization | 2-3 hours | 🔴 Critical |
| Phase 4: Skill Integration | 2-3 hours | 🟡 High |
| Phase 5: Team Features | 3-4 hours | 🟡 High |
| Phase 6: hero.epam.com | 2-3 hours | 🟢 Medium |
| Phase 7: Advanced | 4-6 hours | 🟢 Nice-to-have |
| **TOTAL** | **16-24 hours** | |

**MVP (Phases 1-4):** 7-11 hours
**Full Launch (Phases 1-6):** 12-18 hours
**Complete (All phases):** 16-24 hours

---

## Implementation Order (Detailed)

### Step 1: Core Scoring Engine

**Create: `scoring_engine.py`**
```python
class TokenCraftScorer:
    def __init__(self, history_data, stats_data, company_baseline):
        """Initialize with user's data and company baseline."""

    def calculate_token_efficiency_score(self) -> float:
        """35% weight, 350 points max."""

    def calculate_optimization_adoption_score(self) -> float:
        """25% weight, 250 points max."""

    def calculate_self_sufficiency_score(self) -> float:
        """20% weight, 200 points max."""

    def calculate_improvement_trend_score(self) -> float:
        """15% weight, 150 points max."""

    def calculate_best_practices_score(self) -> float:
        """5% weight, 50 points max."""

    def calculate_total_score(self) -> dict:
        """Return complete breakdown."""
```

**Create: `rank_system.py`**
```python
class SpaceRankSystem:
    RANKS = [
        {"name": "Cadet", "min": 0, "max": 199},
        {"name": "Pilot", "min": 200, "max": 399},
        {"name": "Navigator", "min": 400, "max": 599},
        {"name": "Commander", "min": 600, "max": 799},
        {"name": "Captain", "min": 800, "max": 999},
        {"name": "Admiral", "min": 1000, "max": 1199},
        {"name": "Galactic Legend", "min": 1200, "max": 9999},
    ]

    def get_rank(self, score: int) -> dict:
        """Get current rank info."""

    def get_next_rank(self, score: int) -> dict:
        """Get next rank and points needed."""

    def get_progress_bar(self, score: int, width: int = 50) -> str:
        """Generate ASCII progress bar."""
```

**Create: `user_profile.py`**
```python
class UserProfile:
    def __init__(self, user_email: str):
        """Load or create user profile."""

    def update_from_analysis(self, analysis_data: dict):
        """Update profile with new analysis."""

    def save(self):
        """Save to ~/.claude/token-craft/user_profile.json."""

    def get_current_state(self) -> dict:
        """Get complete current state."""
```

---

### Step 2: Create Snapshot System

**Create: `snapshot_manager.py`**
```python
class SnapshotManager:
    SNAPSHOT_DIR = Path.home() / ".claude" / "token-craft" / "snapshots"

    def create_snapshot(self, profile_data: dict) -> str:
        """Create timestamped snapshot, return filename."""

    def get_latest_snapshot(self) -> dict:
        """Get most recent snapshot."""

    def get_snapshot(self, timestamp: str) -> dict:
        """Get specific snapshot by timestamp."""

    def list_snapshots(self) -> list:
        """List all available snapshots."""
```

**Create: `delta_calculator.py`**
```python
class DeltaCalculator:
    def calculate_delta(self, current: dict, previous: dict) -> dict:
        """Calculate changes between snapshots."""

    def format_delta(self, delta: dict) -> str:
        """Format delta for display (↑↓ indicators)."""
```

---

### Step 3: Visualization

**Create: `report_generator.py`**
```python
class ReportGenerator:
    def generate_full_report(self, profile: UserProfile) -> str:
        """Generate complete mission report."""

    def generate_summary(self, profile: UserProfile) -> str:
        """Generate quick summary."""

    def generate_recommendations(self, profile: UserProfile) -> list:
        """Generate personalized recommendations."""
```

**Create: `progress_visualizer.py`**
```python
def create_progress_bar(current: int, maximum: int, width: int = 50) -> str:
    """Create ASCII progress bar."""

def create_rank_badge(rank_name: str) -> str:
    """Create ASCII art rank badge."""

def create_trend_indicator(delta: float) -> str:
    """Create trend arrow (↑↓→)."""
```

---

### Step 4: Skill Definition

**Create: `token-craft.md`**
```markdown
---
name: token-craft
description: Master LLM efficiency through space exploration
version: 1.0.0
triggers:
  - /token-craft
  - /tc
---

# Token-Craft Skill Instructions

When the user runs `/token-craft`, execute the following:

1. Run the scoring engine on their data
2. Calculate their current rank and score
3. Compare to previous snapshot (if exists)
4. Generate mission report
5. Show recommendations
6. Offer actions:
   - [A] Apply optimizations
   - [E] Export for team
   - [L] View leaderboards
   - [Q] Quit

[Detailed instructions for Claude...]
```

**Create: `skill_handler.py`**
```python
def main():
    """Main entry point for /token-craft skill."""

    # Load user data
    # Run scoring engine
    # Generate report
    # Show interactive menu
    # Handle user choices
```

---

### Step 5: Team Features

**Create: `leaderboard_generator.py`**
```python
class LeaderboardGenerator:
    def generate_company_leaderboard(self, stats_dir: Path) -> dict:
        """Generate anonymous company-wide leaderboard."""

    def generate_project_leaderboard(self, project_name: str) -> dict:
        """Generate project-specific leaderboard."""

    def generate_department_leaderboard(self, department: str) -> dict:
        """Generate department leaderboard."""

    def format_leaderboard(self, leaderboard: dict) -> str:
        """Format for display."""
```

---

### Step 6: hero.epam.com Integration

**Create: `hero_api_client.py`**
```python
class HeroAPIClient:
    def __init__(self, api_url: str, api_key: str):
        """Initialize hero.epam.com API client."""

    def issue_badge(self, user_email: str, badge_id: str, evidence: dict):
        """Issue badge to user."""

    def revoke_badge(self, user_email: str, badge_id: str):
        """Revoke badge (if rank drops)."""

    def get_user_badges(self, user_email: str) -> list:
        """Get all user's badges."""
```

---

## File Structure After Implementation

```
claude-token-analyzer/
├── analyze_tokens.py              # V1 (keep for reference)
├── analyze_tokens_v2.py           # V2 interactive
├── team_aggregator.py             # Team features
│
├── token_craft/                   # NEW: Core package
│   ├── __init__.py
│   ├── scoring_engine.py
│   ├── rank_system.py
│   ├── user_profile.py
│   ├── snapshot_manager.py
│   ├── delta_calculator.py
│   ├── report_generator.py
│   ├── progress_visualizer.py
│   ├── leaderboard_generator.py
│   ├── hero_api_client.py
│   └── recommendation_engine.py
│
├── skill_handler.py               # NEW: Main entry point
├── token-craft.md                 # NEW: Skill definition
│
├── tests/                         # NEW: Test suite
│   ├── test_scoring.py
│   ├── test_rank_system.py
│   └── test_snapshots.py
│
└── docs/                          # Existing docs
    ├── README.md
    ├── TOKEN_CRAFT_REDESIGN.md
    ├── SCORING_AND_BONUSES_EXPLAINED.md
    └── ...

~/.claude/token-craft/             # NEW: User data
├── snapshots/
│   └── snapshot_YYYYMMDD_HHMMSS.json
├── user_profile.json
├── achievements.json
└── config.json
```

---

## Testing Strategy

### Unit Tests
- Test each scoring component independently
- Test rank calculation edge cases
- Test snapshot save/load
- Test delta calculations

### Integration Tests
- Test full scoring pipeline
- Test snapshot → delta → recommendations flow
- Test leaderboard generation

### User Acceptance Tests
- Run on real data (your account)
- Verify scores make sense
- Test rank progression
- Test recommendations relevance

---

## Rollout Plan

### Phase 1: Internal Testing (1-2 weeks)
- Test with 3-5 users (you + volunteers)
- Gather feedback on scoring
- Tune weights if needed
- Fix bugs

### Phase 2: Pilot Program (2-4 weeks)
- Expand to 20-30 users across different roles
- Monitor engagement
- Collect feedback on gamification
- Add requested features

### Phase 3: Department Launch (1 month)
- Launch to Engineering department
- Set up project leaderboards
- Weekly reports
- Hero.epam.com integration

### Phase 4: Company-Wide (Ongoing)
- Open to all EPAM employees
- Company leaderboard
- Monthly challenges
- Certification program

---

## Success Metrics

**Engagement:**
- % of users running `/token-craft` weekly
- Average time between checks
- Feature usage (leaderboards, recommendations)

**Behavior Change:**
- % of users adopting optimizations
- Average token efficiency improvement
- Self-sufficiency rate increase

**Business Impact:**
- Total token savings (company-wide)
- Cost reduction percentage
- ROI on gamification investment

**Culture:**
- Hero.epam.com badge count
- Leaderboard participation
- Mentor/mentee connections

---

## Next Steps

Ready to start Phase 1 (Core Scoring Engine)?

I'll create:
1. `scoring_engine.py` with all 5 scoring components
2. `rank_system.py` with Space Exploration ranks
3. `user_profile.py` for state management
4. `test_scoring.py` with unit tests

Should I proceed?
