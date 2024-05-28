import re
import emoji

from slack_archive_reader.user_db import get_user_name, user_db

def parse_special_cases(text, raw=False):
    def replace_user_id(match):
        user_id = match.group(1)
        user_name = get_user_name(user_id)
        if user_id in user_db:
            return f"@{user_name}" if raw else f"\033[1;33m@{user_name}\033[0m"  # Bright yellow
        else:
            return f"@{user_name}" if raw else f"\033[0;33m@{user_name}\033[0m"  # Dull yellow
    
    def replace_channel_name(match):
        channel_name = match.group(2)
        return f"#{channel_name}"

    def replace_subteam(match):
        subteam_name = match.group(1)
        return f"{subteam_name}" if raw else f"\033[1;32m{subteam_name}\033[0m"  # Green

    def replace_url(match):
        url = match.group(1)
        return f"{url}" if raw else f"\033[1;36m{url}\033[0m"  # Cyan

    def replace_clickable_link(match):
        url = match.group(1)
        text = match.group(2)
        return f"{text}" if raw else f"\033]8;;{url}\033\\{text}\033]8;;\033\\"  # Clickable link

    patterns = [
        (r'<@([A-Z0-9]+)>', replace_user_id),
        (r'<#([A-Z0-9]+)\|([^>]+)>', replace_channel_name),
        (r'<!subteam\^[A-Z0-9]+\|(@[^>]+)>', replace_subteam),
        (r'(_)', r'\_'),  # Preserve underscores by escaping them
        (r'<(https?://[^>]+)>', replace_url),         # For URLs with < and >
        (r'(https?://[\w.-]+(?:/[\w.-_]*)?)', replace_url),  # For standalone URLs (modified)
        (r'(https?://[\w.-]+(?:/[\w.-_]*)?)\|([^>]+)', replace_clickable_link),  # For clickable links (modified)
    ]

    for pattern, repl in patterns:
        text = re.sub(pattern, repl, text)

    custom_replacements = {
        ":shank:": ":shanks:",
        ":schlightly_smiling_face:": ":smile:"
    }

    for old, new in custom_replacements.items():
        text = text.replace(old, new)

    # Convert emoji notations to Unicode emoji after applying custom replacements
    text = emoji.emojize(text, language='alias') if not raw else text

    if not raw:
        # Handle single backtick code blocks
        text = re.sub(r'(?<!`)`([^`]+)`(?!`)', r'\033[1;35m\1\033[0m', text)

        # Handle triple backtick code blocks and ensure underscores are preserved
        code_block_pattern = r'```(.*?)```'
        def replace_code_block(match):
            code_block = match.group(1)
            code_block = code_block.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
            return f"\033[1;35m{code_block}\033[0m"  # Magenta for code blocks
        text = re.sub(code_block_pattern, replace_code_block, text, flags=re.DOTALL)

    return text
