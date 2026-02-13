# Team Token Usage Analysis

## Overview

The team aggregator allows multiple team members to share and analyze their Claude Code token usage collectively.

## Architecture

```
Team Member A           Team Member B           Team Member C
    |                       |                       |
    | export                | export                | export
    v                       v                       v
  stats_A.json          stats_B.json          stats_C.json
    |                       |                       |
    +------------ shared git repo (team-claude-stats) ------------+
                            |
                            | aggregate
                            v
                     team_report.json
                     (combined analysis)
```

## Setup

### 1. Create Shared Repository

One team member creates the shared stats repo:

```bash
mkdir team-claude-stats
cd team-claude-stats
git init
echo "# Team Claude Token Statistics" > README.md
echo "*.json" >> .gitignore  # Initially ignore JSON
git add README.md .gitignore
git commit -m "Initial commit"
git remote add origin <your-git-url>
git push -u origin main
```

### 2. Team Members Clone

Each team member clones the repo:

```bash
git clone <your-git-url>
cd team-claude-stats
```

### 3. Allow JSON Files

Remove `*.json` from `.gitignore` or add specific patterns:

```gitignore
# Allow team stats
!*_at_*.json
!team_report_*.json
```

## Usage

### Export Personal Statistics

Each team member exports their stats:

```bash
# Basic export
python team_aggregator.py export --output-dir ./team-claude-stats

# Export with time filter
python team_aggregator.py export \
  --output-dir ./team-claude-stats \
  --date-from 2024-01-01 \
  --date-to 2024-02-12

# Export and auto-commit
python team_aggregator.py export \
  --output-dir ./team-claude-stats \
  --commit
```

This creates a file like:
```
dmitriy_zhorov_at_epam.com_20240212_180000.json
```

### Push to Shared Repo

```bash
cd team-claude-stats
git push
```

### Pull Latest Team Stats

```bash
cd team-claude-stats
git pull
```

### Aggregate Team Statistics

Anyone can aggregate the team stats:

```bash
python team_aggregator.py aggregate --stats-dir ./team-claude-stats
```

Output example:
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
    Charlie Wilson <charlie@company.com>
      Sessions: 10, Messages: 250

[+] Top Team Projects:
    managed-services-dashboard
      Sessions: 15, Messages: 450
      Contributors: 3
    api-gateway
      Sessions: 12, Messages: 380
      Contributors: 2

[+] Individual Contributions:
    Alice Smith:
      Total sessions: 20
      Top projects:
        - api-gateway: 12 sessions
        - frontend-app: 5 sessions
```

## Time-Based Analysis

### Weekly Comparison

Export stats for specific weeks:

```bash
# Week 1
python team_aggregator.py export \
  --output-dir ./weekly/week1 \
  --date-from 2024-02-05 \
  --date-to 2024-02-11

# Week 2
python team_aggregator.py export \
  --output-dir ./weekly/week2 \
  --date-from 2024-02-12 \
  --date-to 2024-02-18
```

Then compare:
```bash
python team_aggregator.py aggregate --stats-dir ./weekly/week1
python team_aggregator.py aggregate --stats-dir ./weekly/week2
```

### Monthly Trends

```bash
# January
python team_aggregator.py export \
  --output-dir ./monthly/jan \
  --date-from 2024-01-01 \
  --date-to 2024-01-31

# February
python team_aggregator.py export \
  --output-dir ./monthly/feb \
  --date-from 2024-02-01 \
  --date-to 2024-02-29
```

## Workflow

### Daily/Weekly Team Sync

```bash
# Each team member (daily or weekly):
cd team-claude-stats
git pull
python ../team_aggregator.py export --output-dir . --commit
git push

# Team lead (weekly):
git pull
python ../team_aggregator.py aggregate --stats-dir . \
  --output weekly_report_$(date +%Y%m%d).json
```

### Sprint Analysis

At end of sprint:

```bash
# Export sprint period
python team_aggregator.py export \
  --output-dir ./sprint-23 \
  --date-from 2024-02-01 \
  --date-to 2024-02-14

# Aggregate
python team_aggregator.py aggregate --stats-dir ./sprint-23
```

## Export Data Format

Each personal export contains:

```json
{
  "exported_at": "2024-02-12T18:00:00",
  "user": {
    "name": "Your Name",
    "email": "your.email@company.com"
  },
  "date_range": {
    "from": "2024-01-01T00:00:00",
    "to": "2024-02-12T18:00:00"
  },
  "summary": {
    "total_sessions": 19,
    "total_messages": 200,
    "model_usage": {
      "claude-sonnet-4-5": {
        "inputTokens": 44249,
        "outputTokens": 442426
      }
    }
  },
  "by_project": {
    "managed-services-dashboard": {
      "sessions": 1,
      "messages": 25
    }
  },
  "daily_activity": [...],
  "daily_model_tokens": [...]
}
```

## Team Report Format

Aggregated team report contains:

```json
{
  "aggregated_at": "2024-02-12T18:30:00",
  "team_size": 3,
  "members": [
    {
      "name": "Alice Smith",
      "email": "alice@company.com",
      "sessions": 20,
      "messages": 580
    }
  ],
  "totals": {
    "sessions": 45,
    "messages": 1250,
    "tokens": {...}
  },
  "by_project": {
    "project-name": {
      "sessions": 15,
      "messages": 450,
      "contributors": ["alice@company.com", "bob@company.com"],
      "contributor_count": 2
    }
  },
  "by_member": [...]
}
```

## Privacy Considerations

**What's Shared:**
- Session counts
- Message counts
- Token usage by model
- Project names
- Timestamps (aggregated)

**What's NOT Shared:**
- Actual message content
- Specific prompts or responses
- File paths or code
- Credentials or secrets

## Best Practices

1. **Regular Exports** - Export weekly or after major work
2. **Consistent Time Periods** - Use same date ranges for comparison
3. **Clean Project Names** - Avoid sensitive info in project names
4. **Review Before Commit** - Check exported JSON for sensitivity
5. **Access Control** - Use private repo for team stats
6. **Archive Old Data** - Move old stats to archive/ folder

## Integration with V2 Analyzer

You can analyze team aggregated data:

```bash
# Export from team stats
python team_aggregator.py export --output-dir ./team-claude-stats --commit

# Wait for team to sync
cd team-claude-stats && git pull && cd ..

# Aggregate
python team_aggregator.py aggregate --stats-dir ./team-claude-stats

# Individual analysis still uses V2
python analyze_tokens_v2.py
```

## Troubleshooting

**Error: "No statistics files found"**
- Check directory path
- Ensure JSON files exist
- Check file permissions

**Error: "Git commit failed"**
- Ensure you're in a git repo
- Check git config (user.name, user.email)
- Manually commit: `git add . && git commit -m "Add stats"`

**Different team member counts**
- Team members may export at different times
- Use time filters for fair comparison
- Ensure everyone exports for same date range

## Example Team Workflow

```bash
# Monday morning - team lead
cd team-claude-stats
git pull
python ../team_aggregator.py aggregate --stats-dir .
# Review last week's stats

# Throughout the week - all team members
# (After significant work)
python team_aggregator.py export \
  --output-dir ~/team-claude-stats \
  --commit
cd ~/team-claude-stats && git push

# Friday - sprint retrospective
cd team-claude-stats
git pull
python ../team_aggregator.py aggregate --stats-dir . \
  --output sprint_23_report.json

# Review sprint_23_report.json in retrospective
```

## Advanced: Custom Analysis

Load team report for custom analysis:

```python
import json

with open('team_report_20240212.json', 'r') as f:
    team_data = json.load(f)

# Top contributor
top_member = max(team_data['members'], key=lambda x: x['sessions'])
print(f"Top contributor: {top_member['name']} with {top_member['sessions']} sessions")

# Projects needing attention
for project, stats in team_data['by_project'].items():
    if stats['contributor_count'] == 1:
        print(f"Single contributor project: {project}")
```
