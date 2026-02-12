#!/usr/bin/env python3
"""
Token usage analyzer for Claude Code sessions.
Categorizes conversations by task type and shows token breakdown.
"""

import json
import re
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
