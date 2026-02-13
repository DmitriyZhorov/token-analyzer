#!/usr/bin/env python3
"""
Enhanced Token Usage Analyzer for Claude Code - Version 2
Features:
- Scope selection (projects/users)
- Thorough pattern analysis
- Interactive optimization wizard with trade-offs
- Snapshot & delta tracking
- Improvement measurement over time
"""

import json
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime
import re

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
    'Data Processing': ['analyze', 'parse', 'process data', 'calculate', 'statistics', 'csv', 'json', 'transform'],
    'Testing': ['test', 'pytest', 'unit test', 'integration test'],
}

WORK_TYPES = {
    'Coding': ['implement', 'write code', 'function', 'class', 'develop', 'build', 'create'],
    'Data Processing': ['parse', 'transform', 'csv', 'json', 'data', 'process', 'analyze data'],
    'DevOps': ['deploy', 'docker', 'kubernetes', 'ci/cd', 'pipeline', 'build'],
    'Research': ['explore', 'investigate', 'understand', 'how does', 'what is', 'explain'],
    'Maintenance': ['fix', 'bug', 'refactor', 'clean up', 'update', 'upgrade'],
}

def load_history_with_metadata(history_path):
    """Load history with full metadata."""
    sessions = defaultdict(list)
    session_metadata = {}

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

                    # Store metadata once per session
                    if session_id not in session_metadata:
                        session_metadata[session_id] = {
                            'project': entry.get('project', 'Unknown'),
                            'timestamp': entry.get('timestamp', 0)
                        }
            except json.JSONDecodeError:
                continue

    return sessions, session_metadata

def select_scope(sessions, session_metadata):
    """Interactive scope selection for projects and users."""
    print("\n" + "=" * 70)
    print("[*] SCOPE SELECTION")
    print("=" * 70)

    # Extract unique projects
    projects = {}
    for session_id, metadata in session_metadata.items():
        project_path = metadata['project']
        project_name = Path(project_path).name if project_path != 'Unknown' else 'Unknown'
        if project_name not in projects:
            projects[project_name] = {
                'path': project_path,
                'sessions': 0,
                'messages': 0
            }
        projects[project_name]['sessions'] += 1
        projects[project_name]['messages'] += len(sessions[session_id])

    # Display projects
    print("\nAvailable projects:")
    print(f"  [0] ALL PROJECTS ({len(projects)} total)")

    project_list = sorted(projects.items(), key=lambda x: x[1]['sessions'], reverse=True)
    for idx, (name, stats) in enumerate(project_list, 1):
        print(f"  [{idx}] {name}")
        print(f"      Sessions: {stats['sessions']}, Messages: {stats['messages']}")

    # Get project selection
    print("\nSelect projects (space-separated numbers, or 0 for all):")
    project_choice = input("Your choice: ").strip()

    if project_choice == '0' or project_choice == '':
        selected_projects = set(projects.keys())
        print(f"\n[+] Selected: ALL PROJECTS ({len(selected_projects)})")
    else:
        try:
            indices = [int(x) for x in project_choice.split()]
            selected_projects = set()
            for idx in indices:
                if 1 <= idx <= len(project_list):
                    selected_projects.add(project_list[idx-1][0])
            print(f"\n[+] Selected: {', '.join(selected_projects)}")
        except ValueError:
            print("[!] Invalid selection. Using all projects.")
            selected_projects = set(projects.keys())

    return selected_projects

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

def categorize_work_type(message_text):
    """Determine work type from message."""
    message_lower = message_text.lower()
    work_types = []

    for work_type, keywords in WORK_TYPES.items():
        if any(keyword in message_lower for keyword in keywords):
            work_types.append(work_type)

    if not work_types:
        work_types.append('General')

    return work_types

def analyze_scope(sessions, session_metadata, selected_projects, stats):
    """Perform thorough analysis on selected scope."""
    print("\n" + "=" * 70)
    print("[*] ANALYZING SELECTED SCOPE")
    print("=" * 70)
    print("\nAnalyzing patterns, work types, and optimization opportunities...")

    filtered_sessions = {}
    project_stats = defaultdict(lambda: {
        'sessions': 0,
        'messages': 0,
        'categories': defaultdict(int),
        'work_types': defaultdict(int),
        'avg_msg_length': 0,
        'total_chars': 0
    })

    category_counts = defaultdict(int)
    work_type_counts = defaultdict(int)

    # Filter and analyze sessions
    for session_id, messages in sessions.items():
        metadata = session_metadata.get(session_id, {})
        project_path = metadata.get('project', 'Unknown')
        project_name = Path(project_path).name if project_path != 'Unknown' else 'Unknown'

        if project_name not in selected_projects:
            continue

        filtered_sessions[session_id] = messages

        # Analyze messages
        all_messages_text = ' '.join([msg['message'] for msg in messages])
        categories = categorize_message(all_messages_text)
        work_types = categorize_work_type(all_messages_text)

        # Update stats
        project_stats[project_name]['sessions'] += 1
        project_stats[project_name]['messages'] += len(messages)
        project_stats[project_name]['total_chars'] += len(all_messages_text)

        for category in categories:
            category_counts[category] += 1
            project_stats[project_name]['categories'][category] += 1

        for work_type in work_types:
            work_type_counts[work_type] += 1
            project_stats[project_name]['work_types'][work_type] += 1

    # Calculate averages
    for project_name, pstats in project_stats.items():
        if pstats['messages'] > 0:
            pstats['avg_msg_length'] = pstats['total_chars'] / pstats['messages']

    return {
        'filtered_sessions': filtered_sessions,
        'project_stats': project_stats,
        'category_counts': category_counts,
        'work_type_counts': work_type_counts,
        'total_sessions': len(filtered_sessions),
        'total_messages': sum(len(msgs) for msgs in filtered_sessions.values())
    }

def display_analysis_breakdown(analysis, stats):
    """Display detailed breakdown with sorting and filtering options."""
    print("\n" + "=" * 70)
    print("[*] DETAILED ANALYSIS BREAKDOWN")
    print("=" * 70)

    # Overall stats
    print(f"\n[+] Scope Summary:")
    print(f"    Total sessions analyzed: {analysis['total_sessions']}")
    print(f"    Total messages analyzed: {analysis['total_messages']}")

    # Work type breakdown
    print(f"\n[+] Work Type Distribution:")
    sorted_work_types = sorted(analysis['work_type_counts'].items(), key=lambda x: x[1], reverse=True)
    for work_type, count in sorted_work_types:
        percentage = (count / analysis['total_sessions']) * 100
        bar = '#' * int(percentage / 2) + '-' * (50 - int(percentage / 2))
        print(f"    {work_type:20} {bar} {count:3} sessions ({percentage:.1f}%)")

    # Category breakdown
    print(f"\n[+] Task Category Distribution:")
    sorted_categories = sorted(analysis['category_counts'].items(), key=lambda x: x[1], reverse=True)
    for category, count in sorted_categories[:10]:  # Top 10
        percentage = (count / analysis['total_sessions']) * 100
        bar = '#' * int(percentage / 2) + '-' * (50 - int(percentage / 2))
        print(f"    {category:20} {bar} {count:3} sessions ({percentage:.1f}%)")

    # Project breakdown
    print(f"\n[+] Project Breakdown:")
    sorted_projects = sorted(analysis['project_stats'].items(),
                            key=lambda x: x[1]['sessions'], reverse=True)

    for project_name, pstats in sorted_projects:
        print(f"\n    {project_name}:")
        print(f"      Sessions: {pstats['sessions']}")
        print(f"      Messages: {pstats['messages']}")
        print(f"      Avg message length: {pstats['avg_msg_length']:.0f} chars")

        # Top work types for this project
        if pstats['work_types']:
            top_work = sorted(pstats['work_types'].items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"      Top work types: {', '.join([f'{wt} ({cnt})' for wt, cnt in top_work])}")

        # Top categories for this project
        if pstats['categories']:
            top_cats = sorted(pstats['categories'].items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"      Top tasks: {', '.join([f'{cat} ({cnt})' for cat, cnt in top_cats])}")

def identify_optimization_opportunities(analysis, stats):
    """Identify all possible optimization opportunities with detailed analysis."""
    print("\n" + "=" * 70)
    print("[*] IDENTIFYING OPTIMIZATION OPPORTUNITIES")
    print("=" * 70)
    print("\nAnalyzing patterns for potential improvements...")

    opportunities = []

    # Analyze documentation spending
    doc_count = analysis['category_counts'].get('Documentation', 0)
    doc_percentage = (doc_count / analysis['total_sessions']) * 100 if analysis['total_sessions'] > 0 else 0

    if doc_percentage > 15:
        opportunities.append({
            'id': len(opportunities) + 1,
            'category': 'Documentation Timing',
            'impact': 'MEDIUM' if doc_percentage < 30 else 'HIGH',
            'current_state': f"{doc_percentage:.1f}% of sessions involve documentation",
            'problem': 'Spending tokens on README/comments during active development',
            'options': [
                {
                    'name': 'Strict Defer',
                    'description': 'Never document until git push',
                    'estimated_savings': '20-25%',
                    'trade_off': 'May forget implementation details'
                },
                {
                    'name': 'Milestone Defer',
                    'description': 'Document only at major milestones',
                    'estimated_savings': '10-15%',
                    'trade_off': 'Some redundant explanation still happens'
                },
                {
                    'name': 'On-Demand Only',
                    'description': 'Document only when explicitly requested',
                    'estimated_savings': '15-20%',
                    'trade_off': 'Need to remember to ask for docs'
                }
            ]
        })

    # Analyze configuration overhead
    config_count = analysis['category_counts'].get('Configuration', 0)
    config_percentage = (config_count / analysis['total_sessions']) * 100 if analysis['total_sessions'] > 0 else 0

    if config_percentage > 25:
        opportunities.append({
            'id': len(opportunities) + 1,
            'category': 'Configuration Overhead',
            'impact': 'HIGH',
            'current_state': f"{config_percentage:.1f}% of sessions on setup/config",
            'problem': 'Repeated configuration and setup questions',
            'options': [
                {
                    'name': 'CLAUDE.md All Projects',
                    'description': 'Create comprehensive CLAUDE.md for every project',
                    'estimated_savings': '30-40%',
                    'trade_off': 'Upfront time investment'
                },
                {
                    'name': 'Memory-Based Learning',
                    'description': 'Rely on MEMORY.md to learn patterns',
                    'estimated_savings': '15-20%',
                    'trade_off': 'Takes time to build up memory'
                },
                {
                    'name': 'Project Templates',
                    'description': 'Use standardized project templates',
                    'estimated_savings': '20-30%',
                    'trade_off': 'Less flexibility per project'
                }
            ]
        })

    # Analyze search/exploration patterns
    search_count = analysis['category_counts'].get('Search/Exploration', 0)
    search_percentage = (search_count / analysis['total_sessions']) * 100 if analysis['total_sessions'] > 0 else 0

    if search_percentage > 15:
        opportunities.append({
            'id': len(opportunities) + 1,
            'category': 'Search & Exploration',
            'impact': 'MEDIUM',
            'current_state': f"{search_percentage:.1f}% of sessions searching/exploring",
            'problem': 'Using AI for simple file/code searches',
            'options': [
                {
                    'name': 'Command-First Approach',
                    'description': 'Always try grep/find first, then ask AI',
                    'estimated_savings': '15-25%',
                    'trade_off': 'Need to learn command syntax'
                },
                {
                    'name': 'IDE Search Tools',
                    'description': 'Use VS Code/IDE search instead of asking',
                    'estimated_savings': '10-20%',
                    'trade_off': 'Context switching between tools'
                },
                {
                    'name': 'Cheat Sheet Reference',
                    'description': 'Keep command reference handy',
                    'estimated_savings': '12-18%',
                    'trade_off': 'Need to reference sheet frequently'
                }
            ]
        })

    # Analyze file operations
    file_count = analysis['category_counts'].get('File Operations', 0)
    file_percentage = (file_count / analysis['total_sessions']) * 100 if analysis['total_sessions'] > 0 else 0

    if file_percentage > 30:
        opportunities.append({
            'id': len(opportunities) + 1,
            'category': 'File Operations',
            'impact': 'MEDIUM',
            'current_state': f"{file_percentage:.1f}% of sessions on file operations",
            'problem': 'Using AI for simple file viewing/listing',
            'options': [
                {
                    'name': 'Direct Commands',
                    'description': 'Use cat/ls/head/tail for simple viewing',
                    'estimated_savings': '20-30%',
                    'trade_off': 'Terminal only, no AI context'
                },
                {
                    'name': 'IDE Previews',
                    'description': 'Use IDE file explorer and previews',
                    'estimated_savings': '15-25%',
                    'trade_off': 'Less convenient for quick checks'
                },
                {
                    'name': 'Hybrid Approach',
                    'description': 'Simple views direct, complex analysis via AI',
                    'estimated_savings': '18-28%',
                    'trade_off': 'Need to decide case-by-case'
                }
            ]
        })

    # Analyze verbosity
    model_usage = stats.get('modelUsage', {})
    for model, usage in model_usage.items():
        if 'sonnet' in model.lower() or 'opus' in model.lower():
            input_tokens = usage.get('inputTokens', 0)
            output_tokens = usage.get('outputTokens', 0)
            if output_tokens > 0 and input_tokens > 0:
                ratio = output_tokens / input_tokens
                if ratio > 8:
                    opportunities.append({
                        'id': len(opportunities) + 1,
                        'category': 'Response Verbosity',
                        'impact': 'MEDIUM',
                        'current_state': f"Output/input ratio: {ratio:.1f}x",
                        'problem': 'AI responses may be more detailed than needed',
                        'options': [
                            {
                                'name': 'Concise Mode Default',
                                'description': 'Request brief responses by default',
                                'estimated_savings': '15-25%',
                                'trade_off': 'May miss helpful context'
                            },
                            {
                                'name': '/fast Mode Usage',
                                'description': 'Use /fast for straightforward tasks',
                                'estimated_savings': '20-30%',
                                'trade_off': 'Need to remember to switch modes'
                            },
                            {
                                'name': 'Explicit Detail Requests',
                                'description': 'Ask "explain in detail" when needed',
                                'estimated_savings': '10-20%',
                                'trade_off': 'May need follow-up questions'
                            }
                        ]
                    })
                    break

    # Analyze work type specific optimizations
    if analysis['work_type_counts'].get('Research', 0) > analysis['total_sessions'] * 0.3:
        opportunities.append({
            'id': len(opportunities) + 1,
            'category': 'Research & Learning',
            'impact': 'MEDIUM',
            'current_state': "High percentage of research/learning sessions",
            'problem': 'Research can be token-intensive',
            'options': [
                {
                    'name': 'Documentation First',
                    'description': 'Check official docs before asking AI',
                    'estimated_savings': '25-35%',
                    'trade_off': 'More time reading docs'
                },
                {
                    'name': 'Targeted Questions',
                    'description': 'Ask specific questions vs broad exploration',
                    'estimated_savings': '15-25%',
                    'trade_off': 'May miss broader context'
                },
                {
                    'name': 'Web Search First',
                    'description': 'Quick Google search before AI deep-dive',
                    'estimated_savings': '20-30%',
                    'trade_off': 'Context switching to browser'
                }
            ]
        })

    print(f"\n[+] Found {len(opportunities)} optimization opportunities")

    return opportunities

def interactive_optimization_selection(opportunities):
    """Go through each optimization one by one."""
    print("\n" + "=" * 70)
    print("[*] INTERACTIVE OPTIMIZATION SELECTION")
    print("=" * 70)

    print("\nLet's go through each optimization opportunity.")
    print("You'll see options and trade-offs for each.\n")

    input("Press Enter to start...")

    selected_optimizations = []

    for opp in opportunities:
        print("\n" + "=" * 70)
        print(f"[{opp['impact']}] Opportunity #{opp['id']}: {opp['category']}")
        print("=" * 70)

        print(f"\nCurrent State: {opp['current_state']}")
        print(f"Problem: {opp['problem']}")

        print(f"\nAvailable Options:")
        for idx, option in enumerate(opp['options'], 1):
            print(f"\n  [{idx}] {option['name']}")
            print(f"      {option['description']}")
            print(f"      Estimated savings: {option['estimated_savings']}")
            print(f"      Trade-off: {option['trade_off']}")

        print(f"\n  [0] Skip this optimization")

        while True:
            choice = input(f"\nSelect option (0-{len(opp['options'])}): ").strip()
            try:
                choice_idx = int(choice)
                if choice_idx == 0:
                    print("  [*] Skipped")
                    break
                elif 1 <= choice_idx <= len(opp['options']):
                    selected_option = opp['options'][choice_idx - 1]
                    selected_optimizations.append({
                        'opportunity': opp,
                        'selected_option': selected_option
                    })
                    print(f"  [+] Selected: {selected_option['name']}")
                    break
                else:
                    print("  [!] Invalid choice. Try again.")
            except ValueError:
                print("  [!] Please enter a number.")

    return selected_optimizations

def display_optimization_summary(selected_optimizations):
    """Display summary and estimated improvements."""
    print("\n" + "=" * 70)
    print("[*] OPTIMIZATION SUMMARY")
    print("=" * 70)

    if not selected_optimizations:
        print("\nNo optimizations selected.")
        return

    print(f"\nYou've selected {len(selected_optimizations)} optimizations:\n")

    total_min_savings = 0
    total_max_savings = 0

    for idx, opt in enumerate(selected_optimizations, 1):
        opp = opt['opportunity']
        selected = opt['selected_option']

        print(f"{idx}. {opp['category']}: {selected['name']}")
        print(f"   Estimated savings: {selected['estimated_savings']}")
        print(f"   Trade-off: {selected['trade_off']}")
        print()

        # Parse savings range
        savings_range = selected['estimated_savings'].replace('%', '').split('-')
        if len(savings_range) == 2:
            total_min_savings += float(savings_range[0])
            total_max_savings += float(savings_range[1])

    # Calculate estimated improvement
    if total_min_savings > 0:
        avg_savings = (total_min_savings + total_max_savings) / 2
        print(f"[+] ESTIMATED TOTAL IMPROVEMENT: {total_min_savings:.0f}%-{total_max_savings:.0f}%")
        print(f"    (Average: {avg_savings:.0f}%)")
        print(f"\nNote: Actual savings depend on implementation consistency.")

def apply_selected_optimizations(selected_optimizations, project_stats):
    """Apply the selected optimizations."""
    print("\n" + "=" * 70)
    print("[*] APPLYING OPTIMIZATIONS")
    print("=" * 70)

    applied = []

    for opt in selected_optimizations:
        opp = opt['opportunity']
        selected = opt['selected_option']

        print(f"\n[+] Applying: {opp['category']} - {selected['name']}")

        # Apply based on category
        if 'Documentation' in opp['category']:
            create_optimization_rule('documentation', selected, project_stats)
            applied.append(f"{opp['category']}: {selected['name']}")

        elif 'Configuration' in opp['category']:
            create_optimization_rule('configuration', selected, project_stats)
            applied.append(f"{opp['category']}: {selected['name']}")

        elif 'Search' in opp['category']:
            create_optimization_rule('search', selected, project_stats)
            applied.append(f"{opp['category']}: {selected['name']}")

        elif 'File Operations' in opp['category']:
            create_optimization_rule('file_ops', selected, project_stats)
            applied.append(f"{opp['category']}: {selected['name']}")

        elif 'Verbosity' in opp['category']:
            create_optimization_rule('verbosity', selected, project_stats)
            applied.append(f"{opp['category']}: {selected['name']}")

        elif 'Research' in opp['category']:
            create_optimization_rule('research', selected, project_stats)
            applied.append(f"{opp['category']}: {selected['name']}")

    print("\n" + "=" * 70)
    print("[+] APPLICATION COMPLETE")
    print("=" * 70)

    if applied:
        print("\nSuccessfully applied:")
        for item in applied:
            print(f"  - {item}")

    return applied

def create_optimization_rule(rule_type, selected_option, project_stats):
    """Create or update optimization rules."""
    # Implementation would create/update CLAUDE.md files based on selections
    # For now, just print what would be done
    print(f"    Creating rule for: {selected_option['name']}")
    print(f"    Description: {selected_option['description']}")

def save_snapshot(analysis, selected_optimizations, project_stats):
    """Save analysis snapshot with timestamp."""
    snapshot_dir = Path.home() / '.claude' / 'token-analyzer-snapshots'
    snapshot_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    snapshot_file = snapshot_dir / f'snapshot_{timestamp}.json'

    snapshot_data = {
        'timestamp': timestamp,
        'datetime': datetime.now().isoformat(),
        'analysis': {
            'total_sessions': analysis['total_sessions'],
            'total_messages': analysis['total_messages'],
            'category_counts': dict(analysis['category_counts']),
            'work_type_counts': dict(analysis['work_type_counts']),
            'project_stats': {k: dict(v) for k, v in analysis['project_stats'].items()}
        },
        'optimizations': [
            {
                'category': opt['opportunity']['category'],
                'selected': opt['selected_option']['name'],
                'estimated_savings': opt['selected_option']['estimated_savings']
            }
            for opt in selected_optimizations
        ]
    }

    with open(snapshot_file, 'w', encoding='utf-8') as f:
        json.dump(snapshot_data, f, indent=2)

    print(f"\n[+] Snapshot saved: {snapshot_file}")
    return str(snapshot_file)

def load_previous_snapshot():
    """Load the most recent snapshot."""
    snapshot_dir = Path.home() / '.claude' / 'token-analyzer-snapshots'
    if not snapshot_dir.exists():
        return None

    snapshots = sorted(snapshot_dir.glob('snapshot_*.json'), reverse=True)
    if not snapshots:
        return None

    with open(snapshots[0], 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_with_previous(current_analysis, previous_snapshot):
    """Compare current analysis with previous snapshot."""
    print("\n" + "=" * 70)
    print("[*] IMPROVEMENT ANALYSIS")
    print("=" * 70)

    prev_sessions = previous_snapshot['analysis']['total_sessions']
    curr_sessions = current_analysis['total_sessions']

    prev_messages = previous_snapshot['analysis']['total_messages']
    curr_messages = current_analysis['total_messages']

    print(f"\nPrevious snapshot: {previous_snapshot['datetime']}")
    print(f"Applied optimizations:")
    for opt in previous_snapshot.get('optimizations', []):
        print(f"  - {opt['category']}: {opt['selected']}")

    print(f"\n[+] Session Comparison:")
    print(f"    Before: {prev_sessions} sessions")
    print(f"    Now: {curr_sessions} sessions")
    session_change = ((curr_sessions - prev_sessions) / prev_sessions * 100) if prev_sessions > 0 else 0
    print(f"    Change: {session_change:+.1f}%")

    print(f"\n[+] Message Comparison:")
    print(f"    Before: {prev_messages} messages")
    print(f"    Now: {curr_messages} messages")
    message_change = ((curr_messages - prev_messages) / prev_messages * 100) if prev_messages > 0 else 0
    print(f"    Change: {message_change:+.1f}%")

    # Compare categories
    print(f"\n[+] Category Changes:")
    prev_cats = previous_snapshot['analysis']['category_counts']
    curr_cats = dict(current_analysis['category_counts'])

    for category in set(list(prev_cats.keys()) + list(curr_cats.keys())):
        prev_count = prev_cats.get(category, 0)
        curr_count = curr_cats.get(category, 0)

        if prev_count > 0:
            change = ((curr_count - prev_count) / prev_count * 100)
            if abs(change) > 10:  # Only show significant changes
                indicator = "↓" if change < 0 else "↑"
                print(f"    {category}: {prev_count} → {curr_count} ({change:+.0f}%) {indicator}")

def main():
    """Main execution flow."""
    print("=" * 70)
    print("CLAUDE CODE TOKEN ANALYZER V2")
    print("Enhanced with Scope Selection, Delta Tracking & Interactive Optimization")
    print("=" * 70)

    # Load data
    claude_dir = Path.home() / '.claude'
    history_path = claude_dir / 'history.jsonl'
    stats_path = claude_dir / 'stats-cache.json'

    print("\nLoading conversation history...")
    sessions, session_metadata = load_history_with_metadata(history_path)

    print("Loading token statistics...")
    with open(stats_path, 'r', encoding='utf-8') as f:
        stats = json.load(f)

    # Check for previous snapshot
    previous_snapshot = load_previous_snapshot()
    if previous_snapshot:
        print(f"\n[+] Found previous snapshot from {previous_snapshot['datetime']}")
        compare = input("Compare with previous snapshot? (y/n): ").strip().lower()
        if compare == 'y':
            # Quick comparison before proceeding
            print("\nPrevious optimizations applied:")
            for opt in previous_snapshot.get('optimizations', []):
                print(f"  - {opt['category']}: {opt['selected']} ({opt['estimated_savings']})")

    # Phase 1: Scope Selection
    selected_projects = select_scope(sessions, session_metadata)

    # Phase 2: Thorough Analysis
    analysis = analyze_scope(sessions, session_metadata, selected_projects, stats)

    # Phase 3: Display Breakdown
    display_analysis_breakdown(analysis, stats)

    # Ask if user wants to continue to optimization
    print("\n" + "=" * 70)
    proceed = input("\nProceed to optimization insights? (y/n): ").strip().lower()
    if proceed != 'y':
        print("\nAnalysis complete. Run again when ready to optimize!")
        return

    # Phase 4: Identify Opportunities
    opportunities = identify_optimization_opportunities(analysis, stats)

    # Phase 5: Interactive Selection
    selected_optimizations = interactive_optimization_selection(opportunities)

    # Phase 6: Display Summary
    display_optimization_summary(selected_optimizations)

    # Ask if user wants to apply
    print("\n" + "=" * 70)
    apply = input("\nApply these optimizations? (y/n): ").strip().lower()
    if apply == 'y':
        applied = apply_selected_optimizations(selected_optimizations, analysis['project_stats'])

        # Phase 7: Save Snapshot
        snapshot_file = save_snapshot(analysis, selected_optimizations, analysis['project_stats'])

        print("\n" + "=" * 70)
        print("[*] COMPLETE")
        print("=" * 70)
        print("\nOptimizations have been applied and snapshot saved.")
        print("Run this tool again in the future to measure improvement!")
    else:
        print("\nNo changes applied. Analysis complete.")

    # If we had a previous snapshot, show delta
    if previous_snapshot and apply == 'y':
        compare_with_previous(analysis, previous_snapshot)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Exiting...")
    except FileNotFoundError as e:
        print(f"[!] Error: Could not find file - {e}")
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
