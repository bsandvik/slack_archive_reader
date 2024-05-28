import re
from datetime import datetime
from slack_archive_reader.user_db import get_user_name

def get_message_by_ts(data, ts):
    for message in data['messages']:
        if message.get('ts') == ts:
            return message
    return None

def get_thread_by_ts(data, thread_ts):
    thread_messages = []
    for message in data['messages']:
        if message.get('thread_ts') == thread_ts:
            thread_messages.append(message)
        if 'replies' in message:
            for reply in message['replies']:
                if reply.get('thread_ts') == thread_ts or reply.get('ts') == thread_ts:
                    thread_messages.append(reply)
    return thread_messages

import re
from datetime import datetime
from slack_archive_reader.user_db import get_user_name

def search_messages_recursive(messages, search_term=None, start_date=None, end_time=None, user_id=None, user_name=None):
    results = []
    seen = set()
    search_regex = re.compile(re.escape(search_term), re.IGNORECASE) if search_term else None

    def search_message(message, search_regex, start_date, end_time, user_id, user_name):
        ts = float(message.get('ts'))
        msg_date = datetime.fromtimestamp(ts).replace(microsecond=0)
        if start_date and msg_date < start_date:
            return False
        if end_time and msg_date > end_time:
            return False
        if user_id and message.get('user') != user_id:
            return False
        if user_name:
            user_real_name = get_user_name(message.get('user'))
            if not user_real_name or user_name.lower() not in user_real_name.lower():
                return False
        if search_term and not search_regex.search(message.get('text', '')):
            return False
        return True

    def recurse_messages(messages, results, search_regex, start_date, end_time, user_id, user_name, seen):
        for message in messages:
            if search_message(message, search_regex, start_date, end_time, user_id, user_name):
                if message['ts'] not in seen:
                    results.append((datetime.fromtimestamp(float(message['ts'])).replace(microsecond=0), message))
                    seen.add(message['ts'])
            if 'replies' in message:
                recurse_messages(message['replies'], results, search_regex, start_date, end_time, user_id, user_name, seen)

    recurse_messages(messages, results, search_regex, start_date, end_time, user_id, user_name, seen)
    return results

def gather_thread_messages(messages, all_messages):
    results = []
    seen = set()

    def gather_thread(thread_ts, all_messages):
        thread_messages = []
        for message in all_messages:
            if message.get('thread_ts') == thread_ts or message.get('ts') == thread_ts:
                if message['ts'] not in seen:
                    thread_messages.append(message)
                    seen.add(message['ts'])
        return thread_messages

    for msg_date, message in messages:
        results.append((msg_date, message))
        if 'thread_ts' in message:
            thread_messages = gather_thread(message['thread_ts'], all_messages)
            for tm in thread_messages:
                ts = float(tm['ts'])
                results.append((datetime.fromtimestamp(ts).replace(microsecond=0), tm))

    return results
