# Token-Craft Project Context

**Note:** Global permission policy from `~/.claude/CLAUDE.md` applies to this project.
This file adds project-specific context and overrides.

## Project Overview

**Token-Craft** is a gamified LLM token optimization tool that analyzes Claude Code usage and provides personalized recommendations through space exploration ranks.

- **Language:** Python 3.8+ (standard library only)
- **Type:** CLI tool + Claude Skill
- **Status:** Production ready (v1.1.0)
- **Repository:** https://github.com/DmitriyZhorov/token-analyzer

## Project Structure

```
token-analyzer/
├── token_craft/          # Core package (13 modules)
│   ├── scoring_engine.py
│   ├── rank_system.py
│   ├── pricing_calculator.py
│   └── ...
├── skill_handler.py      # Main entry point (interactive)
├── skill_handler_full.py # Full featured handler
├── docs/                 # Documentation
└── tests/                # Unit tests
```

## Permission Policy

### Auto-Approve (No Confirmation Needed) ✅

These operations are safe and should proceed without asking:

**File Operations:**
- `Read` - Reading any file
- `Glob` - Finding files by pattern
- `Grep` - Searching file contents
- `Write` - Creating new files
- `Edit` - Modifying existing files

**Git Operations:**
- `Bash(git status)` - Check status
- `Bash(git diff *)` - View diffs
- `Bash(git log *)` - View history
- `Bash(git add *)` - Stage changes
- `Bash(git commit *)` - Create commits (but NOT --amend)
- `Bash(git push origin master)` - Push to master
- `Bash(git push origin *)` - Push feature branches
- `Bash(git branch *)` - Branch operations
- `Bash(git checkout *)` - Switch branches

**Python Operations:**
- `Bash(python *)` - Run Python scripts
- `Bash(pip install *)` - Install packages
- `Bash(pytest *)` - Run tests

**Research & Documentation:**
- `WebFetch` - Fetch web pages for research (NOT WebSearch - it's broken)

**Safe Commands:**
- `Bash(ls *)` - List files
- `Bash(dir *)` - List files (Windows)
- `Bash(cat *)` - View file contents
- `Bash(echo *)` - Print text
- `Bash(mkdir *)` - Create directories
- `Bash(cd *)` - Change directory
- `Bash(pwd)` - Print working directory
- `Bash(wc *)` - Count lines/words
- `Bash(grep *)` - Search (prefer Grep tool)
- `Bash(find *)` - Find files (prefer Glob tool)

### Always Confirm (Keep Safe) ⚠️

These operations are destructive and should always ask first:

**Destructive File Operations:**
- `Bash(rm *)` - Delete files
- `Bash(rmdir *)` - Delete directories
- `Bash(del *)` - Delete (Windows)
- `Bash(move *)` - Move files (Windows)
- `Bash(mv *)` - Move files (Unix)
- `Bash(ren *)` - Rename (Windows)

**Dangerous Git Operations:**
- `Bash(git push --force *)` - Force push
- `Bash(git push -f *)` - Force push (short form)
- `Bash(git reset --hard *)` - Hard reset
- `Bash(git clean *)` - Clean untracked files
- `Bash(git commit --amend *)` - Amend commits
- `Bash(git rebase *)` - Rebase operations
- `Bash(git branch -D *)` - Force delete branch

**System Operations:**
- `Bash(shutdown *)` - Shutdown system
- `Bash(reboot *)` - Reboot system
- `Bash(format *)` - Format drives
- Any command with `sudo` or admin elevation

### Special Cases

**WebSearch:** Do NOT use - it's currently broken. Always use `WebFetch` instead.

**Command Chaining:** When multiple operations depend on each other, chain them with `&&` in a single Bash call rather than multiple sequential calls.

## Coding Standards

### Python Style
- Follow PEP 8
- Type hints for function signatures
- Docstrings for public methods
- Keep functions under 50 lines
- Use descriptive variable names

### Git Commit Messages
```
<type>: <subject>

<body>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

**Types:** feat, fix, docs, refactor, test, chore

### Documentation
- Keep README.md updated
- Use Markdown format
- Include code examples
- Update version numbers

## Common Tasks

### Run Token-Craft Analysis
```bash
python skill_handler.py
```

### Run Tests
```bash
python -m pytest tests/
```

### Calculate Pricing
```bash
python token_craft/pricing_calculator.py
```

### Create New Snapshot
Happens automatically when running analysis.

## Dependencies

**Core:** Python 3.8+ standard library only
**Optional:**
- `requests` (for hero.epam.com API integration)
- No other dependencies by design!

## Important Notes

### Windows Encoding
The code includes UTF-8 encoding wrapper for Windows CMD:
```python
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

### Data Locations
- **History:** `~/.claude/history.jsonl`
- **Stats:** `~/.claude/stats-cache.json`
- **Profile:** `~/.claude/token-craft/user_profile.json`
- **Snapshots:** `~/.claude/token-craft/snapshots/`

### Skill Integration
The `/token-craft` skill is defined at:
- `~/.claude/skills/token-craft/SKILL.md`

## Development Workflow

1. **Making Changes:**
   - Edit files as needed
   - Test locally
   - Commit with descriptive message
   - Push to GitHub

2. **No Confirmation Needed For:**
   - Reading files to understand code
   - Creating new files
   - Editing existing files
   - Running tests
   - Committing and pushing
   - Fetching documentation via WebFetch

3. **Always Confirm Before:**
   - Deleting files
   - Force operations
   - Renaming/moving files
   - Destructive git operations

## Version

Current: **v1.1.0** (February 12, 2026)
- 100/100 Anthropic best practices alignment
- 8 optimization practices tracked
- Flexible pricing system
- Fully interactive handlers

## Philosophy

Token-Craft is inspired by **demo scene constraint programming culture** - doing more with less. We optimize not just tokens, but also development workflow. That's why we minimize confirmation prompts for safe operations while maintaining safety for destructive ones.

Work fast, work safe, work smart! 🚀
