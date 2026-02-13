# Token-Craft - Shareable Package Guide

## What is Token-Craft?

**Token-Craft** is a Claude Code skill that gamifies LLM token optimization through space exploration ranks. Track your efficiency, earn achievements, and compete on leaderboards!

```
👨‍✈️ Current Rank: Captain
🎯 Score: 835 / 1000 points
🏆 Achievements: Efficiency Master, Halfway There
📈 30% better efficiency than baseline
```

---

## Package Contents

This repository contains everything needed to run Token-Craft:

```
claude-token-analyzer/
├── token-craft.md              # Claude Skill definition (INSTALL THIS)
├── skill_handler.py            # Basic entry point
├── skill_handler_full.py       # Full featured with interactive menu
│
├── token_craft/                # Core package (13 modules)
│   ├── scoring_engine.py       # 5-category scoring system
│   ├── rank_system.py          # 7 space exploration ranks
│   ├── user_profile.py         # User state management
│   ├── snapshot_manager.py     # Historical progress tracking
│   ├── delta_calculator.py     # Compare snapshots
│   ├── report_generator.py     # Beautiful ASCII reports
│   ├── progress_visualizer.py  # Progress bars & badges
│   ├── leaderboard_generator.py # Team rankings
│   ├── hero_api_client.py      # Badge integration
│   ├── team_exporter.py        # Export stats for team
│   ├── recommendation_engine.py # Personalized suggestions
│   └── interactive_menu.py     # Interactive UI
│
├── tests/                      # Unit tests
├── docs/                       # Full documentation
└── INSTALL.md                  # Installation guide
```

---

## Quick Start (3 Steps)

### 1. Download
```bash
# Clone from GitHub
git clone https://github.com/DmitriyZhorov/claude-token-analyzer.git
cd claude-token-analyzer
```

### 2. Install Skill
```bash
# Copy skill to Claude Code
cp token-craft.md ~/.claude/skills/token-craft.md
```

### 3. Run
```bash
# In Claude Code, type:
/token-craft
```

**That's it!** See full installation instructions in `INSTALL.md`

---

## For Team Distribution

### Option 1: Direct File Sharing

**Package to share:**
1. ZIP this entire repository
2. Include `INSTALL.md` in the ZIP
3. Share via:
   - Email attachment
   - Shared network drive
   - Internal file server
   - Slack/Teams file upload

**Recipients:**
1. Extract ZIP
2. Follow `INSTALL.md`
3. Run `/token-craft`

### Option 2: Internal Git Repository

**Setup:**
```bash
# IT Admin creates internal repo
git clone https://github.com/DmitriyZhorov/claude-token-analyzer.git
cd claude-token-analyzer
git remote set-url origin https://internal-git.company.com/tools/token-craft.git
git push -u origin master
```

**Team Members:**
```bash
# Clone from internal repo
git clone https://internal-git.company.com/tools/token-craft.git
cd token-craft
cp token-craft.md ~/.claude/skills/
```

**Benefits:**
- Easy updates (`git pull`)
- Version control
- Team modifications tracked
- Secure (internal network)

### Option 3: Network Share

**IT Admin:**
```bash
# Install to network location
\\company-server\tools\claude-token-analyzer\
```

**Team Members:**
```bash
# Copy skill file only
copy \\company-server\tools\claude-token-analyzer\token-craft.md %USERPROFILE%\.claude\skills\
```

Skill automatically points to shared installation!

---

## What Recipients Get

### Features
✅ **Personal Analytics**
- Real-time token efficiency scoring
- 7 space exploration ranks (Cadet → Galactic Legend)
- Progress tracking with snapshots
- Personalized recommendations

✅ **Gamification**
- Achievement system
- Progress bars and badges
- Rank progression (can go up or down!)
- Visual reports

✅ **Team Features**
- Export stats for team leaderboards
- Company/project/department rankings
- Privacy-preserving anonymous mode
- Team stats aggregation

✅ **Interactive Experience**
- Full interactive menu
- One-click optimization application
- Detailed recommendations
- Achievement gallery

### No Setup Required (Almost!)
- Zero external dependencies (Python standard library only)
- No API keys needed
- No database setup
- No configuration files
- Just install and run!

---

## System Requirements

**Minimum:**
- Python 3.8+
- Claude Code installed
- 5MB disk space
- Any OS (Windows/macOS/Linux)

**Recommended:**
- Python 3.10+
- 10MB disk space (for snapshots)
- Git (for easy updates)

---

## Documentation Included

1. **INSTALL.md** - Step-by-step installation
2. **TOKEN_CRAFT_README.md** - Complete user guide
3. **QUICK_START.md** - Quick reference
4. **SCORING_AND_BONUSES_EXPLAINED.md** - How scoring works
5. **IMPLEMENTATION_COMPLETE.md** - Technical details
6. **This file** - Sharing guide

---

## Customization for Your Organization

### 1. Change Company Baseline

Edit `token_craft/scoring_engine.py`:
```python
DEFAULT_BASELINE = {
    "tokens_per_session": 15000,  # Adjust based on your company data
    "tokens_per_message": 1500,
    # ...
}
```

### 2. Customize Ranks

Edit `token_craft/rank_system.py`:
```python
RANKS = [
    {"name": "Cadet", "min": 0, "max": 199},
    # Modify thresholds as needed
]
```

### 3. Add Custom Achievements

Edit `skill_handler_full.py`:
```python
def _check_achievements(self, score_data, rank_data, delta_data):
    # Add your custom achievements here
    if score >= 750:
        self.profile.add_achievement(
            "company_hero",
            "Company Hero",
            "Top 10% in the company"
        )
```

### 4. Integrate with hero.epam.com

Edit `token_craft/hero_api_client.py`:
```python
def __init__(self, api_url: str = None, api_key: str = None):
    self.api_url = api_url or "https://hero.epam.com/api"
    self.api_key = api_key  # Add your API key
```

---

## Support & Maintenance

### Getting Help
- **Quick issues:** Check `INSTALL.md` troubleshooting section
- **Usage questions:** Read `TOKEN_CRAFT_README.md`
- **Bug reports:** GitHub Issues
- **Feature requests:** GitHub Discussions

### Updates
```bash
cd claude-token-analyzer
git pull origin master
```

### Version
**Current:** 1.0.0 (February 2026)

---

## Security & Privacy

### Data Storage
- **All local:** No data sent to external servers
- **User privacy:** Anonymous leaderboards by default
- **No tracking:** No analytics or telemetry
- **Secure:** Uses only local files

### What's Stored
```
~/.claude/token-craft/
├── snapshots/           # Your historical progress (JSON)
├── user_profile.json    # Your current state
└── team-exports/        # Stats you choose to export
```

### Team Sharing
- Export is **opt-in only**
- You control what's shared
- Anonymous IDs in leaderboards
- No personal data required

---

## License & Attribution

**Creator:** Dmitriy Zhorov (EPAM)
**Date:** February 2026
**License:** Internal EPAM tool (check with legal for external distribution)

**Inspiration:** Demo scene constraint programming culture (64KB demos, assembly optimization)

---

## Sharing Checklist

When sharing Token-Craft with your team:

- [ ] Package entire repository (ZIP or Git)
- [ ] Include `INSTALL.md` (mandatory!)
- [ ] Include `TOKEN_CRAFT_README.md` (recommended)
- [ ] Test installation on clean machine
- [ ] Provide your contact info for support
- [ ] Set up internal support channel (Slack/Teams)
- [ ] Consider customizing company baseline
- [ ] Plan first team leaderboard (after 5-10 users)

---

## Example Sharing Message

```
Subject: 🚀 Token-Craft: Optimize Your AI Token Usage!

Hi Team,

I'm excited to share Token-Craft - a tool that helps you track and
optimize your Claude Code token usage through gamified ranks!

📦 Installation:
1. Download: [link to ZIP or git repo]
2. Extract to any folder
3. Follow INSTALL.md (2 minutes)
4. Run: /token-craft in Claude Code

🎮 What You'll Get:
- Your space exploration rank (Cadet → Galactic Legend)
- Personalized optimization recommendations
- Achievement system and progress tracking
- Team leaderboards (coming soon!)

🏆 Current Stats:
I'm a Captain (835/1000 points) with 30% better efficiency than baseline!

📚 Documentation:
- Quick Start: See QUICK_START.md
- Full Guide: See TOKEN_CRAFT_README.md
- Support: Message me or check docs

Let's optimize together! 🚀

[Your Name]
```

---

## FAQs for Recipients

**Q: Do I need to install anything?**
A: Just Python 3.8+ (probably already have it). No other dependencies!

**Q: Will this slow down Claude Code?**
A: No! Analysis runs separately, takes 2-3 seconds.

**Q: Is my data shared?**
A: Only if you explicitly export it. Everything is local by default.

**Q: Can I use this without a team?**
A: Absolutely! All features work solo. Team features are optional.

**Q: How often should I run it?**
A: Weekly is ideal for tracking trends. Daily if actively optimizing.

**Q: What if I'm not technical?**
A: It's designed for everyone! Just type `/token-craft` and follow the menu.

---

## Success Stories (Example)

*"After using Token-Craft for 2 weeks, I reduced my token usage by 28%
by applying just 3 recommendations: deferring docs, using CLAUDE.md,
and running simple commands directly. I reached Navigator rank!"*
— Your Future Teammate

---

**Ready to Share?**

1. ZIP this repository
2. Include this file (SHARE_PACKAGE.md) and INSTALL.md
3. Share with your team
4. Watch them become space explorers! 🚀

---

Questions? Contact: Dmitriy Zhorov <dmitriy_zhorov@epam.com>
