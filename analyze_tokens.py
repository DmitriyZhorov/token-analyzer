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
    """Load and parse history.jsonl file."""
    sessions = defaultdict(list)

    with open(history_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if 'sessionId' in entry and 'display' in entry:
                    sessions[entry['sessionId']].append({
                        'message': entry['display'],
                        'timestamp': entry.get('timestamp', 0)
                    })
            except json.JSONDecodeError:
                continue

    return sessions

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
    sessions = load_history(history_path)

    print("Loading token statistics...")
    stats = load_stats(stats_path)

    # Categorize sessions
    category_counts = defaultdict(int)
    category_sessions = defaultdict(list)

    print(f"\nAnalyzing {len(sessions)} sessions...\n")

    for session_id, messages in sessions.items():
        # Combine all messages in session for categorization
        all_messages = ' '.join([msg['message'] for msg in messages])
        categories = categorize_message(all_messages)

        for category in categories:
            category_counts[category] += 1
            category_sessions[category].append({
                'id': session_id[:8],
                'messages': len(messages),
                'sample': messages[0]['message'][:60] + '...' if messages else ''
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
                print(f"    - [{session['id']}] {session['messages']} msgs - {session['sample']}")

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
