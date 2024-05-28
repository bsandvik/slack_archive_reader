import pickle
from pathlib import Path

user_db = {}

def load_user_db(db_path='slack_users.db'):
    global user_db
    db_file = Path(db_path)
    if db_file.exists():
        with open(db_file, 'rb') as db:
            user_db = pickle.load(db)
    else:
        user_db = {}

def save_user_db(db_path='slack_users.db'):
    global user_db
    db_file = Path(db_path)
    with open(db_file, 'wb') as db:
        pickle.dump(user_db, db)

def update_user(user_id: str, real_name: str, db_path='slack_users.db'):
    global user_db
    if user_id in user_db:
        user_db[user_id]['real_name'] = real_name
    else:
        user_db[user_id] = {'real_name': real_name}
    save_user_db(db_path)

def get_user_name(user_id: str):
    return user_db.get(user_id, {}).get('real_name', user_id)

def list_users():
    global user_db
    if not user_db:
        print("No users in the database.")
        return
    for user_id, user_info in user_db.items():
        print(f"User ID: {user_id}, Name: {user_info.get('real_name', 'Unknown')}")

def dump_users(data):
    user_ids = set()
    for message in data['messages']:
        if 'user' in message:
            user_ids.add(message['user'])
        if 'replies' in message:
            for reply in message['replies']:
                if 'user' in reply:
                    user_ids.add(reply['user'])
    print("\n".join(user_ids))
