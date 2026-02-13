# Token-Craft Installation Guide

Install the `/token-craft` skill to track and optimize your LLM token usage through gamified space exploration ranks!

## Quick Install

### Step 1: Clone or Download Repository

```bash
# Option A: Clone from GitHub (if published)
git clone https://github.com/DmitriyZhorov/token-analyzer.git
cd claude-token-analyzer

# Option B: Download ZIP and extract
# Download from GitHub releases
# Extract to a permanent location
```

### Step 2: Install the Skill

```bash
# Copy skill to Claude Code skills directory
# Windows:
copy token-craft.md "%USERPROFILE%\.claude\skills\token-craft.md"

# macOS/Linux:
cp token-craft.md ~/.claude/skills/token-craft.md
```

### Step 3: Set Up Python Environment

**No dependencies needed!** Token-Craft uses only Python standard library.

```bash
# Verify Python 3.8+ is installed
python --version

# Optional: Install requests for future hero.epam.com integration
pip install requests
```

### Step 4: Configure Paths

Edit `token-craft.md` and update the path to your installation:

```yaml
# Line ~50 in token-craft.md
# Change this path to where you extracted the repository:
cd /path/to/your/claude-token-analyzer
```

For example:
```yaml
# Windows:
cd C:\tools\claude-token-analyzer

# macOS/Linux:
cd ~/tools/claude-token-analyzer
```

### Step 5: Test Installation

In Claude Code, type:
```
/token-craft
```

You should see your space mission report!

---

## Alternative: Portable Installation

If you want to install Token-Craft in a way that's easier to share with your team:

### 1. Create Shared Directory Structure

```bash
# Create a central location
mkdir -p ~/tools/claude-token-analyzer
cd ~/tools/claude-token-analyzer

# Copy all files
cp -r /path/to/downloaded/token_craft ./
cp /path/to/downloaded/skill_handler*.py ./
cp /path/to/downloaded/token-craft.md ./
```

### 2. Create Wrapper Script

**Windows (`token-craft.bat`):**
```batch
@echo off
python "C:\tools\claude-token-analyzer\skill_handler_full.py" --mode interactive
```

**macOS/Linux (`token-craft.sh`):**
```bash
#!/bin/bash
python3 ~/tools/claude-token-analyzer/skill_handler_full.py --mode interactive
```

Make executable:
```bash
chmod +x ~/tools/claude-token-analyzer/token-craft.sh
```

### 3. Install Skill with Wrapper

Edit `token-craft.md` to call your wrapper:

```yaml
# Windows
cd C:\tools\claude-token-analyzer
token-craft.bat

# macOS/Linux
cd ~/tools/claude-token-analyzer
./token-craft.sh
```

---

## Team Installation (For Organizations)

### Option 1: Shared Network Drive

1. **IT Admin:** Install Token-Craft to shared network location
   ```
   \\company-server\tools\claude-token-analyzer\
   ```

2. **Each User:** Copy skill file to their Claude directory
   ```batch
   copy \\company-server\tools\claude-token-analyzer\token-craft.md %USERPROFILE%\.claude\skills\
   ```

3. **Each User:** Skill automatically points to shared installation

### Option 2: Internal GitHub/GitLab

1. **IT Admin:** Create internal repository
   ```bash
   git clone https://github.com/DmitriyZhorov/token-analyzer.git
   cd claude-token-analyzer
   git remote set-url origin https://internal-git.company.com/tools/token-craft.git
   git push -u origin master
   ```

2. **Each User:** Clone and install
   ```bash
   git clone https://internal-git.company.com/tools/token-craft.git ~/tools/token-craft
   cp ~/tools/token-craft/token-craft.md ~/.claude/skills/
   ```

3. **Updates:** Users pull latest changes
   ```bash
   cd ~/tools/token-craft
   git pull
   ```

---

## Verification

After installation, verify everything works:

### Test 1: Basic Command
```bash
cd /path/to/claude-token-analyzer
python skill_handler.py --mode quick
```

**Expected output:**
```
👨‍✈️ [Your Rank] - [Your Score] points
```

### Test 2: Full Report
```bash
python skill_handler.py --mode summary
```

**Expected output:**
```
==================================================
            TOKEN-CRAFT QUICK SUMMARY
==================================================

Rank: [Your Rank] 🚀
Score: [Your Score]/1000
...
```

### Test 3: Interactive Mode
```bash
python skill_handler_full.py --mode interactive
```

**Expected output:**
```
Loading your data...
Calculating your scores...
...
[Full report with menu]
```

### Test 4: Claude Skill
In Claude Code:
```
/token-craft
```

**Expected:** Claude runs the skill and shows your report

---

## Troubleshooting

### Issue: Skill not found
**Solution:** Verify skill file location
```bash
# Check if skill file exists
# Windows:
dir %USERPROFILE%\.claude\skills\token-craft.md

# macOS/Linux:
ls ~/.claude/skills/token-craft.md
```

### Issue: Python not found
**Solution:** Install Python 3.8+
- Windows: https://python.org/downloads
- macOS: `brew install python3`
- Linux: `sudo apt install python3`

### Issue: ModuleNotFoundError
**Solution:** Verify you're in the correct directory
```bash
cd /path/to/claude-token-analyzer
python -c "import token_craft; print('OK')"
```

### Issue: Permission denied
**Solution:** Run with proper permissions
```bash
# macOS/Linux:
chmod +x skill_handler.py
chmod +x skill_handler_full.py
```

### Issue: Unicode errors on Windows
**Already fixed!** The code handles Windows CMD encoding automatically.

---

## Configuration

### Change Skill Trigger

Edit `token-craft.md`:
```yaml
triggers:
  - /token-craft        # Full name
  - /tc                 # Shortcut
  - /optimize-tokens    # Add custom trigger
```

### Change Default Mode

Edit `token-craft.md` to change default behavior:
```bash
# Current: Full report
python skill_handler.py --mode full

# Change to: Interactive
python skill_handler_full.py --mode interactive

# Change to: Quick status
python skill_handler.py --mode quick
```

### Customize Baseline

Edit `token_craft/scoring_engine.py`:
```python
# Line ~28
DEFAULT_BASELINE = {
    "tokens_per_session": 15000,  # Adjust for your company
    "tokens_per_message": 1500,
    # ...
}
```

---

## Uninstallation

### Remove Skill
```bash
# Windows:
del %USERPROFILE%\.claude\skills\token-craft.md

# macOS/Linux:
rm ~/.claude/skills/token-craft.md
```

### Remove Data (Optional)
```bash
# Windows:
rmdir /s %USERPROFILE%\.claude\token-craft

# macOS/Linux:
rm -rf ~/.claude/token-craft
```

### Remove Code
```bash
# Delete the installation directory
rm -rf /path/to/claude-token-analyzer
```

---

## Updates

### Manual Update
```bash
cd /path/to/claude-token-analyzer
git pull origin master

# Or download new ZIP and replace files
```

### Check Version
```bash
python -c "import token_craft; print(token_craft.__version__)"
```

**Current Version:** 1.0.0

---

## Getting Help

### Documentation
- **Quick Start:** See `QUICK_START.md`
- **Full Guide:** See `README.md`
- **Interactive Guide:** See `INTERACTIVE_GUIDE.md`

### Community
- **Issues:** https://github.com/DmitriyZhorov/token-analyzer/issues
- **Discussions:** https://github.com/DmitriyZhorov/token-analyzer/discussions

---

## Next Steps After Installation

1. **Run your first analysis:** `/token-craft`
2. **Check your rank:** See where you stand (Cadet → Galactic Legend)
3. **Apply optimizations:** Use interactive mode [A] option
4. **Track progress:** Run weekly to see improvement
5. **Share with team:** Export stats and build leaderboards

---

## System Requirements

- **Python:** 3.8 or higher
- **OS:** Windows, macOS, Linux
- **Disk Space:** ~5MB for code + ~100KB per user for data
- **Memory:** <50MB during analysis
- **Network:** None required (all local)

---

**Installation Complete!** 🚀

Run `/token-craft` to start your space exploration journey!
