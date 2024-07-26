# Initialize the key for encryption and decryption of credential passwords. If the key is not found, a new key is generated.

from crypto_utils import get_or_gen_key
from session_user_auth import add_config_creds
from cryptography.fernet import Fernet

def init_key():
    """
    Initializes the key for encryption and decryption of credential passwords. If the key is not found, a new key is generated.

    Returns:
        cipher_suite (Fernet): The cipher suite object used for encryption and decryption.
        None: If there is an error loading the key.

    Raises:
        TypeError: If there is an error loading the key.

    Prints:
        Key loaded successfully!: If the key is loaded successfully.
        Error loading key: {e}: If there is an error loading the key.
    """
    try:
        key = get_or_gen_key()
        cipher_suite = Fernet(key)
        print(f"\nKey loaded successfully!\n")
        return cipher_suite
    except TypeError as e:
        print(f"Error loading key: {e}")
        return None
    
def init_config_creds():
    """
    Initializes the config credentials.

    Returns:
        None
    """
    try:
        add_config_creds()
    except TypeError as e:
        print(f"Error creating config creds: {e}")
        
# [super important comment, you're welcome] init cipher suite a variable: cipher_suite (Redundency? What does redundency mean? Redundancy is good according to Linus Tech Tips. Don't want to lose your data! Oh.. I see. Oh whale.)      
cipher_suite = init_key()

# [super important comment, you're welcome] create config creds (username, password) if they don't exist in config/config.json
add_config_creds()

def encrypt_password(password):
    """
    Encrypts a password using the cipher suite.

    Args:
        password (str): The password to be encrypted.

    Returns:
        str: The encrypted password.

    """
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    """
    Decrypts an encrypted password using the cipher suite.

    Args:
        encrypted_password (str): The encrypted password to be decrypted.

    Returns:
        str: The decrypted password.

    Raises:
        ValueError: If the encrypted password cannot be decrypted.
    """
    return cipher_suite.decrypt(encrypted_password.encode()).decode()
