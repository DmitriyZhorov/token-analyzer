# Claude Code Token Analyzer V2

## 🚀 What's New in V2

Complete redesign with advanced features:
- **Scope Selection**: Choose which projects/users to analyze
- **Thorough Pattern Analysis**: Deep dive into token usage patterns
- **Interactive Optimization**: One-by-one optimization with trade-off analysis
- **Delta Tracking**: Compare improvements over time
- **Detailed Estimations**: See expected savings before applying changes

## Features

### 1. Scope Selection Phase
- Lists all available projects from your Claude Code history
- Shows session count and message count per project
- Select specific projects or analyze everything
- "ALL PROJECTS" quick option

### 2. Thorough Analysis Phase
Analyzes your selected scope for:
- **Work Type Distribution**: Coding, Data Processing, DevOps, Research, Maintenance
- **Task Categories**: Git, Files, Debugging, Documentation, etc.
- **Project Breakdown**: Stats per project with averages
- **Pattern Detection**: Identifies inefficient patterns

### 3. Detailed Breakdown
- Sort and filter results by project
- View average message lengths
- See top work types per project
- Identify heaviest token consumers

### 4. Optimization Opportunities
Identifies opportunities in:
- **Documentation Timing**: When to write docs
- **Configuration Overhead**: Setup inefficiencies
- **Search & Exploration**: Command alternatives
- **File Operations**: Direct vs AI-assisted
- **Response Verbosity**: Output/input ratios
- **Work Type Specific**: Research, coding, data processing

### 5. Interactive Optimization Selection
For each opportunity, you see:
- Current state and problem description
- 3-4 available options
- Estimated savings range (e.g., "15-25%")
- Trade-offs for each option
- Choose option or skip

Examples:
```
[HIGH] Configuration Overhead
Current State: 52.6% of sessions on setup/config
Problem: Repeated configuration and setup questions

Options:
  [1] CLAUDE.md All Projects
      Create comprehensive CLAUDE.md for every project
      Estimated savings: 30-40%
      Trade-off: Upfront time investment

  [2] Memory-Based Learning
      Rely on MEMORY.md to learn patterns
      Estimated savings: 15-20%
      Trade-off: Takes time to build up memory

  [3] Project Templates
      Use standardized project templates
      Estimated savings: 20-30%
      Trade-off: Less flexibility per project

Select option (0-3):
```

### 6. Optimization Summary
- Shows all selected optimizations
- Calculates total estimated improvement
- Example: "25%-45% total savings"
- Applies changes with your confirmation

### 7. Snapshot & Delta Tracking
- Saves timestamped snapshot after each run
- Stored in: `~/.claude/token-analyzer-snapshots/`
- Next run compares against previous snapshot
- Shows actual improvement metrics
- Category-by-category comparison

## Usage

### Basic Usage
```bash
python analyze_tokens_v2.py
```

### Workflow

**First Run:**
1. Select projects to analyze (or "0" for all)
2. Review detailed breakdown
3. Confirm to proceed to optimization
4. Go through each opportunity one-by-one
5. Select your preferred option for each
6. Review summary and estimated savings
7. Confirm to apply changes
8. Snapshot saved automatically

**Subsequent Runs:**
1. Tool detects previous snapshot
2. Option to compare before proceeding
3. See what optimizations were applied before
4. Complete same analysis flow
5. At end, see delta comparison:
   - Session count changes
   - Message count changes
   - Category-by-category changes
   - Actual vs estimated improvements

## Example Output

```
[+] IMPROVEMENT ANALYSIS

Previous snapshot: 2024-02-12T18:00:00
Applied optimizations:
  - Documentation Timing: Strict Defer (20-25%)
  - Configuration Overhead: CLAUDE.md All Projects (30-40%)

[+] Session Comparison:
    Before: 15 sessions
    Now: 12 sessions
    Change: -20.0%

[+] Category Changes:
    Documentation: 5 → 2 (-60%) ↓
    Configuration: 10 → 5 (-50%) ↓
    Code Writing: 3 → 5 (+66%) ↑
```

## Files Created

The tool creates/updates:
- `~/.claude/token-analyzer-snapshots/snapshot_YYYYMMDD_HHMMSS.json` - Analysis snapshots
- Project `CLAUDE.md` files - Based on selected optimizations
- `~/CLAUDE_TEMPLATE.md` - Project template
- `~/claude_commands_cheatsheet.txt` - Command reference

## Snapshot Format

```json
{
  "timestamp": "20240212_180000",
  "datetime": "2024-02-12T18:00:00",
  "analysis": {
    "total_sessions": 15,
    "total_messages": 8864,
    "category_counts": {...},
    "work_type_counts": {...},
    "project_stats": {...}
  },
  "optimizations": [
    {
      "category": "Documentation Timing",
      "selected": "Strict Defer",
      "estimated_savings": "20-25%"
    }
  ]
}
```

## Comparison with V1

| Feature | V1 | V2 |
|---------|----|----|
| Scope selection | ❌ | ✅ |
| Work type analysis | ❌ | ✅ |
| Interactive optimization | Basic | Advanced |
| Trade-off analysis | ❌ | ✅ |
| Estimated savings | ❌ | ✅ |
| Delta tracking | ❌ | ✅ |
| Improvement measurement | ❌ | ✅ |
| Snapshot history | ❌ | ✅ |

## Tips

1. **Run regularly** (weekly/bi-weekly) to track improvements
2. **Be selective** with scope - analyze specific projects when debugging patterns
3. **Review trade-offs carefully** - highest savings isn't always best choice
4. **Compare deltas** - measure actual vs estimated improvements
5. **Iterate** - apply some optimizations, measure, then apply more

## Requirements

- Python 3.7+
- Claude Code with usage history
- `~/.claude/history.jsonl` and `~/.claude/stats-cache.json`

## Advanced Usage

### Analyze Single Project
When prompted for scope, enter the project number:
```
Your choice: 5
```

### Analyze Multiple Specific Projects
```
Your choice: 1 3 5
```

### Skip Optimization Wizard
At "Proceed to optimization insights?" prompt:
```
Proceed to optimization insights? (y/n): n
```

### Review Previous Snapshots
```bash
ls ~/.claude/token-analyzer-snapshots/
cat ~/.claude/token-analyzer-snapshots/snapshot_20240212_180000.json
```
