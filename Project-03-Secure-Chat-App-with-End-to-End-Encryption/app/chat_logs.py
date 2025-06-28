import os
from app.encryption import encrypt_aes, decrypt_aes, generate_aes_key

LOG_FILE = "chat_logs.enc"

# AES key for log encryption - should be kept secure in production!
# Here we use an environment variable or generate one if not set.
LOG_AES_KEY_ENV = "LOG_AES_KEY"
if os.environ.get(LOG_AES_KEY_ENV):
    LOG_AES_KEY = bytes.fromhex(os.environ[LOG_AES_KEY_ENV])
else:
    LOG_AES_KEY = generate_aes_key()
    os.environ[LOG_AES_KEY_ENV] = LOG_AES_KEY.hex()

def log_message(sender, recipient, ciphertext):
    entry = f"{sender}->{recipient}:{ciphertext}".encode('utf-8')
    enc_entry = encrypt_aes(LOG_AES_KEY, entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(enc_entry + "\n")

def read_logs():
    if not os.path.exists(LOG_FILE):
        return []
    logs = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = decrypt_aes(LOG_AES_KEY, line.strip())
                logs.append(entry.decode('utf-8'))
            except Exception:
                continue
    return logs