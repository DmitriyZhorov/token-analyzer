#!/usr/bin/env python3
"""
Team Token Usage Aggregator
Exports individual stats to shared repo and aggregates team statistics
"""

import json
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime
import subprocess

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

def export_personal_stats(output_dir, date_from=None, date_to=None):
    """Export personal token statistics to shared repo."""
    print("\n" + "=" * 70)
    print("[*] EXPORTING PERSONAL STATISTICS")
    print("=" * 70)

    # Load data
    claude_dir = Path.home() / '.claude'
    history_path = claude_dir / 'history.jsonl'
    stats_path = claude_dir / 'stats-cache.json'

    print("\nLoading your Claude Code history...")

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
                if date_from and timestamp < date_from:
                    continue
                if date_to and timestamp > date_to:
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
    date_range = {
        'from': min(all_timestamps) if all_timestamps else 0,
        'to': max(all_timestamps) if all_timestamps else 0
    }

    # Create export data
    export_data = {
        'exported_at': datetime.now().isoformat(),
        'user': user,
        'date_range': {
            'from': datetime.fromtimestamp(date_range['from'] / 1000).isoformat() if date_range['from'] else None,
            'to': datetime.fromtimestamp(date_range['to'] / 1000).isoformat() if date_range['to'] else None
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

    print(f"\n[+] Exported statistics to: {output_path}")
    print(f"    User: {user['name']} <{user['email']}>")
    print(f"    Sessions: {total_sessions}")
    print(f"    Messages: {total_messages}")
    print(f"    Date range: {export_data['date_range']['from']} to {export_data['date_range']['to']}")

    return str(output_path)

def aggregate_team_stats(stats_dir):
    """Aggregate statistics from all team members."""
    print("\n" + "=" * 70)
    print("[*] AGGREGATING TEAM STATISTICS")
    print("=" * 70)

    stats_dir = Path(stats_dir)
    if not stats_dir.exists():
        print(f"[!] Directory not found: {stats_dir}")
        return

    # Load all team member stats
    team_data = []
    for stat_file in stats_dir.glob('*.json'):
        try:
            with open(stat_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                team_data.append(data)
        except Exception as e:
            print(f"[!] Error loading {stat_file.name}: {e}")

    if not team_data:
        print("[!] No statistics files found")
        return

    print(f"\n[+] Found statistics for {len(team_data)} team member(s)")

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
    print("\n" + "=" * 70)
    print("[*] TEAM SUMMARY")
    print("=" * 70)

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

    # Individual contributor breakdown
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

    # Save aggregated report
    report_path = stats_dir / f"team_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(team_summary, f, indent=2)

    print(f"\n[+] Team report saved to: {report_path}")

    return team_summary

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Claude Code Team Token Aggregator')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export personal statistics')
    export_parser.add_argument('--output-dir', required=True, help='Output directory (shared repo)')
    export_parser.add_argument('--date-from', help='Filter from date (YYYY-MM-DD)')
    export_parser.add_argument('--date-to', help='Filter to date (YYYY-MM-DD)')
    export_parser.add_argument('--commit', action='store_true', help='Auto-commit to git repo')

    # Aggregate command
    aggregate_parser = subparsers.add_parser('aggregate', help='Aggregate team statistics')
    aggregate_parser.add_argument('--stats-dir', required=True, help='Directory with team stats')
    aggregate_parser.add_argument('--output', help='Output file for team report')

    args = parser.parse_args()

    if args.command == 'export':
        # Parse dates if provided
        date_from = None
        date_to = None

        if args.date_from:
            dt = datetime.strptime(args.date_from, '%Y-%m-%d')
            date_from = int(dt.timestamp() * 1000)

        if args.date_to:
            dt = datetime.strptime(args.date_to, '%Y-%m-%d')
            date_to = int(dt.timestamp() * 1000)

        # Export stats
        output_file = export_personal_stats(args.output_dir, date_from, date_to)

        # Auto-commit if requested
        if args.commit:
            try:
                output_dir = Path(args.output_dir)
                subprocess.run(['git', '-C', str(output_dir), 'add', Path(output_file).name], check=True)

                user = get_user_identity()
                commit_msg = f"Add token stats for {user['name']} - {datetime.now().strftime('%Y-%m-%d')}"
                subprocess.run(['git', '-C', str(output_dir), 'commit', '-m', commit_msg], check=True)

                print("\n[+] Changes committed to git")
                print("    Run 'git push' to share with team")
            except Exception as e:
                print(f"\n[!] Git commit failed: {e}")
                print("    You can manually commit and push")

    elif args.command == 'aggregate':
        team_summary = aggregate_team_stats(args.stats_dir)

        if args.output and team_summary:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(team_summary, f, indent=2)
            print(f"\n[+] Team report also saved to: {args.output}")

    else:
        parser.print_help()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
