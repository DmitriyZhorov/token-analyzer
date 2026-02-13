# Time-Based Token Analysis

## Overview

Analyze your Claude Code token usage over specific time periods to identify trends, measure improvements, and track optimization effectiveness.

## Features

### 1. Time Period Filtering

Analyze specific date ranges:
- **Weekly analysis** - Compare week-over-week
- **Monthly trends** - Track monthly patterns
- **Sprint analysis** - Measure token usage per sprint
- **Before/After** - Measure optimization impact

### 2. Trend Identification

Detect patterns over time:
- Usage spikes
- Efficiency improvements
- Category shifts (less docs, more coding)
- Project-specific trends

### 3. Optimization Tracking

Measure impact of optimizations:
- Compare pre/post optimization periods
- Validate estimated savings
- Adjust strategies based on actual results

## Usage

### Export Time-Filtered Stats

```bash
# Last 7 days
python team_aggregator.py export \
  --output-dir ./stats/last-week \
  --date-from 2024-02-05 \
  --date-to 2024-02-12

# Last 30 days
python team_aggregator.py export \
  --output-dir ./stats/last-month \
  --date-from 2024-01-12 \
  --date-to 2024-02-12

# Specific sprint
python team_aggregator.py export \
  --output-dir ./stats/sprint-23 \
  --date-from 2024-02-01 \
  --date-to 2024-02-14
```

### Compare Time Periods

```bash
# Before optimization (January)
python team_aggregator.py export \
  --output-dir ./comparison/before \
  --date-from 2024-01-01 \
  --date-to 2024-01-31

# After optimization (February)
python team_aggregator.py export \
  --output-dir ./comparison/after \
  --date-from 2024-02-01 \
  --date-to 2024-02-29

# Compare
echo "=== BEFORE OPTIMIZATION ==="
python team_aggregator.py aggregate --stats-dir ./comparison/before

echo "=== AFTER OPTIMIZATION ==="
python team_aggregator.py aggregate --stats-dir ./comparison/after
```

## Analysis Patterns

### Weekly Tracking

Track week-over-week changes:

```bash
#!/bin/bash
# weekly_analysis.sh

CURRENT_WEEK=$(date +%V)
YEAR=$(date +%Y)

# Export this week
python team_aggregator.py export \
  --output-dir ./weekly/${YEAR}_week${CURRENT_WEEK} \
  --date-from $(date -d "monday this week" +%Y-%m-%d) \
  --date-to $(date -d "sunday this week" +%Y-%m-%d)

# Aggregate
python team_aggregator.py aggregate \
  --stats-dir ./weekly/${YEAR}_week${CURRENT_WEEK} \
  --output ./weekly/${YEAR}_week${CURRENT_WEEK}_report.json
```

### Monthly Dashboard

Create monthly summary:

```bash
#!/bin/bash
# monthly_summary.sh

MONTH=$(date +%m)
YEAR=$(date +%Y)
FIRST_DAY="${YEAR}-${MONTH}-01"
LAST_DAY=$(date -d "${FIRST_DAY} +1 month -1 day" +%Y-%m-%d)

python team_aggregator.py export \
  --output-dir ./monthly/${YEAR}_${MONTH} \
  --date-from ${FIRST_DAY} \
  --date-to ${LAST_DAY}

python team_aggregator.py aggregate \
  --stats-dir ./monthly/${YEAR}_${MONTH}
```

### Sprint Retrospective

Analyze sprint token usage:

```bash
# Sprint 23: Feb 1-14
python team_aggregator.py export \
  --output-dir ./sprints/sprint_23 \
  --date-from 2024-02-01 \
  --date-to 2024-02-14

python team_aggregator.py aggregate --stats-dir ./sprints/sprint_23

# Compare with previous sprint
python team_aggregator.py aggregate --stats-dir ./sprints/sprint_22

# Analysis questions:
# - Did we use more/less tokens?
# - Which projects consumed most tokens?
# - Did optimizations help?
```

### Optimization Impact

Measure before/after optimization:

```bash
# Baseline (before applying optimizations)
python analyze_tokens_v2.py  # Creates snapshot

# Apply optimizations from wizard
# ... work for 2 weeks ...

# After period
python team_aggregator.py export \
  --output-dir ./optimization-tracking/after \
  --date-from 2024-02-12 \
  --date-to 2024-02-26

# Compare
python analyze_tokens_v2.py  # Will show delta from previous snapshot
```

## Metrics to Track

### Session Efficiency

```
Sessions per day = Total Sessions / Days in Period
Messages per session = Total Messages / Total Sessions
```

Lower sessions for same work = more efficient

### Token Efficiency

```
Tokens per message = Total Tokens / Total Messages
Tokens per session = Total Tokens / Total Sessions
```

Lower ratios = more efficient usage

### Category Shifts

Track how category distribution changes:

```
Before: Documentation 30%, Coding 40%, Config 30%
After:  Documentation 15%, Coding 60%, Config 25%

Result: More productive work, less overhead
```

## Example Workflow

### Month 1: Baseline

```bash
# January - no optimizations
python team_aggregator.py export \
  --output-dir ./tracking/month1 \
  --date-from 2024-01-01 \
  --date-to 2024-01-31

python team_aggregator.py aggregate --stats-dir ./tracking/month1
```

Results:
- 50 sessions
- 1,200 messages
- 600,000 tokens
- Documentation: 30% of sessions
- Configuration: 50% of sessions

### Month 2: Apply Optimizations

Run V2 analyzer, apply optimizations:
- Defer documentation
- Create CLAUDE.md files
- Use command-first approach

### Month 3: Measure Impact

```bash
# March - with optimizations
python team_aggregator.py export \
  --output-dir ./tracking/month3 \
  --date-from 2024-03-01 \
  --date-to 2024-03-31

python team_aggregator.py aggregate --stats-dir ./tracking/month3
```

Results:
- 35 sessions (-30%)
- 850 messages (-29%)
- 400,000 tokens (-33%)
- Documentation: 10% of sessions (-67%)
- Configuration: 25% of sessions (-50%)

**Savings: ~33% tokens per month!**

## Automated Tracking

### Cron Job (Linux/Mac)

```bash
# Daily export at midnight
0 0 * * * cd ~/token-analyzer && python team_aggregator.py export --output-dir ~/claude-stats-daily/$(date +\%Y\%m\%d) --date-from $(date +\%Y-\%m-\%d) --date-to $(date +\%Y-\%m-\%d)

# Weekly aggregation on Sundays
0 8 * * 0 cd ~/token-analyzer && python team_aggregator.py aggregate --stats-dir ~/claude-stats-weekly
```

### Task Scheduler (Windows)

Create a batch file `daily_export.bat`:

```batch
@echo off
set TODAY=%DATE:~-4%%DATE:~-10,2%%DATE:~-7,2%
python "C:\path\to\team_aggregator.py" export --output-dir "C:\stats\daily\%TODAY%" --date-from %DATE:~-4%-%DATE:~-10,2%-%DATE:~-7,2%
```

Schedule in Task Scheduler to run daily.

## Visualization

### Export to CSV for Charting

```python
import json
import csv
from glob import glob

# Load all monthly reports
reports = []
for file in sorted(glob('./monthly/*_report.json')):
    with open(file, 'r') as f:
        data = json.load(f)
        reports.append({
            'month': file.split('/')[-1].split('_')[0],
            'sessions': data['totals']['sessions'],
            'messages': data['totals']['messages'],
            'tokens': sum(usage['input'] + usage['output']
                         for usage in data['totals']['tokens'].values())
        })

# Write to CSV
with open('monthly_trends.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['month', 'sessions', 'messages', 'tokens'])
    writer.writeheader()
    writer.writerows(reports)

# Import to Excel/Google Sheets for charting
```

## Key Insights to Look For

### 🚩 Red Flags

- **Increasing sessions for same work** - Efficiency declining
- **High documentation %** - Too much overhead
- **Spike in configuration** - Setup issues
- **Low coding %** - Not productive

### ✅ Good Signs

- **Decreasing tokens/message** - More efficient prompts
- **Increasing coding %** - More productive work
- **Stable or decreasing sessions** - Getting work done faster
- **Low configuration %** - Good project setup

### 📊 Trends to Track

- **Optimization adoption** - Are changes being followed?
- **New project overhead** - Initial setup costs
- **Learning curve** - New tools/frameworks
- **Team onboarding** - New member impact

## Best Practices

1. **Consistent time periods** - Compare apples to apples
2. **Regular exports** - Don't wait too long
3. **Document changes** - Note when optimizations applied
4. **Team communication** - Share findings with team
5. **Iterate** - Adjust strategies based on data
6. **Celebrate wins** - Recognize improvements

## Troubleshooting

**Q: Dates not filtering correctly?**
- Ensure date format: YYYY-MM-DD
- Check timezone (timestamps are in milliseconds)
- Verify --date-from is before --date-to

**Q: No data for time period?**
- Check if you used Claude during that time
- Verify history.jsonl has entries
- Check timestamp format in history

**Q: Comparing different time periods?**
- Use same duration (both 7 days, both 30 days)
- Account for holidays/weekends
- Normalize by working days
