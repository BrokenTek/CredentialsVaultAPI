# For encrypting and decrypting passwords in the sqlite3 db file

import json
from cryptography.fernet import Fernet

CONFIG_FILE = 'config/config.json'

def keygen():
    return Fernet.generate_key()

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)
    
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def write_key():
    config = load_config()
    if "cred_key" not in config or not config['cred_key']:
        config['cred_key'] = keygen()
        save_config(config)
        # return False
    # print("Failed to write key. Key already exists.")
    # return True
    
def load_key():
    config = load_config()
    if "cred_key" in config and config['cred_key']:
        return config['cred_key'].encode()
    print("Failed to load key. Key not found.")

# Persistent key
try:
    key = load_key()
    cipher_suite = Fernet(key)
except TypeError as e:
    print(f"Error loading key: {e}")

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password.encode()).decode()


conf = load_config()
print(conf['cred_key'].encode())

if "cred_key" not in conf or not conf['cred_key']:
    print("No key")
else:
    print("Key exists")
    