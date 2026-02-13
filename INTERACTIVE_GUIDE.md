# Interactive Mode Guide

## Overview

The team aggregator now features a **fully interactive interface** - no command-line arguments needed! Just run the script and follow the prompts.

## Quick Start

```bash
python team_aggregator.py
```

That's it! The script will guide you through everything.

## Interactive Features

### 🎯 Main Menu

When you run the script, you see:

```
======================================================================
CLAUDE CODE TOKEN ANALYZER - TEAM & TIME FEATURES
======================================================================

Welcome! What would you like to do?

  [1] Export my statistics (for personal or team analysis)
  [2] Aggregate team statistics (combine everyone's exports)
  [3] Help & Documentation
  [4] Exit

Your choice:
```

Simply enter a number and press Enter!

### 📤 Export Workflow

When you choose **[1] Export**:

**Step 1: Output Directory**
```
Where should the statistics be saved?
  Tip: Use your team's shared git repo directory

  Path: ./my-stats
```
- Enter any path
- If it doesn't exist, you'll be asked to create it
- Uses `~` for home directory

**Step 2: Date Range**
```
Analyze specific time period?
Filter by date range? (y/n): y

  Quick presets:
    L7 = Last 7 days (2024-02-05 to 2024-02-12)
    L30 = Last 30 days (2024-01-12 to 2024-02-12)
    TW = This week (2024-02-05 to 2024-02-12)
    LW = Last week (2024-01-29 to 2024-02-04)
    TM = This month (2024-02-01 to 2024-02-12)
    LM = Last month (2024-01-01 to 2024-01-31)

  Enter preset code, or 'C' for custom dates

  Your choice:
```

Options:
- **L7** - Last 7 days
- **L30** - Last 30 days
- **TW** - This week
- **LW** - Last week
- **TM** - This month
- **LM** - Last month
- **C** - Custom dates (you'll be prompted for specific dates)
- **n** - No filter (all data)

**Step 3: Results**
```
[+] Statistics Exported!
    File: ./my-stats/dmitriy_zhorov_at_epam.com_20240212_180000.json
    User: Dmitriy Zhorov <dmitriy_zhorov@epam.com>
    Sessions: 19
    Messages: 200

[+] Top Projects:
    Dmitriy_Zhorov: 8 sessions, 138 messages
    GenAI: 5 sessions, 16 messages
```

**Step 4: Git Operations** (if in git repo)
```
[+] Output directory is in a git repository
Commit and prepare for push? (y/n): y

[+] Changes committed!
    Next step: Run 'git push' to share with team

Push to remote now? (y/n): y

[+] Pushed to remote!
```

### 📊 Aggregate Workflow

When you choose **[2] Aggregate**:

**Step 1: Stats Directory**
```
Where are the team statistics files?
  Tip: This is usually your shared git repo directory

  Path: ./team-stats
```

**Step 2: Loading**
```
Found 3 potential stat file(s)...
  [+] Loaded: alice_at_company_20240212.json
  [+] Loaded: bob_at_company_20240212.json
  [+] Loaded: dmitriy_at_epam_20240212.json

[+] Successfully loaded 3 team member(s)
```

**Step 3: Results**
```
======================================================================
[*] TEAM SUMMARY
======================================================================

[+] Team Overview:
    Team size: 3 members
    Total sessions: 45
    Total messages: 1,250

[+] Team Members:
    Alice Smith <alice@company.com>
      Sessions: 20, Messages: 580
    Bob Johnson <bob@company.com>
      Sessions: 15, Messages: 420
    Dmitriy Zhorov <dmitriy_zhorov@epam.com>
      Sessions: 10, Messages: 250

[+] Top Team Projects:
    managed-services-dashboard
      Sessions: 15, Messages: 450
      Contributors: 3

[+] Individual Contributions:
    Alice Smith:
      Total sessions: 20
      Top projects:
        - api-gateway: 12 sessions
```

**Step 4: Save Report**
```
Save team report to file? (y/n): y

  Report filename (or Enter for default): weekly_report.json

[+] Team report saved to: ./team-stats/weekly_report.json
```

## Input Features

### ✅ Validation

- **Paths**: Checks if directories exist, offers to create
- **Dates**: Validates format (YYYY-MM-DD)
- **Numbers**: Only accepts valid menu choices
- **Yes/No**: Accepts y/yes/n/no

### 🔄 Error Handling

```
  [!] Path does not exist: /invalid/path
    Create it? (y/n):
```

The script never crashes - it asks you to fix the input!

### ⌨️ Keyboard Shortcuts

- **Ctrl+C** - Cancel operation safely
- **Enter** - Use default values
- **Up/Down arrows** - Command history (terminal feature)

## Date Presets Explained

| Code | Description | Example |
|------|-------------|---------|
| L7 | Last 7 days | Today - 7 days → Today |
| L30 | Last 30 days | Today - 30 days → Today |
| TW | This week | Monday → Today |
| LW | Last week | Last Monday → Last Sunday |
| TM | This month | 1st of month → Today |
| LM | Last month | 1st of last month → Last day of last month |
| C | Custom | You enter both dates |

## Command-Line Mode (Still Available!)

For automation/scripting:

```bash
# Export with CLI
python team_aggregator.py export --output-dir ./stats

# With date filter
python team_aggregator.py export \
  --output-dir ./stats \
  --date-from 2024-01-01 \
  --date-to 2024-02-12

# Auto-commit
python team_aggregator.py export \
  --output-dir ./stats \
  --commit

# Aggregate
python team_aggregator.py aggregate --stats-dir ./stats
```

## Comparison: Interactive vs CLI

| Feature | Interactive | CLI |
|---------|-------------|-----|
| **Ease of use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Speed** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Automation** | ❌ | ✅ |
| **Date presets** | ✅ | ❌ |
| **Error messages** | ✅ Guided | ⭐⭐⭐ |
| **Learning curve** | None! | Some |

**Use Interactive when:**
- You're doing it manually
- You want date presets
- You're learning the tool
- You want guided help

**Use CLI when:**
- Automating (cron, scripts)
- You know exact parameters
- Speed is critical
- In CI/CD pipelines

## Tips & Tricks

### 💡 Quick Export

Fastest way to export everything:
1. Run: `python team_aggregator.py`
2. Press: `1` (Export)
3. Enter path
4. Press: `n` (No date filter)
5. Done!

### 💡 Weekly Team Ritual

Every Monday morning:
1. `python team_aggregator.py`
2. `1` - Export
3. Enter team repo path
4. `LW` - Last week
5. `y` - Commit and push

### 💡 Sprint Retrospective

At end of sprint:
1. `python team_aggregator.py`
2. `1` - Export
3. Enter sprint folder
4. `C` - Custom dates
5. Enter sprint start/end
6. Then aggregate from sprint folder

## Troubleshooting

**Q: Script exits immediately**
- You might have command-line args from before
- Run: `python team_aggregator.py` with no arguments

**Q: Can't enter path with spaces**
- Use quotes: `"C:\My Folder\stats"`
- Or escape: `C:\My\ Folder\stats`

**Q: Date preset not working**
- Enter exactly: L7, L30, TW, etc.
- Use uppercase
- Or use `C` for custom

**Q: Want to cancel mid-way**
- Press `Ctrl+C` anytime
- Safe to interrupt

## Examples

### Example 1: Personal Weekly Review

```bash
$ python team_aggregator.py

Your choice: 1  # Export

Path: ~/my-weekly-stats

Filter by date range? (y/n): y

Your choice: L7  # Last 7 days

# Review results...

Commit and prepare for push? (y/n): n  # Just local

Do another operation? (y/n): n
```

### Example 2: Team Monthly Report

```bash
$ python team_aggregator.py

Your choice: 2  # Aggregate

Path: ~/team-claude-stats

# See team summary...

Save team report to file? (y/n): y
Report filename: monthly_feb_2024.json

Do another operation? (y/n): n
```

### Example 3: Compare Two Periods

```bash
# First run - January
$ python team_aggregator.py
Your choice: 1
Path: ~/comparison/january
Filter: y
Choice: C  # Custom
From: 2024-01-01
To: 2024-01-31

# Second run - February
Your choice: 1  # Do another? y
Path: ~/comparison/february
Filter: y
Choice: C
From: 2024-02-01
To: 2024-02-29

# Then compare by aggregating each
```

## Next Steps

1. **Try it now**: `python team_aggregator.py`
2. **Export your stats**: Choose option 1
3. **Pick a date range**: Try `L7` for last week
4. **Review results**: See your token usage

The interactive mode makes token analysis **effortless**! 🎉
