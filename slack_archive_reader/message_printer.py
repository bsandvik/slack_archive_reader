import re
import markdown2
import emoji
import pydoc
import shutil
from datetime import datetime
from slack_archive_reader.message_parser import parse_special_cases
from slack_archive_reader.user_db import get_user_name

def print_messages(messages, search_term=None, raw=False, thread_view=False):
    def highlight(text, term):
        return re.sub(f'({re.escape(term)})', r'\033[1;31m\1\033[0m', text, flags=re.IGNORECASE)

    def render_markdown(text):
        html = markdown2.markdown(text)
        return re.sub(r'<[^>]+>', '', html)

    # Sort messages by their timestamps
    messages = sorted(messages, key=lambda x: x[0])

    content = []
    for i, (msg_date, message) in enumerate(messages):
        user_name = get_user_name(message['user']) if 'user' in message else "Unknown User"
        text = message['text']
        thread_indicator = ""
        if 'thread_ts' in message and message['ts'] == message['thread_ts']:
            thread_indicator = f" [Thread ID: {message['thread_ts']}]"
        if thread_view and i > 0:
            timestamp = f"🧵 {msg_date.strftime('%m-%d %H:%M:%S')}"
        else:
            timestamp = f"{msg_date.strftime('%Y-%m-%d %H:%M:%S')}"
        if not raw:
            text = parse_special_cases(text)
            if search_term:
                text = highlight(text, search_term)
            text = render_markdown(text)
            content.append(f"\033[1;32m{timestamp}\033[0m - \033[1;34m{user_name}\033[0m: {text.rstrip()}{thread_indicator}")
        else:
            text = parse_special_cases(text, raw=True)
            content.append(f"{timestamp} - {user_name}: {text.rstrip()}{thread_indicator}")

        # Add replies if expanded view is enabled
        if thread_view and 'replies' in message:
            for reply in message['replies']:
                reply_user_name = get_user_name(reply['user']) if 'user' in reply else "Unknown User"
                reply_text = reply['text']
                reply_timestamp = datetime.fromtimestamp(float(reply['ts'])).strftime('%Y-%m-%d %H:%M:%S')
                if not raw:
                    reply_text = parse_special_cases(reply_text)
                    if search_term:
                        reply_text = highlight(reply_text, search_term)
                    reply_text = render_markdown(reply_text)
                    content.append(f"    \033[1;32m{reply_timestamp}\033[0m - \033[1;34m{reply_user_name}\033[0m: {reply_text.rstrip()}")
                else:
                    reply_text = parse_special_cases(reply_text, raw=True)
                    content.append(f"    {reply_timestamp} - {reply_user_name}: {reply_text.rstrip()}")

    # Output the content
    terminal_size = shutil.get_terminal_size((80, 20))
    if len(content) <= terminal_size.lines:
        for line in content:
            line = line.rstrip()
            if line.strip():  # Only print the line if it's not empty after stripping whitespace
                print(line)
    else:
        pydoc.pipepager("\n".join(content), cmd='less -R')
