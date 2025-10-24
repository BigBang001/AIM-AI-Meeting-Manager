import json
from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def save_memory(memory, filename="journal.enc"):
    data = json.dumps(memory).encode()
    encrypted = cipher.encrypt(data)
    with open(filename, "wb") as f:
        f.write(encrypted)

def load_memory(filename="journal.enc"):
    try:
        with open(filename, "rb") as f:
            encrypted = f.read()
        data = cipher.decrypt(encrypted)
        return json.loads(data)
    except FileNotFoundError:
        return []