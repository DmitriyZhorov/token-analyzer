# Token-Craft Claude Skill Installation

**Skill Name:** `/token-craft`
**Version:** 1.1.0
**Skill Type:** Personal (available across all projects)

---

## What is the Token-Craft Skill?

The Token-Craft skill integrates directly with Claude Code, allowing you to check your token optimization score and get personalized recommendations using the `/token-craft` slash command from anywhere.

**Example:**
```
/token-craft
```

Claude will run the analysis and show your:
- Current space exploration rank
- Score breakdown across 5 categories
- Top optimization opportunities
- Progress since last check
- Unlocked achievements

---

## Installation

### Step 1: Verify Skill File Location

The skill file should be at:
```
~/.claude/skills/token-craft/SKILL.md
```

**Windows:** `C:\Users\<USERNAME>\.claude\skills\token-craft\SKILL.md`
**macOS/Linux:** `~/.claude/skills/token-craft/SKILL.md`

### Step 2: Copy Skill File

**Option A: Manual Copy (if not already there)**

Copy the skill file from this repository:
```bash
# Windows
mkdir "%USERPROFILE%\.claude\skills\token-craft"
copy token-craft-skill\SKILL.md "%USERPROFILE%\.claude\skills\token-craft\SKILL.md"

# macOS/Linux
mkdir -p ~/.claude/skills/token-craft
cp token-craft-skill/SKILL.md ~/.claude/skills/token-craft/SKILL.md
```

**Option B: Already Installed (this repo)**

If you cloned this repo to the standard location, the skill is already at:
```
C:\Users\Dmitriy_Zhorov\.claude\skills\token-craft\SKILL.md
```

No action needed! ✅

### Step 3: Verify Installation

In Claude Code, type:
```
What skills are available?
```

You should see `token-craft` in the list.

---

## How to Use

### Invoke Directly

```
/token-craft
```

The skill will present an interactive menu:
```
[1] Full Report (detailed breakdown with recommendations)
[2] Quick Summary (rank and score overview)
[3] One-Line Status (just rank and score)
[4] JSON Output (for programmatic access)
[Q] Quit
```

### Let Claude Invoke Automatically

Just ask naturally:
```
How's my token efficiency?
Check my Token-Craft score
Show me my optimization progress
What's my current rank?
```

Claude will automatically invoke the skill when relevant.

---

## Skill Configuration

The skill uses these frontmatter settings:

```yaml
name: token-craft
description: Master LLM efficiency through space exploration ranks...
disable-model-invocation: false  # Claude can auto-invoke
user-invocable: true             # You can invoke with /token-craft
```

### Customization Options

You can edit `~/.claude/skills/token-craft/SKILL.md` to:

1. **Prevent auto-invocation** (manual only):
   ```yaml
   disable-model-invocation: true
   ```

2. **Change the argument hint**:
   ```yaml
   argument-hint: [quick|summary|full]
   ```

3. **Hide from menu** (background only):
   ```yaml
   user-invocable: false
   ```

---

## What the Skill Does

### 1. Analyzes Your Usage
- Scans `~/.claude/history.jsonl`
- Calculates token efficiency metrics
- Measures adoption of 8 Anthropic best practices

### 2. Assigns Your Rank
7 space exploration ranks based on score:
- 🎓 Cadet (0-199)
- ✈️ Pilot (200-399)
- 🧭 Navigator (400-599)
- ⭐ Commander (600-799)
- 👨‍✈️ Captain (800-999)
- 🎖️ Admiral (1000-1199)
- 🌌 Galactic Legend (1200+)

### 3. Tracks 8 Best Practices
- Defer Documentation (50 pts)
- Use CLAUDE.md (50 pts)
- Concise Response Mode (40 pts)
- Direct Commands (60 pts)
- Context Management (50 pts)
- XML Tags Usage (20 pts) ✨ NEW
- Chain of Thought (30 pts) ✨ NEW
- Examples Usage (25 pts) ✨ NEW

### 4. Provides Recommendations
Personalized suggestions with:
- Impact estimate (+X points)
- Token savings potential
- Specific action steps

### 5. Tracks Progress
- Creates snapshots after each run
- Compares to previous state
- Shows trend indicators (↑↓→)
- Unlocks achievements

---

## Technical Details

### Execution Path

When you invoke `/token-craft`, the skill:

1. Changes directory to:
   ```
   C:\Users\Dmitriy_Zhorov\Documents\Personal\GenAI\token-analyzer
   ```

2. Runs the interactive handler:
   ```bash
   python skill_handler.py
   ```

3. Presents the interactive menu (no parameters needed!)

4. Returns the formatted report to Claude

5. Claude presents the results to you with context and recommendations

### Data Sources

- **History:** `~/.claude/history.jsonl`
- **Stats:** `~/.claude/stats-cache.json`
- **Profile:** `~/.claude/token-craft/user_profile.json`
- **Snapshots:** `~/.claude/token-craft/snapshots/`

### Requirements

- Python 3.8+ (standard library only)
- Claude Code installed
- Read access to `~/.claude/` directory
- Token-Craft repository cloned to the path above

---

## Skill vs Direct Execution

### Using the Skill (Recommended)
```
/token-craft
```

**Advantages:**
- ✅ Available from any project
- ✅ Natural language invocation
- ✅ Claude provides context and interpretation
- ✅ No need to remember paths
- ✅ Integrated with your workflow

### Direct Execution (Alternative)
```bash
cd C:\Users\Dmitriy_Zhorov\Documents\Personal\GenAI\token-analyzer
python skill_handler.py
```

**When to use:**
- Testing the tool directly
- Debugging issues
- Running without Claude Code
- Automation/scripting

---

## Troubleshooting

### Skill Not Found

**Check skill file exists:**
```bash
# Windows
dir "%USERPROFILE%\.claude\skills\token-craft\SKILL.md"

# macOS/Linux
ls ~/.claude/skills/token-craft/SKILL.md
```

**If missing:** Follow installation steps above.

### Python Not Found

**Verify Python installation:**
```bash
python --version
```

**If not installed:** Download from https://python.org

### Permission Denied

**Check file permissions:**
```bash
# Windows
icacls "%USERPROFILE%\.claude\history.jsonl"

# macOS/Linux
ls -la ~/.claude/history.jsonl
```

**Fix:** Ensure your user has read access.

### Skill Runs But Shows Error

**Check the Token-Craft directory exists:**
```bash
dir "C:\Users\Dmitriy_Zhorov\Documents\Personal\GenAI\token-analyzer"
```

**If wrong path:** Edit `SKILL.md` and update the `cd` command path.

### Claude Doesn't Auto-Invoke

**Try being more explicit:**
```
Run /token-craft to check my score
Show me my token efficiency using token-craft
```

**Or invoke directly:**
```
/token-craft
```

---

## Advanced: Custom Arguments

While the handler is fully interactive, you can hint at preferences:

```
/token-craft quick        # Suggest option [3] (one-line status)
/token-craft summary      # Suggest option [2] (quick summary)
/token-craft full         # Suggest option [1] (full report)
```

The skill will guide you to the appropriate menu choice.

---

## Team Distribution

To share this skill with your team:

### Option 1: Everyone Clones Repo
Each team member:
1. Clones the token-analyzer repo
2. Skill file is already in their `~/.claude/skills/token-craft/`
3. Done! ✅

### Option 2: Manual Skill Distribution
Share just the SKILL.md file:
1. Copy from `~/.claude/skills/token-craft/SKILL.md`
2. Share via Slack/email/etc.
3. Each person puts it in their `~/.claude/skills/token-craft/SKILL.md`
4. They each clone the main repo separately

### Option 3: Enterprise Distribution
If your org uses [managed settings](https://code.claude.com/docs/en/permissions#managed-settings):
1. Add skill to enterprise config
2. Auto-deployed to all users
3. Centrally managed updates

---

## Skill vs Plugin

**This is a SKILL, not a plugin.** Skills are simpler:

| Feature | Skill (token-craft) | Plugin |
|---------|---------------------|--------|
| File format | Markdown + YAML | Full package structure |
| Invocation | `/token-craft` | MCP integration |
| Distribution | Copy SKILL.md | Install package |
| Complexity | Simple | Complex |
| Our use case | ✅ Perfect fit | Overkill |

---

## Version History

### v1.1.0 (Current)
- ✅ 100/100 Anthropic alignment
- ✅ 8 best practices tracked
- ✅ Flexible pricing system
- ✅ Fully interactive (no parameters)
- ✅ Claude Skill integration

### v1.0.0
- ✅ Initial release
- ✅ 5 best practices tracked
- ✅ 95/100 Anthropic alignment

---

## Next Steps

1. **Verify installation:**
   ```
   What skills are available?
   ```

2. **Run your first check:**
   ```
   /token-craft
   ```

3. **Share with team:**
   - Send them this INSTALL guide
   - Have them clone the repo
   - Skill auto-available!

4. **Track progress:**
   - Run weekly to see trends
   - Apply recommendations
   - Watch your rank climb!

---

**Skill Location:** `~/.claude/skills/token-craft/SKILL.md`
**Main Repo:** `C:\Users\Dmitriy_Zhorov\Documents\Personal\GenAI\token-analyzer`
**Version:** 1.1.0
**Status:** ✅ Production Ready

---

*Master LLM efficiency through space exploration ranks!* 🚀
