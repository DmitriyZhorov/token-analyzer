# Claude Code Token Analyzer

Analyzes your Claude Code token usage and provides breakdown by task categories.

## 🆕 Latest Features!

### [Version 2](README_V2.md) - Interactive Analyzer
- Scope selection (choose projects to analyze)
- Interactive optimization with trade-off analysis
- Delta tracking and improvement measurement
- Detailed estimated savings
- Snapshot history

**Quick start:** `python analyze_tokens_v2.py`

### [Time-Based Analysis](TIME_BASED_ANALYSIS.md) - New!
- Filter by date range
- Weekly/monthly trends
- Sprint analysis
- Before/after optimization comparison

**Quick start:** `python team_aggregator.py export --output-dir ./stats --date-from 2024-01-01 --date-to 2024-02-12`

### [Team Aggregation](TEAM_USAGE.md) - New!
- Export stats to shared git repo
- Team-level insights
- Collaborative tracking
- Individual contributor breakdown

**Quick start:** `python team_aggregator.py aggregate --stats-dir ./team-stats`

📚 **[Quick Start Guide](QUICK_START.md)** - Start here!

---

## Version 1 (Original)

## What it does

- Shows total token usage across all models (Sonnet, Opus, Haiku)
- Breaks down sessions by task type (Configuration, File Operations, Debugging, etc.)
- Provides project-specific breakdown (sessions and messages per project)
- Shows activity statistics (sessions, messages, tool calls)
- Lists sample sessions for each category
- Detects optimization opportunities and provides actionable insights
- **Interactive Wizard**: Apply optimizations automatically with one click

## Usage

```bash
python analyze_tokens.py
```

The script reads from your Claude Code data:
- `~/.claude/stats-cache.json` - Token usage statistics
- `~/.claude/history.jsonl` - Conversation history

## Requirements

- Python 3.x
- Claude Code installed

## Output

The analyzer will show:
- Token breakdown by model
- Total tokens used
- Activity statistics
- Task category distribution with visual bars
- Sample sessions for each category
- Project-specific breakdown
- Token optimization insights
- Interactive optimization wizard

## Optimization Wizard

After analysis, the tool offers an interactive questionnaire where you can:

1. **Defer Documentation** - Add rules to skip README/comments until pushing to GitHub
2. **Reduce Configuration Time** - Create CLAUDE.md templates for your projects
3. **Command Cheat Sheet** - Generate a quick reference for common commands
4. **Concise Response Mode** - Set preference for brief responses by default

The wizard will automatically:
- Create/update CLAUDE.md files in your top 3 projects
- Generate command reference files
- Apply your chosen optimizations

## Note

Claude Code doesn't track per-session token usage, so task categories are estimated based on keywords in your messages. Total token usage is accurate from Claude's stats file.
