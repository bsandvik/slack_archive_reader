import argparse
import os
import re
from datetime import datetime

from slack_archive_reader.helpers import load_json, parse_date
from slack_archive_reader.user_db import load_user_db, list_users, update_user, dump_users
from slack_archive_reader.message_search import get_message_by_ts, get_thread_by_ts, search_messages_recursive, gather_thread_messages
from slack_archive_reader.message_printer import print_messages

def main():
    parser = argparse.ArgumentParser(description="Slack JSON reader and search tool")
    parser.add_argument('-f', '--file', help='Slack JSON file', required=True)
    parser.add_argument('input', nargs='?', help='Search term for search')
    parser.add_argument('-s', '--start-time', help='Start time for search (YYYY-MM-DD HH:MM:SS or YYYY-MM-DD)')
    parser.add_argument('-e', '--end-time', help='End time for search (YYYY-MM-DD HH:MM:SS or YYYY-MM-DD)')
    parser.add_argument('-m', '--message', help='Message ID (timestamp) to fetch')
    parser.add_argument('-t', '--thread', help='Thread ID (thread_ts) to fetch')
    parser.add_argument('-u', '--user', help='Display messages from a specific user')
    parser.add_argument('--add-user', nargs=2, help='Add or update user ID with real name')
    parser.add_argument('--list-users', action='store_true', help='List all users in the database')
    parser.add_argument('--dump-users', action='store_true', help='Dump all user IDs from the file')
    parser.add_argument('--raw', action='store_true', help='Bypass all formatting')
    parser.add_argument('--db', help='Path to the user database file')
    parser.add_argument('--expanded', action='store_true', help='Show all messages from threads')

    args = parser.parse_args()

    # Set the default database path if not provided
    if not args.db:
        args.db = os.path.join(os.path.dirname(args.file), 'slack_users.db')

    load_user_db(args.db)  # Ensure user database is loaded

    if args.list_users:
        list_users()
        return

    if args.add_user:
        update_user(args.add_user[0], args.add_user[1], db_path=args.db)
        print(f"User {args.add_user[0]} updated to {args.add_user[1]}")
        return

    if 'SLACK_CHANNEL' in os.environ and not args.file:
        file_path = os.environ['SLACK_CHANNEL']
    else:
        file_path = args.file

    if not file_path:
        print("No file specified")
        return

    data = load_json(file_path)

    if args.dump_users:
        dump_users(data)
        return

    start_time = parse_date(args.start_time) if args.start_time else None
    end_time = parse_date(args.end_time) if args.end_time else None

    if args.message:
        message = get_message_by_ts(data, args.message)
        if message:
            print_messages([(datetime.fromtimestamp(float(message['ts'])).replace(microsecond=0), message)], raw=args.raw)
        else:
            print(f"No message found with timestamp {args.message}")
        return

    if args.thread:
        thread_messages = get_thread_by_ts(data, args.thread)
        if thread_messages:
            messages = [(datetime.fromtimestamp(float(m['ts'])).replace(microsecond=0), m) for m in thread_messages]
            messages = sorted(messages, key=lambda x: x[0])
            unique_messages = []
            seen = set()
            for message in messages:
                if message[1]['ts'] not in seen:
                    unique_messages.append(message)
                    seen.add(message[1]['ts'])
            print_messages(unique_messages, raw=args.raw, thread_view=True)
        else:
            print(f"No thread found with thread_ts {args.thread}")
        return

    if args.user:
        user_id = None
        user_name = args.user
        if re.match(r'^U[A-Z0-9]{8,}$', args.user):
            user_id = args.user
            user_name = None
        results = search_messages_recursive(data['messages'], search_term=args.input, start_date=start_time, end_time=end_time, user_id=user_id, user_name=user_name)
        if args.expanded:
            print(f"Gathering expanded thread messages... {len(results)} initial messages")
            results = gather_thread_messages(results, data['messages'])
            print(f"Expanded to {len(results)} total messages")
        print_messages(results, raw=args.raw, thread_view=args.expanded)
        return

    if args.input:
        search_term = args.input
        results = search_messages_recursive(data['messages'], search_term=search_term, start_date=start_time, end_time=end_time)
        if args.expanded:
            print(f"Gathering expanded thread messages... {len(results)} initial messages")
            results = gather_thread_messages(results, data['messages'])
            print(f"Expanded to {len(results)} total messages")
        print_messages(results, search_term=search_term, raw=args.raw, thread_view=args.expanded)
    else:
        messages = [(datetime.fromtimestamp(float(m['ts'])).replace(microsecond=0), m) for m in data['messages']]
        messages = [(msg_date, m) for msg_date, m in messages if (not start_time or msg_date >= start_time) and (not end_time or msg_date <= end_time)]
        if args.expanded:
            print(f"Gathering expanded thread messages... {len(messages)} initial messages")
            messages = gather_thread_messages(messages, data['messages'])
            print(f"Expanded to {len(messages)} total messages")
        print_messages(messages, raw=args.raw if args.raw else False, thread_view=args.expanded)

if __name__ == '__main__':
    main()
