#!/usr/bin/env python3
"""
Team Token Usage Aggregator - Interactive Version
Fully interactive interface with guided prompts
"""

import json
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import re

def get_user_identity():
    """Get user identity from git config."""
    try:
        name = subprocess.check_output(['git', 'config', 'user.name'], text=True).strip()
        email = subprocess.check_output(['git', 'config', 'user.email'], text=True).strip()
        return {'name': name, 'email': email}
    except:
        import getpass
        import socket
        return {
            'name': getpass.getuser(),
            'email': f"{getpass.getuser()}@{socket.gethostname()}"
        }

def print_header(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"[*] {title}")
    print("=" * 70)

def print_menu(options):
    """Print menu options."""
    print()
    for idx, option in enumerate(options, 1):
        print(f"  [{idx}] {option}")
    print()

def get_choice(prompt, max_choice):
    """Get user choice with validation."""
    while True:
        try:
            choice = input(prompt).strip()
            choice_num = int(choice)
            if 1 <= choice_num <= max_choice:
                return choice_num
            else:
                print(f"  [!] Please enter a number between 1 and {max_choice}")
        except ValueError:
            print("  [!] Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n[!] Cancelled by user")
            sys.exit(0)

def get_yes_no(prompt):
    """Get yes/no confirmation."""
    while True:
        response = input(prompt + " (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("  [!] Please enter 'y' or 'n'")

def get_path(prompt, must_exist=False, create_if_missing=False):
    """Get path with validation."""
    while True:
        path_str = input(prompt).strip()
        if not path_str:
            print("  [!] Path cannot be empty")
            continue

        path = Path(path_str).expanduser()

        if must_exist and not path.exists():
            print(f"  [!] Path does not exist: {path}")
            if create_if_missing:
                create = get_yes_no("    Create it?")
                if create:
                    path.mkdir(parents=True, exist_ok=True)
                    print(f"  [+] Created: {path}")
                    return str(path)
            continue

        return str(path)

def get_date(prompt, allow_empty=False):
    """Get date with validation."""
    print(f"\n{prompt}")
    print("  Format: YYYY-MM-DD (e.g., 2024-02-12)")
    if allow_empty:
        print("  Or press Enter to skip")

    while True:
        date_str = input("  Date: ").strip()

        if not date_str and allow_empty:
            return None

        if not date_str:
            print("  [!] Date is required")
            continue

        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return dt
        except ValueError:
            print("  [!] Invalid date format. Use YYYY-MM-DD")

def show_date_presets():
    """Show common date range presets."""
    print("\n  Quick presets:")
    today = datetime.now()

    presets = {
        'L7': ('Last 7 days', today - timedelta(days=7), today),
        'L30': ('Last 30 days', today - timedelta(days=30), today),
        'TW': ('This week', today - timedelta(days=today.weekday()), today),
        'LW': ('Last week',
               today - timedelta(days=today.weekday() + 7),
               today - timedelta(days=today.weekday() + 1)),
        'TM': ('This month', today.replace(day=1), today),
        'LM': ('Last month',
               (today.replace(day=1) - timedelta(days=1)).replace(day=1),
               today.replace(day=1) - timedelta(days=1))
    }

    for code, (desc, start, end) in presets.items():
        print(f"    {code} = {desc} ({start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')})")

    return presets

def get_date_range():
    """Get date range interactively."""
    print_header("DATE RANGE SELECTION")

    print("\nAnalyze specific time period?")
    use_filter = get_yes_no("Filter by date range?")

    if not use_filter:
        return None, None

    # Show presets
    presets = show_date_presets()
    print("\n  Enter preset code, or 'C' for custom dates")

    while True:
        choice = input("\n  Your choice: ").strip().upper()

        if choice in presets:
            _, date_from, date_to = presets[choice]
            print(f"\n  [+] Selected: {date_from.strftime('%Y-%m-%d')} to {date_to.strftime('%Y-%m-%d')}")
            return date_from, date_to

        elif choice == 'C':
            date_from = get_date("From date (start of period):", allow_empty=False)
            date_to = get_date("To date (end of period):", allow_empty=False)

            if date_from > date_to:
                print("  [!] From date must be before To date")
                continue

            return date_from, date_to

        else:
            print("  [!] Invalid choice. Enter preset code or 'C'")

def export_personal_stats(output_dir, date_from=None, date_to=None):
    """Export personal token statistics."""
    print_header("EXPORTING PERSONAL STATISTICS")

    # Load data
    claude_dir = Path.home() / '.claude'
    history_path = claude_dir / 'history.jsonl'
    stats_path = claude_dir / 'stats-cache.json'

    if not history_path.exists():
        print(f"\n[!] Error: Claude history not found at {history_path}")
        print("    Make sure you have used Claude Code before")
        return None

    print("\nLoading your Claude Code history...")

    # Convert dates to timestamps
    ts_from = int(date_from.timestamp() * 1000) if date_from else None
    ts_to = int(date_to.timestamp() * 1000) if date_to else None

    # Load sessions with time filtering
    sessions = defaultdict(list)
    session_metadata = {}

    with open(history_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if 'sessionId' not in entry or 'display' not in entry:
                    continue

                timestamp = entry.get('timestamp', 0)

                # Apply time filtering
                if ts_from and timestamp < ts_from:
                    continue
                if ts_to and timestamp > ts_to:
                    continue

                session_id = entry['sessionId']
                sessions[session_id].append({
                    'message': entry['display'],
                    'timestamp': timestamp
                })

                if session_id not in session_metadata:
                    session_metadata[session_id] = {
                        'project': entry.get('project', 'Unknown'),
                        'timestamp': timestamp
                    }
            except:
                continue

    if not sessions:
        print("\n[!] No sessions found in the specified date range")
        return None

    # Load token stats
    with open(stats_path, 'r', encoding='utf-8') as f:
        stats = json.load(f)

    # Get user identity
    user = get_user_identity()

    # Calculate statistics
    total_sessions = len(sessions)
    total_messages = sum(len(msgs) for msgs in sessions.values())

    # Calculate by project
    project_stats = defaultdict(lambda: {'sessions': 0, 'messages': 0})
    for session_id, messages in sessions.items():
        metadata = session_metadata.get(session_id, {})
        project_path = metadata.get('project', 'Unknown')
        project_name = Path(project_path).name if project_path != 'Unknown' else 'Unknown'

        project_stats[project_name]['sessions'] += 1
        project_stats[project_name]['messages'] += len(messages)

    # Calculate date range
    all_timestamps = [m['timestamp'] for msgs in sessions.values() for m in msgs]
    actual_range = {
        'from': min(all_timestamps) if all_timestamps else 0,
        'to': max(all_timestamps) if all_timestamps else 0
    }

    # Create export data
    export_data = {
        'exported_at': datetime.now().isoformat(),
        'user': user,
        'date_range': {
            'from': datetime.fromtimestamp(actual_range['from'] / 1000).isoformat() if actual_range['from'] else None,
            'to': datetime.fromtimestamp(actual_range['to'] / 1000).isoformat() if actual_range['to'] else None
        },
        'summary': {
            'total_sessions': total_sessions,
            'total_messages': total_messages,
            'model_usage': stats.get('modelUsage', {})
        },
        'by_project': dict(project_stats),
        'daily_activity': stats.get('dailyActivity', []),
        'daily_model_tokens': stats.get('dailyModelTokens', [])
    }

    # Save to output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{user['email'].replace('@', '_at_')}_{timestamp}.json"
    output_path = output_dir / filename

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2)

    print(f"\n[+] Statistics Exported!")
    print(f"    File: {output_path}")
    print(f"    User: {user['name']} <{user['email']}>")
    print(f"    Sessions: {total_sessions}")
    print(f"    Messages: {total_messages}")
    print(f"    Date range: {export_data['date_range']['from']} to {export_data['date_range']['to']}")

    # Show top projects
    if project_stats:
        print(f"\n[+] Top Projects:")
        sorted_projects = sorted(project_stats.items(), key=lambda x: x[1]['sessions'], reverse=True)[:5]
        for project, pstats in sorted_projects:
            print(f"    {project}: {pstats['sessions']} sessions, {pstats['messages']} messages")

    return str(output_path)

def aggregate_team_stats(stats_dir):
    """Aggregate statistics from all team members."""
    print_header("AGGREGATING TEAM STATISTICS")

    stats_dir = Path(stats_dir)
    if not stats_dir.exists():
        print(f"\n[!] Directory not found: {stats_dir}")
        return None

    # Load all team member stats
    team_data = []
    json_files = list(stats_dir.glob('*_at_*.json'))

    if not json_files:
        print(f"\n[!] No team statistics files found in {stats_dir}")
        print("    Files should match pattern: *_at_*.json")
        return None

    print(f"\nFound {len(json_files)} potential stat file(s)...")

    for stat_file in json_files:
        try:
            with open(stat_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Validate structure
                if 'user' in data and 'summary' in data:
                    team_data.append(data)
                    print(f"  [+] Loaded: {stat_file.name}")
                else:
                    print(f"  [!] Skipped (invalid format): {stat_file.name}")
        except Exception as e:
            print(f"  [!] Error loading {stat_file.name}: {e}")

    if not team_data:
        print("\n[!] No valid statistics files found")
        return None

    print(f"\n[+] Successfully loaded {len(team_data)} team member(s)")

    # Aggregate data
    team_summary = {
        'aggregated_at': datetime.now().isoformat(),
        'team_size': len(team_data),
        'members': [],
        'totals': {
            'sessions': 0,
            'messages': 0,
            'tokens': defaultdict(lambda: {'input': 0, 'output': 0})
        },
        'by_project': defaultdict(lambda: {'sessions': 0, 'messages': 0, 'contributors': set()}),
        'by_member': []
    }

    for member_data in team_data:
        user = member_data['user']
        summary = member_data['summary']

        # Add member info
        team_summary['members'].append({
            'name': user['name'],
            'email': user['email'],
            'sessions': summary['total_sessions'],
            'messages': summary['total_messages']
        })

        # Aggregate totals
        team_summary['totals']['sessions'] += summary['total_sessions']
        team_summary['totals']['messages'] += summary['total_messages']

        # Aggregate tokens by model
        for model, usage in summary.get('model_usage', {}).items():
            team_summary['totals']['tokens'][model]['input'] += usage.get('inputTokens', 0)
            team_summary['totals']['tokens'][model]['output'] += usage.get('outputTokens', 0)

        # Aggregate by project
        for project, pstats in member_data.get('by_project', {}).items():
            team_summary['by_project'][project]['sessions'] += pstats['sessions']
            team_summary['by_project'][project]['messages'] += pstats['messages']
            team_summary['by_project'][project]['contributors'].add(user['email'])

        # Member-level stats
        team_summary['by_member'].append({
            'user': user,
            'sessions': summary['total_sessions'],
            'messages': summary['total_messages'],
            'top_projects': sorted(
                member_data.get('by_project', {}).items(),
                key=lambda x: x[1]['sessions'],
                reverse=True
            )[:3]
        })

    # Convert sets to lists for JSON serialization
    for project in team_summary['by_project'].values():
        project['contributors'] = list(project['contributors'])
        project['contributor_count'] = len(project['contributors'])

    team_summary['totals']['tokens'] = dict(team_summary['totals']['tokens'])
    team_summary['by_project'] = dict(team_summary['by_project'])

    # Display results
    print_header("TEAM SUMMARY")

    print(f"\n[+] Team Overview:")
    print(f"    Team size: {team_summary['team_size']} members")
    print(f"    Total sessions: {team_summary['totals']['sessions']}")
    print(f"    Total messages: {team_summary['totals']['messages']}")

    print(f"\n[+] Team Members:")
    sorted_members = sorted(team_summary['members'], key=lambda x: x['sessions'], reverse=True)
    for member in sorted_members:
        print(f"    {member['name']} <{member['email']}>")
        print(f"      Sessions: {member['sessions']}, Messages: {member['messages']}")

    print(f"\n[+] Top Team Projects:")
    sorted_projects = sorted(
        team_summary['by_project'].items(),
        key=lambda x: x[1]['sessions'],
        reverse=True
    )[:10]

    for project, pstats in sorted_projects:
        print(f"    {project}")
        print(f"      Sessions: {pstats['sessions']}, Messages: {pstats['messages']}")
        print(f"      Contributors: {pstats['contributor_count']}")

    print(f"\n[+] Token Usage by Model:")
    for model, usage in team_summary['totals']['tokens'].items():
        model_name = model.split('/')[-1]
        total = usage['input'] + usage['output']
        print(f"    {model_name}:")
        print(f"      Input: {usage['input']:,}, Output: {usage['output']:,}")
        print(f"      Total: {total:,}")

    print(f"\n[+] Individual Contributions:")
    for member_stats in sorted(team_summary['by_member'], key=lambda x: x['sessions'], reverse=True):
        user = member_stats['user']
        print(f"\n    {user['name']}:")
        print(f"      Total sessions: {member_stats['sessions']}")
        print(f"      Total messages: {member_stats['messages']}")
        if member_stats['top_projects']:
            print(f"      Top projects:")
            for project, pstats in member_stats['top_projects']:
                print(f"        - {project}: {pstats['sessions']} sessions")

    # Ask to save report
    print("\n" + "=" * 70)
    save_report = get_yes_no("Save team report to file?")

    if save_report:
        report_name = input("  Report filename (or Enter for default): ").strip()
        if not report_name:
            report_name = f"team_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        if not report_name.endswith('.json'):
            report_name += '.json'

        report_path = stats_dir / report_name
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(team_summary, f, indent=2)

        print(f"\n[+] Team report saved to: {report_path}")

    return team_summary

def interactive_export():
    """Interactive export workflow."""
    print_header("EXPORT PERSONAL STATISTICS")

    print("\nThis will export your Claude Code token usage statistics.")
    print("You can then commit these to a shared git repository for team analysis.")

    # Get output directory
    print("\n" + "-" * 70)
    print("Output Directory")
    print("-" * 70)
    print("\nWhere should the statistics be saved?")
    print("  Tip: Use your team's shared git repo directory")

    output_dir = get_path("  Path: ", must_exist=False, create_if_missing=True)

    # Get date range
    date_from, date_to = get_date_range()

    # Export
    output_file = export_personal_stats(output_dir, date_from, date_to)

    if not output_file:
        return

    # Git operations
    print("\n" + "=" * 70)
    print("[*] GIT OPERATIONS")
    print("=" * 70)

    # Check if in git repo
    output_path = Path(output_file)
    try:
        subprocess.run(
            ['git', '-C', str(output_path.parent), 'rev-parse', '--git-dir'],
            check=True,
            capture_output=True
        )
        in_git_repo = True
    except:
        in_git_repo = False

    if in_git_repo:
        print("\n[+] Output directory is in a git repository")
        auto_commit = get_yes_no("Commit and prepare for push?")

        if auto_commit:
            try:
                # Add file
                subprocess.run(
                    ['git', '-C', str(output_path.parent), 'add', output_path.name],
                    check=True
                )

                # Commit
                user = get_user_identity()
                commit_msg = f"Add token stats for {user['name']} - {datetime.now().strftime('%Y-%m-%d')}"
                subprocess.run(
                    ['git', '-C', str(output_path.parent), 'commit', '-m', commit_msg],
                    check=True
                )

                print("\n[+] Changes committed!")
                print("    Next step: Run 'git push' to share with team")

                push_now = get_yes_no("\nPush to remote now?")
                if push_now:
                    subprocess.run(
                        ['git', '-C', str(output_path.parent), 'push'],
                        check=True
                    )
                    print("\n[+] Pushed to remote!")
            except subprocess.CalledProcessError as e:
                print(f"\n[!] Git operation failed: {e}")
                print("    You can manually commit and push")
    else:
        print("\n[!] Output directory is not in a git repository")
        print("    Consider initializing git for team collaboration")

def interactive_aggregate():
    """Interactive aggregate workflow."""
    print_header("AGGREGATE TEAM STATISTICS")

    print("\nThis will combine statistics from all team members.")
    print("Make sure everyone has exported their stats to the shared directory.")

    # Get stats directory
    print("\n" + "-" * 70)
    print("Statistics Directory")
    print("-" * 70)
    print("\nWhere are the team statistics files?")
    print("  Tip: This is usually your shared git repo directory")

    stats_dir = get_path("  Path: ", must_exist=True)

    # Aggregate
    aggregate_team_stats(stats_dir)

def main_menu():
    """Main interactive menu."""
    print("\n" + "=" * 70)
    print("CLAUDE CODE TOKEN ANALYZER - TEAM & TIME FEATURES")
    print("=" * 70)

    print("\nWelcome! What would you like to do?")

    options = [
        "Export my statistics (for personal or team analysis)",
        "Aggregate team statistics (combine everyone's exports)",
        "Help & Documentation",
        "Exit"
    ]

    print_menu(options)

    choice = get_choice("Your choice: ", len(options))

    if choice == 1:
        interactive_export()
    elif choice == 2:
        interactive_aggregate()
    elif choice == 3:
        show_help()
    elif choice == 4:
        print("\nGoodbye!")
        sys.exit(0)

def show_help():
    """Show help information."""
    print_header("HELP & DOCUMENTATION")

    print("""
PERSONAL ANALYSIS:
  Export your statistics for a specific time period.
  Useful for tracking your own efficiency over time.

TEAM ANALYSIS:
  1. Each team member exports their stats
  2. Everyone commits to a shared git repo
  3. Anyone can aggregate to see team totals

TIME-BASED ANALYSIS:
  Filter by date range to compare:
  - Week over week
  - Month over month
  - Before/after optimization
  - Sprint retrospectives

WORKFLOW:
  1. Export → 2. Commit → 3. Push → 4. Aggregate

DOCUMENTATION:
  See README files in the project directory:
  - TEAM_USAGE.md - Team collaboration guide
  - TIME_BASED_ANALYSIS.md - Time analysis guide
  - QUICK_START.md - Quick reference

COMMAND-LINE MODE:
  For automation, use:
    python team_aggregator.py export --output-dir ./dir
    python team_aggregator.py aggregate --stats-dir ./dir

  Run with --help for all options
""")

    input("\nPress Enter to continue...")

def main():
    """Main entry point."""
    try:
        # Check if command-line args provided (automation mode)
        if len(sys.argv) > 1:
            # Fall back to original CLI mode
            import argparse
            parser = argparse.ArgumentParser(description='Claude Code Team Token Aggregator')
            subparsers = parser.add_subparsers(dest='command', help='Commands')

            # Export command
            export_parser = subparsers.add_parser('export', help='Export personal statistics')
            export_parser.add_argument('--output-dir', required=True, help='Output directory')
            export_parser.add_argument('--date-from', help='Filter from date (YYYY-MM-DD)')
            export_parser.add_argument('--date-to', help='Filter to date (YYYY-MM-DD)')
            export_parser.add_argument('--commit', action='store_true', help='Auto-commit to git')

            # Aggregate command
            aggregate_parser = subparsers.add_parser('aggregate', help='Aggregate team statistics')
            aggregate_parser.add_argument('--stats-dir', required=True, help='Directory with team stats')

            args = parser.parse_args()

            if args.command == 'export':
                date_from = datetime.strptime(args.date_from, '%Y-%m-%d') if args.date_from else None
                date_to = datetime.strptime(args.date_to, '%Y-%m-%d') if args.date_to else None

                output_file = export_personal_stats(args.output_dir, date_from, date_to)

                if args.commit and output_file:
                    try:
                        output_path = Path(output_file)
                        subprocess.run(['git', '-C', str(output_path.parent), 'add', output_path.name], check=True)
                        user = get_user_identity()
                        commit_msg = f"Add token stats for {user['name']} - {datetime.now().strftime('%Y-%m-%d')}"
                        subprocess.run(['git', '-C', str(output_path.parent), 'commit', '-m', commit_msg], check=True)
                        print("\n[+] Changes committed to git")
                    except Exception as e:
                        print(f"\n[!] Git commit failed: {e}")

            elif args.command == 'aggregate':
                aggregate_team_stats(args.stats_dir)

            else:
                parser.print_help()

        else:
            # Interactive mode
            while True:
                main_menu()
                print("\n" + "=" * 70)
                another = get_yes_no("Do another operation?")
                if not another:
                    print("\nGoodbye!")
                    break

    except KeyboardInterrupt:
        print("\n\n[!] Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
