#!/usr/bin/env python3
"""
Token usage analyzer for Claude Code sessions.
Categorizes conversations by task type and shows token breakdown.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# Category definitions with keywords
CATEGORIES = {
    'Git Operations': ['git', 'commit', 'push', 'pull', 'merge', 'branch', 'clone', 'rebase', 'checkout'],
    'File Operations': ['read', 'write', 'edit', 'file', 'directory', 'folder', 'create file', 'delete file'],
    'Code Writing': ['implement', 'add feature', 'create function', 'write code', 'develop', 'build'],
    'Debugging/Fixing': ['fix', 'bug', 'error', 'issue', 'debug', 'problem', 'not working', 'failing'],
    'Web Scraping/API': ['scrape', 'api', 'fetch', 'request', 'endpoint', 'curl', 'http'],
    'Search/Exploration': ['search', 'find', 'look for', 'explore', 'show me', 'list', 'where is'],
    'Refactoring': ['refactor', 'clean up', 'reorganize', 'restructure', 'optimize', 'improve code'],
    'Documentation': ['document', 'readme', 'comment', 'explain', 'describe'],
    'Configuration': ['config', 'setup', 'install', 'configure', 'settings'],
    'Data Analysis': ['analyze', 'parse', 'process data', 'calculate', 'statistics'],
    'Testing': ['test', 'pytest', 'unit test', 'integration test'],
}

def categorize_message(message_text):
    """Categorize a message based on keywords."""
    message_lower = message_text.lower()
    categories = []

    for category, keywords in CATEGORIES.items():
        if any(keyword in message_lower for keyword in keywords):
            categories.append(category)

    if not categories:
        categories.append('Other')

    return categories

def load_history(history_path):
    """Load and parse history.jsonl file with project info."""
    sessions = defaultdict(list)
    session_projects = {}  # Track which project each session belongs to

    with open(history_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if 'sessionId' in entry and 'display' in entry:
                    session_id = entry['sessionId']
                    sessions[session_id].append({
                        'message': entry['display'],
                        'timestamp': entry.get('timestamp', 0)
                    })
                    # Store project path for this session
                    if 'project' in entry and session_id not in session_projects:
                        session_projects[session_id] = entry['project']
            except json.JSONDecodeError:
                continue

    return sessions, session_projects

def load_stats(stats_path):
    """Load stats-cache.json file."""
    with open(stats_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def apply_optimizations(insights, project_stats):
    """Interactive questionnaire to apply optimizations."""
    print("\n" + "=" * 70)
    print("[*] OPTIMIZATION WIZARD")
    print("=" * 70)
    print("\nWould you like to apply optimizations automatically?")
    print("I can help you set up:")
    print("  - CLAUDE.md files with project preferences")
    print("  - Command cheat sheets")
    print("  - Workflow improvements")

    response = input("\nApply optimizations? (y/n): ").strip().lower()
    if response != 'y':
        print("\nSkipping optimizations. You can run this script again anytime!")
        return

    print("\n" + "=" * 70)
    print("SELECT OPTIMIZATIONS TO APPLY")
    print("=" * 70)

    available_optimizations = []

    # Option 1: Defer documentation
    if any(i['category'] == 'Documentation' for i in insights):
        available_optimizations.append({
            'id': 1,
            'name': 'Defer Documentation',
            'description': 'Add rule to CLAUDE.md: Skip README/comments until pushing to GitHub'
        })

    # Option 2: Configuration optimization
    if any(i['category'] == 'Configuration' for i in insights):
        available_optimizations.append({
            'id': 2,
            'name': 'Reduce Configuration Time',
            'description': 'Create CLAUDE.md template for your most-used projects'
        })

    # Option 3: Direct commands cheat sheet
    if any(i['category'] in ['Search/Exploration', 'File Operations'] for i in insights):
        available_optimizations.append({
            'id': 3,
            'name': 'Command Cheat Sheet',
            'description': 'Create a quick reference for common commands (git, grep, find, etc.)'
        })

    # Option 4: Concise mode preference
    if any(i['category'] == 'Verbosity' for i in insights):
        available_optimizations.append({
            'id': 4,
            'name': 'Concise Response Mode',
            'description': 'Add preference to CLAUDE.md: Keep responses brief unless asked'
        })

    # Display options
    print("\nAvailable optimizations:\n")
    for opt in available_optimizations:
        print(f"  [{opt['id']}] {opt['name']}")
        print(f"      {opt['description']}")
        print()

    print("Enter optimization numbers separated by spaces (e.g., '1 3 4')")
    print("Or press Enter to apply all, or 'n' to skip")

    choice = input("\nYour choice: ").strip()

    if choice.lower() == 'n':
        print("\nNo optimizations applied.")
        return

    # Parse choices
    if choice == '':
        selected = [opt['id'] for opt in available_optimizations]
    else:
        try:
            selected = [int(x) for x in choice.split()]
        except ValueError:
            print("\n[!] Invalid input. Skipping optimizations.")
            return

    # Apply selected optimizations
    print("\n" + "=" * 70)
    print("APPLYING OPTIMIZATIONS...")
    print("=" * 70)

    applied = []

    for opt_id in selected:
        opt = next((o for o in available_optimizations if o['id'] == opt_id), None)
        if not opt:
            continue

        print(f"\n[+] Applying: {opt['name']}")

        if opt_id == 1:  # Defer documentation
            create_claude_md_rule('defer_documentation', project_stats)
            applied.append(opt['name'])

        elif opt_id == 2:  # Configuration optimization
            create_claude_md_template(project_stats)
            applied.append(opt['name'])

        elif opt_id == 3:  # Command cheat sheet
            create_command_cheatsheet()
            applied.append(opt['name'])

        elif opt_id == 4:  # Concise mode
            create_claude_md_rule('concise_mode', project_stats)
            applied.append(opt['name'])

    # Summary
    print("\n" + "=" * 70)
    print("[*] OPTIMIZATION SUMMARY")
    print("=" * 70)
    if applied:
        print("\nSuccessfully applied:")
        for opt_name in applied:
            print(f"  - {opt_name}")
        print("\nCheck your project directories for new/updated files!")
    else:
        print("\nNo optimizations were applied.")
    print()

def create_claude_md_rule(rule_type, project_stats):
    """Create or update CLAUDE.md files with optimization rules."""
    rules = {
        'defer_documentation': '''
## Documentation Strategy
- DEFER documentation (README, comments) until code is ready to push to GitHub
- Focus on functionality first, document later
- Only add inline comments for complex logic that isn't self-evident
''',
        'concise_mode': '''
## Response Style
- Keep responses concise and focused by default
- Only provide detailed explanations when explicitly asked
- Use /fast mode for straightforward tasks
'''
    }

    rule_content = rules.get(rule_type, '')

    # Find top projects
    sorted_projects = sorted(project_stats.items(), key=lambda x: x[1]['sessions'], reverse=True)
    top_projects = [p for p, s in sorted_projects[:3] if p not in ['Unknown', '']]

    files_created = []

    for project_name in top_projects:
        # Try to find project path
        claude_dir = Path.home() / '.claude'
        history_path = claude_dir / 'history.jsonl'

        project_path = None
        with open(history_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if 'project' in entry and Path(entry['project']).name == project_name:
                        project_path = Path(entry['project'])
                        break
                except:
                    continue

        if not project_path or not project_path.exists():
            continue

        claude_md_path = project_path / 'CLAUDE.md'

        if claude_md_path.exists():
            # Append to existing
            with open(claude_md_path, 'a', encoding='utf-8') as f:
                f.write(rule_content)
            print(f"    Updated: {claude_md_path}")
        else:
            # Create new
            with open(claude_md_path, 'w', encoding='utf-8') as f:
                f.write(f"# Claude Code Configuration for {project_name}\n")
                f.write(rule_content)
            print(f"    Created: {claude_md_path}")

        files_created.append(str(claude_md_path))

    if not files_created:
        print(f"    Note: Could not find project paths. Create CLAUDE.md manually in your project root.")

def create_claude_md_template(project_stats):
    """Create a CLAUDE.md template file."""
    template_path = Path.home() / 'CLAUDE_TEMPLATE.md'

    template_content = '''# Claude Code Project Configuration Template

## Workflow Preferences
- Use direct commands when possible: git log, cat, grep, ls
- Keep responses concise unless detailed explanation needed
- Defer documentation until ready to push to GitHub

## Project-Specific Rules
[Add your project-specific preferences here]

## Code Style
[Add your coding standards here]

## Testing
[Add testing preferences here]

## Deployment
[Add deployment notes here]
'''

    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content)

    print(f"    Created template: {template_path}")
    print(f"    Copy this to your project roots as CLAUDE.md")

def create_command_cheatsheet():
    """Create a command reference cheat sheet."""
    cheatsheet_path = Path.home() / 'claude_commands_cheatsheet.txt'

    cheatsheet_content = '''# Claude Code - Command Cheat Sheet
Save tokens by running these commands directly instead of asking Claude!

## File Operations
  cat <file>              # View file contents
  head -20 <file>         # View first 20 lines
  tail -20 <file>         # View last 20 lines
  ls -la                  # List files with details
  tree                    # Show directory structure

## Git Operations
  git log --oneline -20   # View last 20 commits
  git status              # Check working tree status
  git diff                # View changes
  git branch -a           # List all branches

## Search Operations
  git grep "pattern"      # Search in git-tracked files
  grep -r "keyword" .     # Search all files recursively
  find . -name "*.py"     # Find files by pattern

## Code Navigation
  grep -n "function" *.py # Search with line numbers
  wc -l <file>            # Count lines in file

## Quick Analysis
  du -sh *                # Directory sizes
  ps aux | grep <name>    # Find running processes

Remember: Use Claude for complex reasoning, coding, and analysis.
Use these commands for simple information retrieval!
'''

    with open(cheatsheet_path, 'w', encoding='utf-8') as f:
        f.write(cheatsheet_content)

    print(f"    Created cheat sheet: {cheatsheet_path}")
    print(f"    Keep this handy for quick reference!")

def analyze_tokens():
    """Main analysis function."""
    # Paths
    claude_dir = Path.home() / '.claude'
    history_path = claude_dir / 'history.jsonl'
    stats_path = claude_dir / 'stats-cache.json'

    print("Loading conversation history...")
    sessions, session_projects = load_history(history_path)

    print("Loading token statistics...")
    stats = load_stats(stats_path)

    # Categorize sessions
    category_counts = defaultdict(int)
    category_sessions = defaultdict(list)
    project_stats = defaultdict(lambda: {'sessions': 0, 'messages': 0, 'categories': defaultdict(int)})

    print(f"\nAnalyzing {len(sessions)} sessions...\n")

    for session_id, messages in sessions.items():
        # Combine all messages in session for categorization
        all_messages = ' '.join([msg['message'] for msg in messages])
        categories = categorize_message(all_messages)

        # Get project for this session
        project_path = session_projects.get(session_id, 'Unknown')
        project_name = Path(project_path).name if project_path != 'Unknown' else 'Unknown'

        # Update project stats
        project_stats[project_name]['sessions'] += 1
        project_stats[project_name]['messages'] += len(messages)

        for category in categories:
            category_counts[category] += 1
            project_stats[project_name]['categories'][category] += 1
            category_sessions[category].append({
                'id': session_id[:8],
                'messages': len(messages),
                'sample': messages[0]['message'][:60] + '...' if messages else '',
                'project': project_name
            })

    # Print results
    print("=" * 70)
    print("TOKEN USAGE BREAKDOWN BY TASK TYPE")
    print("=" * 70)

    # Overall stats
    model_usage = stats.get('modelUsage', {})
    total_tokens = 0

    print("\n[*] OVERALL TOKEN USAGE:\n")
    for model, usage in model_usage.items():
        model_name = model.split('/')[-1]  # Clean up model name
        input_tokens = usage.get('inputTokens', 0)
        output_tokens = usage.get('outputTokens', 0)
        total = input_tokens + output_tokens
        total_tokens += total

        if total > 0:
            print(f"  {model_name}:")
            print(f"    Input:  {input_tokens:,} tokens")
            print(f"    Output: {output_tokens:,} tokens")
            print(f"    Total:  {total:,} tokens")
            print()

    print(f"[+] Total tokens used: {total_tokens:,}")

    # Activity stats
    print(f"\n[*] Activity Statistics:")
    print(f"  Total sessions: {stats.get('totalSessions', 0)}")
    print(f"  Total messages: {stats.get('totalMessages', 0)}")

    daily_activity = stats.get('dailyActivity', [])
    if daily_activity:
        last_day = daily_activity[-1]
        print(f"  Last active: {last_day.get('date')}")
        print(f"    Sessions: {last_day.get('sessionCount', 0)}")
        print(f"    Messages: {last_day.get('messageCount', 0)}")
        print(f"    Tool calls: {last_day.get('toolCallCount', 0)}")

    # Category breakdown
    print(f"\n[*] TASK CATEGORY BREAKDOWN:\n")
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

    for category, count in sorted_categories:
        percentage = (count / len(sessions)) * 100
        bar_length = int(percentage / 2)
        bar = '#' * bar_length + '-' * (50 - bar_length)

        print(f"  {category:20} {bar} {count:3} sessions ({percentage:.1f}%)")

    # Top sessions by category
    print(f"\n[*] SAMPLE SESSIONS BY CATEGORY:\n")
    for category, sessions_list in sorted(category_sessions.items()):
        if sessions_list:
            print(f"\n  {category}:")
            for session in sessions_list[:3]:  # Show top 3
                print(f"    - [{session['id']}] {session['messages']} msgs - [{session['project']}] {session['sample']}")

    # Project breakdown
    print("\n" + "=" * 70)
    print("[*] PROJECT BREAKDOWN:")
    print("=" * 70)

    sorted_projects = sorted(project_stats.items(), key=lambda x: x[1]['sessions'], reverse=True)

    for project_name, stats_data in sorted_projects:
        sessions_count = stats_data['sessions']
        messages_count = stats_data['messages']
        percentage = (sessions_count / len(sessions)) * 100

        print(f"\n  {project_name}")
        print(f"    Sessions: {sessions_count} ({percentage:.1f}%)")
        print(f"    Messages: {messages_count}")

        # Show top categories for this project
        if stats_data['categories']:
            top_categories = sorted(stats_data['categories'].items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"    Top tasks: {', '.join([f'{cat} ({cnt})' for cat, cnt in top_categories])}")

    # Token optimization insights
    print("\n" + "=" * 70)
    print("[*] TOKEN OPTIMIZATION INSIGHTS:")
    print("=" * 70)

    insights = []

    # Analyze documentation spending
    doc_percentage = (category_counts.get('Documentation', 0) / len(sessions)) * 100
    if doc_percentage > 15:
        insights.append({
            'category': 'Documentation',
            'impact': 'MEDIUM',
            'percentage': doc_percentage,
            'suggestion': 'Consider deferring documentation (README, comments) until ready to push to GitHub. Focus on code functionality first.'
        })

    # Analyze configuration spending
    config_percentage = (category_counts.get('Configuration', 0) / len(sessions)) * 100
    if config_percentage > 30:
        insights.append({
            'category': 'Configuration',
            'impact': 'HIGH',
            'percentage': config_percentage,
            'suggestion': 'High setup/config time. Consider: (1) Using CLAUDE.md for project rules, (2) Saving common configs as templates, (3) Using direct commands when possible.'
        })

    # Analyze search/exploration
    search_percentage = (category_counts.get('Search/Exploration', 0) / len(sessions)) * 100
    if search_percentage > 15:
        insights.append({
            'category': 'Search/Exploration',
            'impact': 'MEDIUM',
            'percentage': search_percentage,
            'suggestion': 'Use direct commands to save tokens: "git grep <pattern>", "find . -name <file>", "ls -R", "tree" instead of asking me.'
        })

    # Analyze file operations
    file_percentage = (category_counts.get('File Operations', 0) / len(sessions)) * 100
    if file_percentage > 30:
        insights.append({
            'category': 'File Operations',
            'impact': 'MEDIUM',
            'percentage': file_percentage,
            'suggestion': 'For simple file viewing: use "cat <file>", "head <file>", "tail <file>" directly. Reserve my help for complex edits.'
        })

    # Check output vs input ratio
    for model, usage in model_usage.items():
        if 'sonnet' in model.lower() or 'opus' in model.lower():
            input_tokens = usage.get('inputTokens', 0)
            output_tokens = usage.get('outputTokens', 0)
            if output_tokens > 0:
                ratio = output_tokens / input_tokens if input_tokens > 0 else 0
                if ratio > 8:
                    insights.append({
                        'category': 'Verbosity',
                        'impact': 'MEDIUM',
                        'percentage': 0,
                        'suggestion': f'Output/input ratio is {ratio:.1f}x. Consider asking for more concise responses or using /fast mode for quicker tasks.'
                    })

    # Print insights
    if insights:
        print("\n  Potential Optimizations:\n")
        for i, insight in enumerate(insights, 1):
            print(f"  [{insight['impact']}] {insight['category']}")
            if insight['percentage'] > 0:
                print(f"      Current: {insight['percentage']:.1f}% of sessions")
            print(f"      Tip: {insight['suggestion']}")
            print()
    else:
        print("\n  No major optimization opportunities detected. You're using tokens efficiently!\n")

    # General tips
    print("  General Tips:")
    print("  - Use MEMORY.md to teach me project patterns (auto-loaded every session)")
    print("  - Use CLAUDE.md for project-specific rules and preferences")
    print("  - Run simple commands yourself: git log, ls, cat, grep")
    print("  - Ask for concise responses when you don't need detailed explanations")
    print("  - Use /fast mode for quick, straightforward tasks")

    print("\n" + "=" * 70)

    # Run optimization wizard
    apply_optimizations(insights, project_stats)

    print("\n" + "=" * 70)
    print("\n[!] Note: Token usage is not tracked per-session by Claude Code,")
    print("   so this shows task distribution rather than exact token breakdown.")
    print("   Total token usage is accurate from stats-cache.json")
    print("=" * 70)

if __name__ == '__main__':
    try:
        analyze_tokens()
    except FileNotFoundError as e:
        print(f"[!] Error: Could not find file - {e}")
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
