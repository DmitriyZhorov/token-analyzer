# Claude Code Token Analyzer

Analyzes your Claude Code token usage and provides breakdown by task categories.

## What it does

- Shows total token usage across all models (Sonnet, Opus, Haiku)
- Breaks down sessions by task type (Configuration, File Operations, Debugging, etc.)
- Shows activity statistics (sessions, messages, tool calls)
- Lists sample sessions for each category

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

## Note

Claude Code doesn't track per-session token usage, so task categories are estimated based on keywords in your messages. Total token usage is accurate from Claude's stats file.
