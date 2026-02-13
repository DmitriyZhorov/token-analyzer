# Token-Craft: Master LLM Efficiency Through Space Exploration

🚀 A gamified token optimization system that tracks your LLM usage efficiency and awards space exploration ranks based on your mastery.

## Quick Start

```bash
# Run full analysis
python skill_handler.py

# Quick summary
python skill_handler.py --mode summary

# One-line status
python skill_handler.py --mode quick
```

## What is Token-Craft?

Token-Craft helps you optimize your LLM token usage through:
- **7 Space Exploration Ranks**: Progress from Cadet to Galactic Legend
- **5 Scoring Categories**: Track efficiency, adoption, self-sufficiency, trends, and best practices
- **Personalized Recommendations**: Get specific suggestions to improve your score
- **Progress Tracking**: Compare current performance to previous snapshots
- **Achievements**: Earn badges for milestones and accomplishments

## Space Exploration Ranks

| Rank | Score Range | Description |
|------|-------------|-------------|
| 🎓 **Cadet** | 0-199 | Academy training, learning fundamentals |
| ✈️ **Pilot** | 200-399 | First missions, gaining experience |
| 🧭 **Navigator** | 400-599 | Charting efficient courses |
| ⭐ **Commander** | 600-799 | Leading missions with precision |
| 👨‍✈️ **Captain** | 800-999 | Commanding the ship with mastery |
| 🎖️ **Admiral** | 1000-1199 | Fleet command, strategic excellence |
| 🌌 **Galactic Legend** | 1200+ | Explored uncharted territories |

## Scoring System (1000 points total)

### 1. Token Efficiency (35%, 350 points)
Measures your average tokens per session compared to company baseline.
- **Goal**: Use fewer tokens to accomplish the same tasks
- **Impact**: 30% improvement = ~$100-150 saved annually per user

### 2. Optimization Adoption (25%, 250 points)
Tracks usage of 5 key optimizations:
- Defer documentation (50 pts) - Wait until code is ready for GitHub
- Use CLAUDE.md (50 pts) - Project-specific context files
- Concise response mode (40 pts) - Brief responses by default
- Direct commands (60 pts) - Run git/ls/cat directly instead of asking AI
- Context management (50 pts) - Keep sessions focused (5-15 messages)

### 3. Self-Sufficiency (20%, 200 points)
How often you run commands directly vs asking AI.
- **Goal**: Run `git status` instead of "show me git status"
- **Impact**: Saves 800-1500 tokens per command

### 4. Improvement Trend (15%, 150 points)
Progress over time (last 30 days vs previous 30 days).
- 10%+ improvement: 150 points
- 5-10% improvement: 100 points
- Maintaining: 20 points
- **Note**: Can go negative if performance declines!

### 5. Best Practices (5%, 50 points)
Basic setup and configuration:
- CLAUDE.md in top 3 projects (30 pts)
- Memory.md has optimizations (10 pts)
- Uses appropriate tooling (10 pts)

## Installation

1. **Python Dependencies**: None! Uses only standard library.

2. **File Structure**:
```
claude-token-analyzer/
├── token_craft/           # Core package
│   ├── scoring_engine.py
│   ├── rank_system.py
│   ├── user_profile.py
│   ├── snapshot_manager.py
│   ├── delta_calculator.py
│   ├── report_generator.py
│   └── progress_visualizer.py
├── skill_handler.py       # Main entry point
├── token-craft.md         # Claude Skill definition
└── tests/                 # Unit tests

~/.claude/token-craft/     # User data (auto-created)
├── snapshots/
├── user_profile.json
└── achievements.json
```

## Usage

### As Claude Skill (Recommended)

Once set up, just type:
```
/token-craft
```

Claude will run the analysis and show your report.

### As Standalone Script

```bash
# Full report
python skill_handler.py

# Summary
python skill_handler.py --mode summary

# JSON output (for automation)
python skill_handler.py --json
```

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
  Avg Tokens/Session................ 11,200
  Current Rank...................... Commander
  Achievements Earned............... 5

Top Optimization Opportunities:
======================================================================

┌────────────────────────────────────────────────────────────────────┐
│ ► Increase Self-Sufficiency to 75%                                 │
├────────────────────────────────────────────────────────────────────┤
│   Run commands directly: git status, ls, cat instead of asking AI  │
├────────────────────────────────────────────────────────────────────┤
│   Impact: +50 points, Captain rank in 2 months                     │
└────────────────────────────────────────────────────────────────────┘
```

## How Scoring Works

### Real Example Calculation

User with 45 sessions, avg 11,200 tokens/session:

**Token Efficiency**: 11,200 vs 15,000 baseline = 25% better → **177 points** (51% of 350)

**Optimization Adoption**:
- Defer docs: 85% consistency → 42.5 pts
- CLAUDE.md: 90% → 45 pts
- Concise mode: 75% → 30 pts
- Direct commands: 60% → 36 pts
- Context mgmt: 70% → 35 pts
- **Total: 188.5 points** (75% of 250)

**Self-Sufficiency**: 60% rate → **120 points** (60% of 200)

**Improvement Trend**: 12% improvement → **150 points** (100% of 150)

**Best Practices**: All setup complete → **40 points** (80% of 50)

**Grand Total: 675.5 points = Commander Rank** ⭐

## Key Optimizations to Apply

### 1. Defer Documentation (High Impact)
❌ **Bad**: Writing README while coding
```
User: "Create a user authentication system"
Claude: [writes code]
User: "Now write the README"
Claude: [writes documentation]  ← 2000-3000 tokens wasted if code changes
```

✅ **Good**: Defer until ready for GitHub
```
User: "Create auth system, skip docs for now"
Claude: [writes code only]
[... test, refine, finalize ...]
User: "Now write README"  ← Only 1 documentation pass needed
```

**Savings**: 2000-3000 tokens per feature = **+50 points**

### 2. Use CLAUDE.md (High Impact)
Create `CLAUDE.md` in your top 3 projects:

```markdown
## Project Context
This is a React dashboard for monitoring managed services.

## Tech Stack
- React 18, TypeScript
- Vite for bundling
- Material-UI components

## Coding Style
- Use functional components
- TypeScript strict mode
- ESLint + Prettier configured

## Preferences
- Defer documentation until pushing to GitHub
- Keep responses concise
- Use existing components before creating new ones
```

**Savings**: 1500-2500 tokens per session = **+50 points**

### 3. Run Commands Directly (Medium Impact)
❌ **Bad**: Asking AI
```
User: "Show me git status"
Claude: [runs Bash tool, returns output]  ← 1200 tokens
```

✅ **Good**: Run yourself
```
$ git status  ← 0 tokens, instant result
[... see output ...]
User: "Why is file.txt unstaged?"  ← Focused question, 600 tokens
```

**Savings**: 800-1500 tokens per command = **+60 points**

### 4. Context Management (Medium Impact)
❌ **Bad**: One long session
```
Session 1: 45 messages, 35,000 tokens
- Start with bug fix
- Add new feature
- Refactor old code
- Write tests
- Update docs
← Context bloated, responses get verbose
```

✅ **Good**: Focused sessions
```
Session 1: Bug fix (8 messages, 6,000 tokens)
Session 2: New feature (12 messages, 9,000 tokens)
Session 3: Tests (7 messages, 5,000 tokens)
← Each session stays focused
```

**Savings**: 10-20% reduction = **+50 points**

## Testing

Run unit tests:
```bash
cd tests
python test_scoring.py
```

## Data Storage

All data stays local on your machine:

```
~/.claude/token-craft/
├── snapshots/                    # Historical progress
│   ├── snapshot_20260212_120000.json
│   └── snapshot_20260112_093000.json
├── user_profile.json             # Current state
└── achievements.json             # Earned achievements
```

## Roadmap

### Phase 1: Core (✅ COMPLETE)
- [x] Scoring engine
- [x] Rank system
- [x] Snapshot tracking
- [x] Report generation
- [x] Achievement system

### Phase 2: Team Features (Coming Soon)
- [ ] Leaderboards (company/project/department)
- [ ] Team export/aggregation
- [ ] Anonymous rankings

### Phase 3: Integration (Future)
- [ ] hero.epam.com badges
- [ ] /insights integration
- [ ] Mentorship matching
- [ ] Monthly challenges

## FAQ

**Q: How often should I run /token-craft?**
A: Weekly is ideal for tracking trends. Daily if you're actively optimizing.

**Q: Can my rank go down?**
A: Yes! Scoring is based on 90-day rolling window. If you stop optimizing, your score will decrease.

**Q: What's a good target rank?**
A: Navigator (400+) is solid. Commander (600+) is advanced. Captain (800+) is mastery.

**Q: How much can I actually save?**
A: Average user with 100 sessions/month spending $40. With optimizations:
- 20% improvement = $8/month = $96/year
- 30% improvement = $12/month = $144/year

**Q: Is this only for engineers?**
A: No! Ranks work for anyone using LLMs - designers, PMs, analysts, writers, etc.

## Contributing

Found a bug or have a suggestion? Open an issue!

## License

Internal EPAM tool. Not for external distribution.

---

Made with 🚀 by Dmitriy Zhorov
Inspired by demo scene constraint programming culture
