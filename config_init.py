# 

from crypto_utils import get_or_gen_key
from cryptography.fernet import Fernet

def init_key():
    # Persistent key
    try:
        key = get_or_gen_key()
        cipher_suite = Fernet(key)
        print(f"Key loaded successfully!")
        return cipher_suite
    except TypeError as e:
        print(f"Error loading key: {e}")
        return None
        

cipher_suite = init_key()

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password.encode()).decode()
