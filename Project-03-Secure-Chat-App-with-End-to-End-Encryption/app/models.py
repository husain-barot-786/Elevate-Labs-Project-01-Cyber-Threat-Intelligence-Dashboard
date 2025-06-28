# In-memory store only for demo; use DB in production!
users = {}  # username -> {'public_key': str, 'sid': str}

def register_user(username, public_key, sid):
    users[username] = {
        'public_key': public_key,
        'sid': sid
    }

def get_public_key(username):
    return users[username]['public_key']

def get_sid(username):
    return users[username]['sid']

def get_all_users():
    return list(users.keys())

def remove_user_by_sid(sid):
    to_remove = [u for u, v in users.items() if v['sid'] == sid]
    for u in to_remove:
        del users[u]
        return u