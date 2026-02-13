# Token-Craft Enhancement Analysis

**Date:** February 12, 2026
**Version:** 2.0 Planning Document
**Status:** Research & Analysis Complete

---

## Executive Summary

Comprehensive analysis of Token-Craft enhancements covering scoring weights, team features, data storage, integration strategies, categories, benchmarks, cost tracking, and /insights integration.

**Key Finding:** `/insights` exists as Anthropic built-in - Token-Craft complements it perfectly with quantitative metrics vs qualitative analysis.

---

## 1. Current State Assessment

### What's Already Implemented ✅

**Cost Tracking (pricing_calculator.py)**
- ✅ Multi-deployment support (Direct API, AWS Bedrock, Google Vertex)
- ✅ Flexible pricing configuration (pricing_config.json)
- ✅ Per-session, monthly, and savings calculations
- ✅ Cache cost tracking (read/write)
- ✅ Deployment comparison features

**Team Features**
- ✅ Team exporter (team_exporter.py)
- ✅ Leaderboard generator (leaderboard_generator.py)
- ✅ Company-wide, project-level, and department leaderboards
- ✅ Anonymous/named mode for privacy
- ✅ Export/import for aggregation

**Data Storage**
- ✅ Location: `~/.claude/token-craft/`
- ✅ User profile: `user_profile.json`
- ✅ Snapshots: `snapshots/snapshot_YYYYMMDD_HHMMSS.json`
- ✅ Team exports: `team-exports/`
- ✅ Team stats: `team-stats/`

**Integration**
- ✅ Claude Skill architecture
- ✅ SKILL.md with trigger phrases
- ✅ Standalone skill at `~/.claude/skills/token-craft/`

---

## 2. /insights Integration Analysis ⭐ KEY FINDING

### What /insights Does (Anthropic Built-in)

**Discovered:** `/insights` is a built-in Anthropic feature that provides:

```
/insights Output:
├── At a Glance (session summary)
├── Project Areas (what you work on)
├── Interaction Style (how you communicate)
├── What Works (successes)
├── Friction Analysis (pain points)
├── Suggestions (behavioral improvements)
├── On the Horizon (future opportunities)
└── Fun Ending (personality touch)

Format: HTML report (file:///.../ report.html)
Focus: Qualitative, behavioral, workflow analysis
```

### Token-Craft's Complementary Role

**Token-Craft provides what /insights doesn't:**

```
Token-Craft Output:
├── Token Efficiency Score (quantitative)
├── Cost Tracking ($ per session, monthly)
├── Rank & Achievements (gamification)
├── Team Leaderboards (social comparison)
├── Optimization Adoption (8 best practices)
├── Cache Effectiveness (90%+ savings)
├── Tool Usage Efficiency (parallel calls)
├── Session Focus (message count)
└── Real-Time Alerts (budget limits)

Format: Terminal + HTML reports
Focus: Quantitative, metrics, optimization, costs
```

### Perfect Complement - Zero Overlap

| Aspect | /insights | Token-Craft |
|--------|-----------|-------------|
| **Analysis Type** | Qualitative | Quantitative |
| **Focus** | Behavior & workflow | Efficiency & costs |
| **Metrics** | Narrative descriptions | Numbers, scores, ranks |
| **Goal** | Improve how you work | Reduce tokens & costs |
| **Social** | Individual only | Team leaderboards |
| **Gamification** | None | Ranks, achievements |
| **Cost Visibility** | None | Real-time $ tracking |
| **Optimization** | Suggestions | Scored best practices |
| **Format** | HTML report | Terminal + HTML + email |
| **Frequency** | On-demand | Daily/weekly/monthly |

**Conclusion:** No need for "token-insights" skill - Token-Craft already has unique value proposition!

---

## 3. Scoring Weights & Thresholds Analysis

### Current Scoring System (1000 points total)

```
Token Efficiency:        300 pts (30%)
Optimization Adoption:   325 pts (32.5%)
Self-Sufficiency:        200 pts (20%)
Improvement Trend:       125 pts (12.5%)
Best Practices:          50 pts (5%)
```

### Current Baseline (DEFAULT_BASELINE in scoring_engine.py)

```python
{
    "tokens_per_session": 15000,
    "tokens_per_message": 1500,
    "self_sufficiency_rate": 0.40,
    "optimization_adoption_rate": 0.30
}
```

### Issues with Current Thresholds

**Problem 1: Token Efficiency Baseline Too Low**
- Current baseline: 15,000 tokens/session
- Real user (you): 33,762 tokens/session (2.25x baseline)
- Result: 0/300 points (harsh penalty)

**Observation:** The baseline assumes very short sessions. Real coding sessions with Claude Code are longer and more complex.

**Problem 2: Binary Scoring for Optimizations**
- Current: 80%+ adoption = full points, <20% = 0 points
- Issue: No granularity in 20-80% range
- Result: Hard to see incremental improvement

**Problem 3: Improvement Trend Weight**
- Currently 12.5% of total score
- Requires historical data (unfair to new users)
- Most users get 20/125 points (16%) = "maintaining" status

### Recommended Changes

**Immediate Improvements:**
1. Add dynamic baseline calculation from user's own history
2. Implement sliding scale for 20-80% adoption range
3. Add "warm-up period" for new users (first 10 sessions)
4. Separate baselines by session type (coding, research, writing)

**Details:** See `RECOMMENDED_BENCHMARKS.md`

---

## 4. Additional Categories to Track

### Currently Tracked (5 categories)

1. Token Efficiency
2. Optimization Adoption (8 sub-metrics)
3. Self-Sufficiency
4. Improvement Trend
5. Best Practices

### Proposed New Categories

#### 6. Cache Effectiveness (100 pts)
**Why:** Prompt caching reduces costs by 90% (cache reads)

**Metrics:**
- Cache hit rate (% of tokens from cache)
- Cache write efficiency (reusable context)
- Cost savings from caching

**Data Source:** `stats-cache.json` already tracks:
```json
"cacheReadInputTokens": 172132166,
"cacheCreationInputTokens": 59290310
```

**Scoring:**
- 90%+ cache hit rate = 100 pts
- 70-89% = 75 pts
- 50-69% = 50 pts
- 30-49% = 25 pts
- <30% = 0 pts

#### 7. Tool Usage Efficiency (75 pts)
**Why:** Efficient tool calls reduce tokens

**Metrics:**
- Read before Edit compliance (never edit without reading)
- Parallel tool calls (batch independent operations)
- Tool call success rate (no retries)
- Glob/Grep usage (vs asking AI to search)

**Data Source:** `history.jsonl` tracks all tool calls

**Scoring:**
- Parallel tool usage: 30 pts
- Read-before-edit: 25 pts
- Search tools usage: 20 pts

#### 8. Session Focus (50 pts)
**Why:** Focused sessions are more efficient

**Metrics:**
- Average messages per session (sweet spot: 5-15)
- Topic coherence (no context switching)
- Task completion rate

**Scoring:**
- 5-15 messages/session = 50 pts
- 3-5 or 15-20 = 30 pts
- <3 or >20 = 10 pts

#### 9. Cost Consciousness (75 pts)
**Why:** Direct financial impact

**Metrics:**
- Cost per task completion
- Model selection appropriateness (Haiku for simple, Opus for complex)
- Cost trend over time

**Scoring:**
- <$0.50/session avg = 75 pts
- $0.50-$1.00 = 50 pts
- $1.00-$2.00 = 25 pts
- >$2.00 = 0 pts

#### 10. Autonomy & Learning (50 pts)
**Why:** Encourages skill development

**Metrics:**
- Direct command usage growth over time
- Repeated mistake avoidance
- Growing independence

**Scoring:**
- Growing autonomy = 50 pts
- Stable = 25 pts
- Declining = 0 pts

### New Total: 1350 points (from 1000)

**Revised Ranks:**
- 0-269: 🎓 Cadet
- 270-539: ✈️ Pilot
- 540-809: 🧭 Navigator
- 810-1079: ⭐ Commander
- 1080-1349: 👨‍✈️ Captain
- 1350-1619: 🎖️ Admiral
- 1620+: 🌌 Galactic Legend

---

## 5. Team Features Architecture

### Current Implementation

**Exports:** Individual user stats to `team-exports/`
**Aggregation:** Reads from `team-stats/` directory
**Leaderboards:** Company, project, department levels

### Decisions Made: Git Repository + Free Services

**Primary Method: Git Repository (GitHub)**

```
company-token-craft-stats/  (GitHub private repo)
├── team-stats/
│   ├── user1@company_20260212.json
│   ├── user2@company_20260212.json
│   └── userN@company_20260212.json
├── leaderboards/
│   ├── company_latest.json
│   ├── company_weekly.json
│   └── company_monthly.json
├── benchmarks/
│   └── company_baseline.json
└── .github/workflows/
    └── generate-leaderboard.yml  # Auto-generate on push
```

**Benefits:**
- Free (GitHub)
- Version control (full audit trail)
- Easy setup (2-3 hours)
- CI/CD integration
- Familiar to developers

**Implementation:**
```bash
# Setup
gh repo create company-token-craft-stats --private
git clone git@github.com:company/token-craft-stats.git

# Configure Token-Craft
{
  "team_settings": {
    "enabled": true,
    "method": "git",
    "repo_path": "/path/to/token-craft-stats",
    "auto_push": true
  }
}
```

### Phase 2: Cloud Storage (Optional)

**Free Options:**
- AWS S3 Free Tier: 5GB for 12 months
- Cloudflare R2: 10GB free forever (recommended)
- Azure Blob: 5GB free for 12 months

**Use Case:** Scale beyond Git, faster real-time access

### Phase 3: Notifications (Optional)

**Email: SendGrid or Resend (Free)**
- SendGrid: 100 emails/day free
- Resend: 3,000 emails/month free
- Use for: Weekly digests, monthly reports

**Windows Toast Notifications**
- Library: win10toast (free)
- Use for: Real-time cost alerts

---

## 6. Data Storage Best Practices

### Current Structure (Aligned with Claude Skills Standards)

```
~/.claude/token-craft/
├── user_profile.json              # Current state
├── snapshots/                     # Historical data
│   └── snapshot_YYYYMMDD_HHMMSS.json
├── team-exports/                  # Individual exports
├── team-stats/                    # Aggregated team data
├── cache/                         # NEW: Speed optimization
└── exports/                       # NEW: User reports (HTML, CSV)
```

### Recommended Additions

#### cache/ directory
**Purpose:** Speed up repeated calculations

**Files:**
- `score_cache.json` - Last calculated scores (TTL: 1 hour)
- `leaderboard_cache.json` - Last fetched leaderboard
- `benchmark_cache.json` - Industry benchmarks (TTL: 24 hours)

#### exports/ directory
**Purpose:** User-requested exports

**Files:**
- `report_YYYYMMDD.html` - HTML report (web links)
- `report_YYYYMMDD.csv` - CSV export for Excel
- `monthly_YYYYMM.html` - Monthly review

### Data Retention Policy

**Snapshots:** Keep last 30, then monthly for 1 year
**Exports:** Auto-delete after 30 days
**Cache:** Auto-delete after TTL
**Profile:** Keep forever (migrate on schema changes)

### Schema Versioning

**Add to all JSON files:**
```json
{
  "schema_version": "2.0.0",
  "data": { ... }
}
```

---

## 7. Integration Strategy: Standalone Skill

### Current: Standalone Skill (Keep It!)

**Location:** `~/.claude/skills/token-craft/SKILL.md`

**Why Keep Standalone:**
- ✅ Simple to install
- ✅ No dependencies
- ✅ Complements /insights perfectly
- ✅ Unique value proposition (quantitative metrics)
- ✅ Team features built-in
- ✅ No need for additional skills

**Decision:** No new skills needed - Token-Craft is complete as-is!

### Focus Token-Craft On Its Strengths

**What Token-Craft Does Best:**
1. Quantitative metrics (tokens, costs, efficiency)
2. Gamification (ranks, achievements, competition)
3. Team leaderboards (social aspect)
4. Cost tracking (real financial impact)
5. Optimization scoring (8 best practices)
6. Automated reporting (daily/weekly/monthly)

**What /insights Does Best:**
1. Qualitative analysis (behavioral patterns)
2. Project focus identification
3. Friction detection
4. Workflow suggestions
5. Interaction style analysis

**Together = Complete Picture!**

---

## 8. Industry Benchmarks Strategy

### Approach: Community-Driven Benchmarks

**Phase 1:** Use real user data + estimates
```
Coding sessions:      25-35K tokens (avg)
Research sessions:    10-20K tokens
Cost per session:     $0.30-$0.50 (Sonnet 4.5)
Cache hit rate:       70-90% (good)
Messages per session: 5-15 (focused)
```

**Phase 2:** Opt-in data collection
```
[Optional] Help improve Token-Craft benchmarks?
□ Yes, share anonymized stats
□ No, keep local only

Benefits:
- Real industry percentiles (P50, P75, P90, P95)
- Better recommendations
- Community-driven improvements
```

**Data to Collect (Anonymized):**
- Tokens per session (by use case)
- Cost per session (by model)
- Cache hit rates
- Session lengths
- Optimization adoption rates

**Privacy:** All data anonymized, opt-in only, user controls

---

## 9. Cost Tracking Enhancements

### Current Implementation ✅

**PricingCalculator class supports:**
- Per-session cost
- Monthly cost estimates
- Savings calculations
- Deployment comparisons
- Cache cost tracking

### Proposed Enhancements

#### 1. Real-Time Cost Tracking

**Integration Point:** Add to reports

**Implementation:**
```python
# In skill_handler.py
from token_craft.pricing_calculator import PricingCalculator

def calculate_session_cost(session_data):
    """Calculate real-time cost for session."""
    calc = PricingCalculator()

    model = session_data.get("model", "claude-sonnet-4-5")
    deployment = "direct_api"  # Or from user config

    cost = calc.calculate_cost(
        input_tokens=session_data["input_tokens"],
        output_tokens=session_data["output_tokens"],
        model=model,
        deployment=deployment,
        use_cache=session_data.get("cache_reads", 0) > 0,
        cache_read_tokens=session_data.get("cache_reads", 0)
    )

    return cost
```

#### 2. Cost Alerts (Multi-Channel)

**Terminal Alerts:**
```python
if daily_cost > daily_budget * 0.8:
    print("⚠️  Alert: 80% of daily budget used")
    print(f"   Current: ${daily_cost:.2f} / ${daily_budget:.2f}")
```

**Email Alerts (SendGrid):**
```python
import sendgrid
from sendgrid.helpers.mail import Mail

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

message = Mail(
    from_email='token-craft@company.com',
    to_emails='user@company.com',
    subject='Token-Craft: Budget Alert',
    html_content=f'<p>Daily budget 80% used: ${daily_cost:.2f}</p>'
)

sg.send(message)
```

**Windows Toast:**
```python
from win10toast import ToastNotifier

toaster = ToastNotifier()
toaster.show_toast(
    "Token-Craft Alert",
    f"80% of daily budget used (${daily_cost:.2f})",
    duration=10
)
```

#### 3. Cost Trends Dashboard

**Add to reports:**
```
Cost Analysis (Last 30 Days):
────────────────────────────────────────
Total Spent:        $47.32
Daily Average:      $1.58
Most Expensive Day: $4.23 (Feb 8)
Trend:              ↓ -12% vs previous month

By Model:
  Sonnet 4.5:  $42.10 (89%)
  Haiku 4.5:   $4.12 (9%)
  Opus 4.6:    $1.10 (2%)

Optimization Savings: $8.45 (15% reduction)
```

---

## 10. Implementation Roadmap

### Week 1: Core Fixes + Git Setup
**Priority: Fix Scoring + Team Infrastructure**

- [ ] Implement dynamic baseline (scoring_engine.py)
- [ ] Add smooth sliding scale for adoption
- [ ] Add warm-up period for new users
- [ ] Set up GitHub repository for team stats
- [ ] Implement Git auto-push for team exports
- [ ] Add terminal cost alerts
- [ ] Test with real user data

**Expected Outcome:** Score 495 → ~800, Git team features live

### Week 2: New Categories
**Priority: Add 5 New Metrics**

- [ ] Cache effectiveness tracking
- [ ] Tool usage efficiency
- [ ] Session focus scoring
- [ ] Cost efficiency tracking
- [ ] Learning & growth metrics
- [ ] Update rank thresholds (1000 → 1350 pts)
- [ ] Add daily terminal reports

**Expected Outcome:** Score ~800 → 1035 (Captain!), richer analytics

### Week 3: Multi-Channel & Reports
**Priority: Notifications & Rich Reports**

- [ ] SendGrid email integration (free tier)
- [ ] Windows toast notifications
- [ ] Weekly email digest
- [ ] HTML report generation (web links)
- [ ] Project-level tracking
- [ ] AWS S3 or Cloudflare R2 (optional, free tier)

**Expected Outcome:** Full notification system, professional reports

### Week 4: Polish & Launch
**Priority: v2.0 Release**

- [ ] Monthly review reports (HTML)
- [ ] Documentation updates (README, CLAUDE.md)
- [ ] Migration script for v1.0 users
- [ ] Changelog & v2.0 announcement
- [ ] GitHub release tag
- [ ] Collect feedback
- [ ] Plan v2.1 features

**Expected Outcome:** Production-ready v2.0, user feedback collected

---

## 11. Technology Stack (All Free!)

### Core (No Changes)
- Python 3.8+ (standard library only)
- JSON for data storage
- Existing Token-Craft modules

### New Dependencies (Optional)
```python
# requirements-optional.txt
sendgrid==6.9.7           # Email (100/day free)
# OR
resend==0.5.0             # Email alternative (3K/month free)

win10toast==0.9           # Windows notifications
boto3==1.26.0             # AWS S3 (if using)
```

### Services (Free Tiers)
- GitHub: Unlimited private repos (free)
- SendGrid: 100 emails/day (free)
- Resend: 3,000 emails/month (free)
- AWS S3: 5GB for 12 months (free)
- Cloudflare R2: 10GB forever (free)

**Total Monthly Cost: $0**

---

## 12. Summary & Next Steps

### What's Already Great ✅

1. **Cost tracking** - Comprehensive pricing calculator
2. **Team features** - Leaderboards, exports, department tracking
3. **Data storage** - Clean architecture following Claude Skills best practices
4. **Integration** - Proper skill structure
5. **Complementary to /insights** - Zero overlap, perfect complement

### What Needs Enhancement 🔧

1. **Scoring thresholds** - Dynamic baseline, smooth scale
2. **Additional categories** - Cache, tools, session focus, cost, autonomy
3. **Team aggregation** - Git repository (GitHub)
4. **Notifications** - Email, Windows toast, multi-channel
5. **Reports** - Daily/weekly/monthly, HTML + web links

### Decisions Made ✅

- Team aggregation: GitHub (free)
- Privacy: Named leaderboards
- Cost alerts: All channels (terminal, email, toast)
- Reports: All frequencies (daily, weekly, monthly)
- Email: SendGrid or Resend (free tiers)
- Cloud storage: Cloudflare R2 (free forever) or AWS S3
- Report delivery: Web links (not attachments)

### Immediate Next Steps

1. Review this analysis
2. Start Phase 1 implementation (Week 1)
3. Set up GitHub repository
4. Implement dynamic baseline
5. Test with real data

---

## 13. /insights + Token-Craft: Perfect Team

**Use Both Together:**

**Morning Routine:**
```bash
/token-craft              # Check efficiency, costs, rank
/insights                 # Understand workflow patterns
```

**Weekly Review:**
```bash
/token-craft              # Weekly digest (email)
/insights                 # Behavioral analysis
```

**Monthly Planning:**
```bash
/token-craft              # Monthly cost review, optimization ROI
/insights                 # Long-term patterns, strategic improvements
```

**Result:** Complete visibility into both quantitative efficiency and qualitative workflow!

---

**End of Analysis**

**Status:** Ready for Implementation
**Timeline:** 4 weeks to v2.0
**Cost:** $0/month (all free services)
**Your Benefit:** 495 → 1035 pts, Captain rank, team features, cost savings

---

**Questions? Ready to start?**
