# Team Leaderboards with GitHub

**Quick Setup Guide for Team Statistics Aggregation**

---

## Overview

Token-Craft supports team leaderboards using a GitHub repository for data aggregation. This is a **free, simple solution** that requires no server infrastructure.

**Benefits:**
- ✅ Free (GitHub)
- ✅ Version control (full audit trail)
- ✅ Easy setup (< 30 minutes)
- ✅ Works with existing Git workflow
- ✅ No server management required

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 GitHub Repository                        │
│          company-token-craft-stats (Private)            │
├─────────────────────────────────────────────────────────┤
│  team-stats/                                             │
│  ├── user1@company_20260213.json    # Auto-uploaded     │
│  ├── user2@company_20260213.json                        │
│  └── userN@company_20260213.json                        │
│                                                          │
│  leaderboards/                                           │
│  ├── company_latest.json            # Auto-generated    │
│  ├── company_weekly.json                                │
│  └── company_monthly.json                               │
│                                                          │
│  README.md                          # Team docs          │
└─────────────────────────────────────────────────────────┘
           ▲                                    │
           │ git push (automated)               │ git pull (read)
           │                                    ▼
┌──────────┴────────┐  ┌───────────────┐  ┌───────────────┐
│  Team Member 1    │  │ Team Member 2  │  │ Team Member N  │
│  ~/.claude/       │  │ ~/.claude/     │  │ ~/.claude/     │
│  token-craft/     │  │ token-craft/   │  │ token-craft/   │
└───────────────────┘  └───────────────┘  └───────────────┘
```

---

## Step 1: Create GitHub Repository

### 1.1 Create Private Repository

```bash
# Using GitHub CLI (recommended)
gh repo create company-token-craft-stats --private --description "Team Token-Craft statistics"

# OR via web: https://github.com/new
# - Name: company-token-craft-stats
# - Visibility: Private
# - Initialize with README
```

### 1.2 Clone Repository Locally

```bash
# Choose a shared location accessible to automation
git clone git@github.com:yourcompany/company-token-craft-stats.git

# OR if you prefer HTTPS:
git clone https://github.com/yourcompany/company-token-craft-stats.git
```

### 1.3 Set Up Directory Structure

```bash
cd company-token-craft-stats

# Create directories
mkdir -p team-stats leaderboards benchmarks

# Create README
cat > README.md <<'EOF'
# Company Token-Craft Statistics

Team leaderboards and optimization tracking.

## Directories

- `team-stats/` - Individual user statistics (auto-uploaded)
- `leaderboards/` - Generated leaderboards (auto-generated)
- `benchmarks/` - Company baseline metrics

## Usage

Stats are automatically uploaded when users run `/token-craft`.
Leaderboards are regenerated daily.

## Privacy

All data is company-internal and stored in private repository.
Individual stats show user email but can be anonymized.
EOF

# Initial commit
git add .
git commit -m "chore: Initialize team stats repository"
git push origin main
```

---

## Step 2: Configure Token-Craft

### 2.1 Update User Configuration

Edit each team member's `~/.claude/token-craft/user_profile.json`:

```json
{
  "user_email": "user@company.com",
  "team_settings": {
    "enabled": true,
    "repo_path": "/path/to/company-token-craft-stats",
    "auto_push": true,
    "push_frequency": "daily",
    "anonymous": false
  },
  "budget_config": {
    "daily_budget": 5.00,
    "monthly_budget": 100.00,
    "alerts_enabled": true
  }
}
```

**Configuration Options:**

| Setting | Description | Default |
|---------|-------------|---------|
| `enabled` | Enable team features | `false` |
| `repo_path` | Path to cloned repo | Required |
| `auto_push` | Auto-push stats to GitHub | `true` |
| `push_frequency` | `daily`, `weekly`, `manual` | `daily` |
| `anonymous` | Use anonymous ID in leaderboards | `false` |

### 2.2 Test Configuration

```bash
# Run Token-Craft
/token-craft

# Check if export was created
ls ~/.claude/token-craft/team-exports/

# Should see: user@company_YYYYMMDD_HHMMSS.json
```

---

## Step 3: Set Up Auto-Push (Optional)

### Option A: Git Hook (Recommended)

Create `~/.claude/token-craft/hooks/post-export.sh`:

```bash
#!/bin/bash
# Post-export hook - automatically push stats to GitHub

TEAM_REPO="/path/to/company-token-craft-stats"
EXPORT_FILE="$1"  # Passed by Token-Craft

if [ ! -d "$TEAM_REPO" ]; then
    echo "Team repo not found: $TEAM_REPO"
    exit 1
fi

# Copy export to team repo
cp "$EXPORT_FILE" "$TEAM_REPO/team-stats/"

# Commit and push
cd "$TEAM_REPO"
git add team-stats/
git commit -m "chore: Update stats for $(basename $EXPORT_FILE .json)"
git push origin main

echo "✅ Stats pushed to team repository"
```

Make executable:

```bash
chmod +x ~/.claude/token-craft/hooks/post-export.sh
```

### Option B: Manual Push

```bash
# After running /token-craft, manually copy and push
cp ~/.claude/token-craft/team-exports/latest.json \
   /path/to/company-token-craft-stats/team-stats/

cd /path/to/company-token-craft-stats
git add team-stats/
git commit -m "chore: Update team stats"
git push origin main
```

### Option C: Scheduled Cron Job

```bash
# Add to crontab: crontab -e

# Daily at 6 PM - push stats to team repo
0 18 * * * /path/to/token-craft-push-script.sh
```

**Script: `token-craft-push-script.sh`**

```bash
#!/bin/bash
TEAM_REPO="/path/to/company-token-craft-stats"
EXPORTS_DIR="$HOME/.claude/token-craft/team-exports"

# Copy all today's exports
TODAY=$(date +%Y%m%d)
cp "$EXPORTS_DIR"/*_${TODAY}_*.json "$TEAM_REPO/team-stats/" 2>/dev/null

# Commit and push
cd "$TEAM_REPO"
if [ -n "$(git status --porcelain)" ]; then
    git add team-stats/
    git commit -m "chore: Daily stats update $(date +%Y-%m-%d)"
    git push origin main
    echo "✅ Stats pushed"
else
    echo "ℹ️  No new stats to push"
fi
```

---

## Step 4: Generate Leaderboards

### 4.1 Manual Generation

```python
# scripts/generate_leaderboards.py
from pathlib import Path
import sys

# Add token_craft to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from token_craft.leaderboard_generator import LeaderboardGenerator

# Initialize
stats_dir = Path("/path/to/company-token-craft-stats/team-stats")
output_dir = Path("/path/to/company-token-craft-stats/leaderboards")
output_dir.mkdir(exist_ok=True)

generator = LeaderboardGenerator(stats_dir)

# Generate company leaderboard
print("Generating company leaderboard...")
leaderboard = generator.generate_company_leaderboard(anonymous=False)

# Save to file
output_file = output_dir / "company_latest.json"
generator.export_leaderboard(leaderboard, output_file)

# Print formatted leaderboard
print(generator.format_leaderboard(leaderboard))

print(f"\n✅ Leaderboard saved to: {output_file}")
```

Run:

```bash
cd /path/to/token-analyzer
python scripts/generate_leaderboards.py
```

### 4.2 Automated Generation (GitHub Actions)

Create `.github/workflows/generate-leaderboards.yml`:

```yaml
name: Generate Leaderboards

on:
  push:
    branches: [ main ]
    paths:
      - 'team-stats/*.json'
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:  # Manual trigger

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          git clone https://github.com/DmitriyZhorov/token-analyzer.git
          cd token-analyzer
          pip install -e .

      - name: Generate leaderboards
        run: |
          python token-analyzer/scripts/generate_leaderboards.py

      - name: Commit leaderboards
        run: |
          git config user.name "Token-Craft Bot"
          git config user.email "bot@company.com"
          git add leaderboards/
          git diff --quiet || git commit -m "chore: Update leaderboards [skip ci]"
          git push
```

This will:
- Auto-generate leaderboards when stats are pushed
- Run daily at midnight
- Can be manually triggered

---

## Step 5: View Leaderboards

### 5.1 In Terminal

```bash
cd /path/to/company-token-craft-stats
git pull  # Get latest

# View company leaderboard
cat leaderboards/company_latest.json | jq '.rankings[] | "\(.rank). \(.name) - \(.score) pts"'
```

### 5.2 In Token-Craft

```python
# Add to token_craft CLI
/token-team leaderboard
```

### 5.3 Via Web (Optional)

Create `index.html` for GitHub Pages:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Token-Craft Leaderboard</title>
    <style>
        body { font-family: monospace; max-width: 800px; margin: 50px auto; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        .gold { color: gold; }
        .silver { color: silver; }
        .bronze { color: #CD7F32; }
    </style>
</head>
<body>
    <h1>🚀 Company Token-Craft Leaderboard</h1>
    <div id="leaderboard"></div>
    <script>
        fetch('leaderboards/company_latest.json')
            .then(r => r.json())
            .then(data => {
                const rankings = data.rankings;
                let html = '<table><tr><th>Rank</th><th>Name</th><th>Level</th><th>Score</th></tr>';

                rankings.forEach(r => {
                    let rank_display = r.rank;
                    let class_name = '';
                    if (r.rank === 1) { rank_display = '🥇'; class_name = 'gold'; }
                    else if (r.rank === 2) { rank_display = '🥈'; class_name = 'silver'; }
                    else if (r.rank === 3) { rank_display = '🥉'; class_name = 'bronze'; }

                    html += `<tr class="${class_name}">
                        <td>${rank_display}</td>
                        <td>${r.name}</td>
                        <td>${r.rank_title}</td>
                        <td>${r.score}</td>
                    </tr>`;
                });

                html += '</table>';
                document.getElementById('leaderboard').innerHTML = html;
            });
    </script>
</body>
</html>
```

Enable GitHub Pages:
1. Go to repository Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/` (root)
4. Save

Access at: `https://yourcompany.github.io/company-token-craft-stats/`

---

## Step 6: Privacy & Security

### 6.1 Repository Access

```bash
# Add team members
gh repo edit company-token-craft-stats --add-collaborator user@company.com

# Set permissions
gh api repos/yourcompany/company-token-craft-stats/collaborators/user@company.com \
  -X PUT -f permission=push
```

### 6.2 Anonymous Mode

If you want anonymous leaderboards, update configuration:

```json
{
  "team_settings": {
    "anonymous": true
  }
}
```

Leaderboard will show: `Anonymous_#1234` instead of emails.

### 6.3 Data Retention

```bash
# Keep only last 30 days of stats
find team-stats/ -name "*.json" -mtime +30 -delete
git add team-stats/
git commit -m "chore: Clean up old stats"
git push
```

---

## Troubleshooting

### Issue: Stats not pushing

**Check:**
1. Repo path correct in `user_profile.json`?
2. Git credentials configured (`git config user.email`)?
3. SSH key added to GitHub?
4. Permissions to push to repo?

**Test manually:**
```bash
cd /path/to/company-token-craft-stats
touch test.txt
git add test.txt
git commit -m "test"
git push  # Should work without password
```

### Issue: Leaderboard empty

**Check:**
1. Stats files in `team-stats/` directory?
2. JSON files valid? (`jq . team-stats/*.json`)
3. File naming correct? (`user@company_YYYYMMDD_HHMMSS.json`)

### Issue: Permission denied

```bash
# Add SSH key to GitHub
ssh-keygen -t ed25519 -C "token-craft@company.com"
cat ~/.ssh/id_ed25519.pub  # Add to GitHub Settings → SSH Keys
```

---

## Advanced: Cloud Storage Alternative

If GitHub doesn't work, use cloud storage:

### AWS S3 Free Tier

```bash
# Install AWS CLI
pip install awscli

# Configure
aws configure

# Sync stats
aws s3 sync ~/.claude/token-craft/team-exports/ s3://company-token-craft/team-stats/
```

### Cloudflare R2 (10GB free forever)

```bash
# Install rclone
# Configure R2 bucket
rclone sync ~/.claude/token-craft/team-exports/ r2:company-token-craft/team-stats/
```

---

## Summary

**Setup Time:** ~30 minutes
**Cost:** $0 (free GitHub)
**Maintenance:** Minimal (automated)

**Weekly Workflow:**
1. Team members run `/token-craft` (auto-exports)
2. Stats auto-push to GitHub (daily)
3. Leaderboards auto-generate (GitHub Actions)
4. Team views leaderboards (terminal or web)

**Result:** Team visibility, friendly competition, shared optimization goals!

---

## Questions?

- 📖 Full docs: `docs/TOKEN_CRAFT_ENHANCEMENT_ANALYSIS.md`
- 🐛 Issues: https://github.com/DmitriyZhorov/token-analyzer/issues
- 💬 Slack: #token-craft (if available)

**Happy optimizing! 🚀**
