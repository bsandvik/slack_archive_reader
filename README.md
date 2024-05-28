Slack JSON reader and search tool

usage: slack-archive-tool [-h] -f FILE [-s START_TIME] [-e END_TIME]
                          [-m MESSAGE] [-t THREAD] [-u USER]
                          [--add-user ADD_USER ADD_USER] [--list-users]
                          [--dump-users] [--raw] [--db DB] [--expanded]
                          [input]


positional arguments:
  input                 Search term for search

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Slack JSON file
  -s START_TIME, --start-time START_TIME
                        Start time for search (YYYY-MM-DD HH:MM:SS or YYYY-MM-
                        DD)
  -e END_TIME, --end-time END_TIME
                        End time for search (YYYY-MM-DD HH:MM:SS or YYYY-MM-
                        DD)
  -m MESSAGE, --message MESSAGE
                        Message ID (timestamp) to fetch
  -t THREAD, --thread THREAD
                        Thread ID (thread_ts) to fetch
  -u USER, --user USER  Display messages from a specific user
  --add-user ADD_USER ADD_USER
                        Add or update user ID with real name
  --list-users          List all users in the database
  --dump-users          Dump all user IDs from the file
  --raw                 Bypass all formatting
  --db DB               Path to the user database file
  --expanded            Show all messages from threads
