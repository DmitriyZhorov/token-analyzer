# Quick Start Guide

## Personal Analysis

### Run V2 Analyzer (Interactive)

```bash
python analyze_tokens_v2.py
```

Follow prompts to:
1. Select projects
2. Review analysis
3. Choose optimizations
4. Apply changes

## Time-Based Analysis

### Last 7 Days

```bash
python team_aggregator.py export \
  --output-dir ./my-stats \
  --date-from 2024-02-05 \
  --date-to 2024-02-12
```

### Last 30 Days

```bash
python team_aggregator.py export \
  --output-dir ./my-stats \
  --date-from 2024-01-12 \
  --date-to 2024-02-12
```

### Compare Periods

```bash
# Before optimization
python team_aggregator.py export \
  --output-dir ./before \
  --date-from 2024-01-01 \
  --date-to 2024-01-31

# After optimization
python team_aggregator.py export \
  --output-dir ./after \
  --date-from 2024-02-01 \
  --date-to 2024-02-29

# View results
python team_aggregator.py aggregate --stats-dir ./before
python team_aggregator.py aggregate --stats-dir ./after
```

## Team Collaboration

### Setup (One-Time)

```bash
# Team lead creates repo
mkdir team-claude-stats
cd team-claude-stats
git init
git remote add origin <your-git-url>

# Team members clone
git clone <your-git-url>
```

### Daily Workflow

```bash
# Export your stats
python team_aggregator.py export \
  --output-dir ../team-claude-stats \
  --commit

# Push to team
cd ../team-claude-stats
git push
```

### Weekly Team Review

```bash
# Pull latest
cd team-claude-stats
git pull

# Aggregate team stats
python ../team_aggregator.py aggregate --stats-dir .
```

## Common Scenarios

### Scenario 1: Measure Optimization Impact

```bash
# 1. Run baseline analysis
python analyze_tokens_v2.py
# Creates snapshot_TIMESTAMP.json

# 2. Apply optimizations from wizard

# 3. Work for 2 weeks

# 4. Run analysis again
python analyze_tokens_v2.py
# Shows delta from previous snapshot
```

### Scenario 2: Sprint Retrospective

```bash
# Export sprint period
python team_aggregator.py export \
  --output-dir ./sprint-23 \
  --date-from 2024-02-01 \
  --date-to 2024-02-14

# Aggregate team stats
python team_aggregator.py aggregate --stats-dir ./sprint-23

# Review in retrospective meeting
```

### Scenario 3: Weekly Team Dashboard

```bash
#!/bin/bash
# weekly_dashboard.sh

# Each Monday, team members export
python team_aggregator.py export \
  --output-dir ~/team-stats \
  --date-from $(date -d "7 days ago" +%Y-%m-%d) \
  --date-to $(date +%Y-%m-%d) \
  --commit

cd ~/team-stats
git push

# Team lead aggregates
git pull
python ../team_aggregator.py aggregate --stats-dir .
```

## Files & Directories

```
claude-token-analyzer/
├── analyze_tokens_v2.py      # Interactive analyzer
├── team_aggregator.py         # Time & team features
├── README_V2.md               # V2 documentation
├── TEAM_USAGE.md              # Team guide
├── TIME_BASED_ANALYSIS.md     # Time analysis guide
└── QUICK_START.md             # This file

~/.claude/
├── history.jsonl              # Your conversation history
├── stats-cache.json           # Token usage stats
└── token-analyzer-snapshots/  # Optimization snapshots
    └── snapshot_*.json

team-claude-stats/ (shared repo)
├── user1_at_company_*.json    # Team member exports
├── user2_at_company_*.json
└── team_report_*.json         # Aggregated reports
```

## Next Steps

1. **Try personal analysis**: `python analyze_tokens_v2.py`
2. **Export time period**: `python team_aggregator.py export --output-dir ./stats`
3. **Read detailed guides**:
   - [V2 Features](README_V2.md)
   - [Time Analysis](TIME_BASED_ANALYSIS.md)
   - [Team Usage](TEAM_USAGE.md)

## Help

- All scripts support `--help`: `python team_aggregator.py --help`
- Check documentation for detailed examples
- Open issues on GitHub: https://github.com/DmitriyZhorov/token-analyzer
