# Token-Craft

**Gamified LLM token optimization tool** that analyzes Claude Code usage and provides personalized recommendations through space exploration ranks.

## Features

- **Interactive Analysis** - Scope selection, optimization recommendations, delta tracking
- **Space Explorer Ranks** - Progress through ranks from Space Cadet to Grand Explorer
- **Time-Based Analysis** - Filter by date range, weekly/monthly trends, sprint analysis
- **Team Features** - Leaderboards, team-level insights, collaborative tracking
- **Cost Tracking** - Multi-deployment pricing (Direct API, AWS Bedrock, Google Vertex)
- **Claude Skill Integration** - Use `/token-craft` command in Claude Code

## Quick Start

**As a Claude Skill:**
```bash
/token-craft
```

**Standalone:**
```bash
python skill_handler.py
```

📚 **[Installation Guide](INSTALL.md)** | **[Quick Start](QUICK_START.md)** | **[Skill Setup](SKILL_INSTALLATION.md)**

## What it Does

- **Token Analysis** - Breakdown by model, task category, and project
- **Optimization Recommendations** - Personalized suggestions based on your usage patterns
- **Progress Tracking** - Snapshot history to measure improvements
- **Scoring System** - Earn points for optimization practices (context efficiency, tool use, etc.)
- **Cost Calculations** - Estimate spending across different deployment methods
- **Team Leaderboards** - Company-wide and project-level rankings

## Requirements

- Python 3.8+
- Claude Code installed
- Optional: `requests` (for hero.epam.com API integration)

## Data Sources

Reads from your Claude Code data:
- `~/.claude/stats-cache.json` - Token usage statistics
- `~/.claude/history.jsonl` - Conversation history

## Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[Installation](INSTALL.md)** - Detailed setup instructions
- **[Skill Installation](SKILL_INSTALLATION.md)** - Add `/token-craft` command to Claude Code
- **[Team Usage](TEAM_USAGE.md)** - Team features and leaderboards
- **[Time-Based Analysis](TIME_BASED_ANALYSIS.md)** - Filtering and trend analysis
- **[Interactive Guide](INTERACTIVE_GUIDE.md)** - Using interactive features
- **[Sharing](SHARE_PACKAGE.md)** - Distribution and packaging

## Version

**v1.1.0** (February 12, 2026)
- 100/100 Anthropic best practices alignment
- 8 optimization practices tracked
- Flexible pricing system
- Fully interactive handlers

See [UPGRADE_TO_V1.1.md](UPGRADE_TO_V1.1.md) and [V1.1.0_RELEASE_NOTES.md](V1.1.0_RELEASE_NOTES.md) for details.
