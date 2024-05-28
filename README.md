# Slack Archive Reader

Slack Archive Reader is a tool for reading and searching Slack JSON export files. It provides functionality to list users, search messages, and display threads in a readable format.

## Features

- List users from the Slack archive
- Search messages by keyword
- Display messages and threads with special formatting
- Expand threads to show all messages in a conversation

## Installation

### Prerequisites

- Python 3.6 or later
- `pip` (Python package installer)

### Steps

1. Clone the repository:

    ```sh
    git clone https://github.com/bsandvik/slack_archive_reader.git
    cd slack_archive_reader
    ```

2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Install the package:

    ```sh
    python setup.py install
    ```

## Usage

### Basic Commands

- **List Users**

    ```sh
    slack-archive-reader --list-users -f path/to/your/slack-archive.json
    ```

- **Search Messages**

    ```sh
    slack-archive-reader -f path/to/your/slack-archive.json -u username
    ```

- **Display Threads**

    ```sh
    slack-archive-reader -f path/to/your/slack-archive.json --expanded
    ```

### Command-line Options

- `-f, --file`: Path to the Slack JSON file (required)
- `-s, --start-time`: Start time for search (optional)
- `-e, --end-time`: End time for search (optional)
- `-m, --message`: Message ID (timestamp) to fetch (optional)
- `-t, --thread`: Thread ID (thread_ts) to fetch (optional)
- `-u, --user`: Display messages from a specific user (optional)
- `--add-user`: Add or update user ID with real name (optional)
- `--list-users`: List all users in the database (optional)
- `--dump-users`: Dump all user IDs from the file (optional)
- `--raw`: Bypass all formatting (optional)
- `--expanded`: Display expanded thread messages (optional)

## Examples

### List All Users

```sh
slack-archive-reader --list-users -f /path-to/your-slack-archive.json
```

### Search for Messages by a Specific User
```sh
slack-archive-reader -f /path/to/your-slack-archive.json -u username
```

Display Messages with Threads Expanded
```sh
slack-archive-reader -f /path/to/your-slack-archive.json --expanded
```

### Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas. This is an early release, and there are several features that would be needed to make this more versatile.

### Acknowledgments

Thanks to (https://www.openai.com|OpenAI) for providing assistance in developing this tool.
