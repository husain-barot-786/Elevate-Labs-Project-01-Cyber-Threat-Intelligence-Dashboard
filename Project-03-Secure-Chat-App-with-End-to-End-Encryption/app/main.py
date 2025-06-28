import eventlet
eventlet.monkey_patch()

from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from app.models import register_user, get_public_key, get_sid, get_all_users, remove_user_by_sid
from app.chat_logs import log_message, read_logs

import os

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

app = Flask(__name__, static_folder=STATIC_DIR)
socketio = SocketIO(app, cors_allowed_origins="*")

online_users = set()
groups = {} # group_name -> set(usernames)

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/logs")
def logs():
    # Decrypt and return logs
    return "<br>".join(read_logs())

@socketio.on("register")
def handle_register(data):
    username = data.get("username", "").strip()
    public_key = data.get("publicKey")
    if not username or not public_key:
        emit("register_error", {"error": "Invalid registration data"})
        return
    register_user(username, public_key, request.sid)
    online_users.add(username)
    users = get_all_users()
    user_keys = {u: get_public_key(u) for u in users}
    emit("public_keys", user_keys, broadcast=True)
    emit_user_status()

def emit_user_status():
    all_users = get_all_users()
    emit("user_status", {"online": list(online_users), "all_users": all_users}, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    user_sid = request.sid
    removed = remove_user_by_sid(user_sid)
    if removed:
        online_users.discard(removed)
    users = get_all_users()
    user_keys = {u: get_public_key(u) for u in users}
    emit("public_keys", user_keys, broadcast=True)
    emit_user_status()

@socketio.on("send_message")
def handle_send_message(data):
    sender = data.get("sender", "").strip()
    recipient = data.get("recipient", "").strip()
    ciphertext = data.get("ciphertext")
    if not sender or not recipient or not ciphertext:
        emit("message_error", {"error": "Invalid message data"})
        return
    log_message(sender, recipient, ciphertext)
    recipient_sid = get_sid(recipient) if recipient else None
    if recipient_sid:
        emit("receive_message", {
            "sender": sender,
            "recipient": recipient,
            "ciphertext": ciphertext
        }, room=recipient_sid)
    sender_sid = get_sid(sender) if sender else None
    if sender_sid and sender_sid != recipient_sid:
        emit("receive_message", {
            "sender": sender,
            "recipient": recipient,
            "ciphertext": ciphertext
        }, room=sender_sid)

# --- GROUP SUPPORT ---
@socketio.on("create_group")
def handle_create_group(data):
    group = data.get("group")
    members = data.get("members", [])
    if not group or not members:
        return
    groups[group] = set(members)
    for m in members:
        sid = get_sid(m)
        if sid:
            join_room(group, sid=sid)
            emit("group_created", {"group": group, "members": members}, room=sid)

@socketio.on("send_group_key")
def handle_send_group_key(data):
    group = data.get("group")
    to = data.get("to")
    encKey = data.get("encKey")
    from_user = None
    for uname, v in get_all_user_data().items():
        if v['sid'] == request.sid:
            from_user = uname
    sid = get_sid(to)
    if sid:
        emit("receive_group_key", {"group": group, "encKey": encKey, "from": from_user}, room=sid)

def get_all_user_data():
    from app.models import users
    return users

@socketio.on("send_group_message")
def handle_send_group_message(data):
    group = data.get("group")
    sender = data.get("sender")
    ciphertext = data.get("ciphertext")
    if group not in groups or not sender or not ciphertext:
        return
    # broadcast to all in group EXCEPT the sender
    for m in groups[group]:
        if m == sender:
            continue
        sid = get_sid(m)
        if sid:
            emit("receive_group_message", {"group": group, "sender": sender, "ciphertext": ciphertext}, room=sid)
    # Log the group message (encrypted)
    log_message(sender, f"group:{group}", ciphertext)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)