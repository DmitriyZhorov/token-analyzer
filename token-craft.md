---
name: token-craft
description: Master LLM efficiency through space exploration ranks
version: 1.0.0
triggers:
  - /token-craft
  - /tc
---

# Token-Craft Skill

## Purpose
Help users optimize their LLM token usage through gamified ranks inspired by space exploration. Track progress, provide recommendations, and celebrate achievements.

## When to Use
User types `/token-craft` or `/tc` to check their token optimization progress.

## What This Skill Does

1. **Analyzes Usage**: Reads history.jsonl and stats-cache.json to calculate token efficiency
2. **Calculates Rank**: Assigns space exploration rank (Cadet → Galactic Legend) based on 5 scoring categories
3. **Tracks Progress**: Compares to previous snapshots to show improvement trends
4. **Provides Recommendations**: Suggests specific optimizations to improve score
5. **Awards Achievements**: Recognizes milestones and accomplishments

## Space Exploration Ranks (7 Levels)

1. **Cadet** (0-199 points) - Academy training, learning fundamentals
2. **Pilot** (200-399 points) - First missions, gaining experience
3. **Navigator** (400-599 points) - Charting efficient courses
4. **Commander** (600-799 points) - Leading missions with precision
5. **Captain** (800-999 points) - Commanding the ship with mastery
6. **Admiral** (1000-1199 points) - Fleet command, strategic excellence
7. **Galactic Legend** (1200+ points) - Explored uncharted territories

## Scoring Categories (1000 points total)

1. **Token Efficiency (35%, 350 points)**: Performance vs company baseline
2. **Optimization Adoption (25%, 250 points)**: Using best practices consistently
3. **Self-Sufficiency (20%, 200 points)**: Running commands directly vs asking AI
4. **Improvement Trend (15%, 150 points)**: Progress over time
5. **Best Practices (5%, 50 points)**: Setup and configuration (CLAUDE.md, Memory.md)

## How to Execute

When user types `/token-craft`:

1. Run the Python skill handler:
   ```bash
   cd C:\Users\Dmitriy_Zhorov\Documents\Personal\GenAI\claude-token-analyzer
   python skill_handler.py --mode full
   ```

2. The script will:
   - Load user's history and stats
   - Calculate scores across 5 categories
   - Determine current rank
   - Compare to previous snapshot (if exists)
   - Generate comprehensive report
   - Save new snapshot

3. Present the report to the user with:
   - Current rank and progress bar
   - Score breakdown by category
   - Progress since last check (if applicable)
   - Top 3 optimization recommendations
   - Achievements earned
   - Leaderboard position (future)

4. Offer interactive menu:
   ```
   What would you like to do?
   [A] Apply recommended optimizations
   [E] Export stats for team analysis
   [L] View leaderboards
   [H] View achievements history
   [Q] Quit
   ```

## Command Variations

- `/token-craft` or `/tc` - Full report
- `/tc summary` - Quick summary (1 screen)
- `/tc quick` - One-line status

To run variations:
```bash
python skill_handler.py --mode summary  # Quick summary
python skill_handler.py --mode quick    # One-line status
```

## Key Recommendations to Suggest

Based on user's scores, suggest:

1. **If Token Efficiency < 50%**:
   - "Your avg tokens/session is above baseline. Review sessions to identify optimization opportunities."
   - Impact: +50-100 points

2. **If Defer Documentation not adopted**:
   - "Avoid writing documentation mid-development. Wait until code is complete."
   - Impact: +30-50 points, saves 2000-3000 tokens per feature

3. **If CLAUDE.md missing**:
   - "Create CLAUDE.md files in your top 3 projects with project-specific context."
   - Impact: +35-50 points, saves 1500-2500 tokens per session

4. **If Self-Sufficiency < 60%**:
   - "Run simple commands directly: git status, ls, cat instead of asking AI."
   - Impact: +40-60 points, saves 800-1500 tokens per command

5. **If Context Management poor**:
   - "Keep sessions focused (5-15 messages). Start new session for new topics."
   - Impact: +25-40 points

## Example Output

```
======================================================================
TOKEN-CRAFT: YOUR SPACE MISSION REPORT
======================================================================

Current Rank: [COMMANDER] ████████████░░░ 685/800
Next Rank:    [CAPTAIN] in 115 points

Progress Since Last Check:
----------------------------------------------------------------------
  Great progress! +47 points

  Score change: ↑ +47.0 points
  Rank: No change

Score Breakdown:
----------------------------------------------------------------------
Token Efficiency       [████████░░░░░░░░░░░░░░░░░░░░] 177/350 (51%)
Optimization Adoption  [████████████████░░░░░░░░░░░░] 218/250 (87%)
Self-Sufficiency       [██████████████░░░░░░░░░░░░░░] 128/200 (64%)
Improvement Trend      [██████████████████████████████] 150/150 (100%)
Best Practices         [████████████████████████░░░░░░] 40/50 (80%)

Your Mission Stats:
----------------------------------------------------------------------
  Total Sessions.................... 45
  Total Messages.................... 420
  Total Tokens...................... 504,000
  Avg Tokens/Session................ 11,200
  Current Rank...................... Commander
  Achievements Earned............... 5

Top Optimization Opportunities:
======================================================================

┌────────────────────────────────────────────────────────────────────┐
│ ► Increase Self-Sufficiency to 75%                                 │
├────────────────────────────────────────────────────────────────────┤
│   Run commands directly instead of asking AI: git status, ls, cat  │
│   grep. Builds skills and saves tokens.                            │
├────────────────────────────────────────────────────────────────────┤
│   Impact: +50 points, Captain rank in 2 months                     │
└────────────────────────────────────────────────────────────────────┘

======================================================================
Run '/token-craft' anytime to check your progress!
======================================================================
```

## Important Notes

- Scoring is based on 90-day rolling window
- Ranks can go DOWN if optimization practices decline (bidirectional progress)
- Snapshots saved to ~/.claude/token-craft/snapshots/
- User profile saved to ~/.claude/token-craft/user_profile.json
- All data stays local (no external API calls required)

## Error Handling

If script fails:
1. Check that history.jsonl and stats-cache.json exist in ~/.claude/
2. Check Python is available and token_craft module is importable
3. Show user friendly error message with troubleshooting steps

## Future Enhancements (Not Yet Implemented)

- Team leaderboards (company/project/department)
- hero.epam.com badge integration
- Mentorship matching (Admirals mentor Cadets)
- Monthly challenges
- Integration with `/insights` command
- Automated weekly reports
