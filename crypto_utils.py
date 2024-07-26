# For encrypting and decrypting passwords in the sqlite3 db file

import os
import json
from cryptography.fernet import Fernet

CONFIG_DIR = 'config/'
CONFIG_FILE = 'config.json'
CONFIG_PATH = CONFIG_DIR + CONFIG_FILE

def keygen():
    """
    Generates a new encryption key using the Fernet library.

    Returns:
        bytes: A randomly generated encryption key.
    """
    return Fernet.generate_key()

def is_file_empty(file_path):
    """
    Checks if a file is empty or not.

    Args:
        file_path (str): The path to the file to be checked.

    Returns:
        bool: True if the file is empty, False otherwise.

    Raises:
        FileNotFoundError: If the file specified by file_path does not exist.
        json.JSONDecodeError: If the file is not a valid JSON file.
    """
    with open(file_path, 'r') as f:
        try:
            # load json data
            data = json.load(f)
            # check if data is empty
            return not bool(data) # evals to true if empty
        except json.JSONDecodeError:
            # consider the file to be empty
            return True
        
def isConfigDir(file_path):
    """
    Checks if a directory exists at the given file path.

    Args:
        file_path (str): The path to the directory to check.

    Returns:
        bool: True if the directory exists, False otherwise.
    """
    return os.path.exists(file_path)

def isConfigFile(file_path):
    """
    Checks if a file exists at the given file path.

    Args:
        file_path (str): The path to the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(file_path)
        
def get_or_gen_key():
    """
    Retrieves or generates a key for encryption and decryption of credential passwords.

    This function checks if the configuration directory exists and creates it if it doesn't.
    It also checks if the configuration file exists and creates it if it doesn't.
    If the configuration file is empty, it initializes it with an empty JSON object.

    The function then loads the configuration file and checks if the 'cred_key' key exists and is not empty.
    If the key is missing or empty, it generates a new key using the keygen function and adds it to the configuration file.
    The new key is then returned.

    If the key is already present in the configuration file, it is returned.

    Returns:
        str: The generated or retrieved key for encryption and decryption.

    Raises:
        None

    Prints:
        str: A message indicating the creation of the configuration directory or file.
    """
    # if not os.path.exists(CONFIG_FILE):
    if not isConfigDir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        print(f"Created directory: {CONFIG_DIR}")
        
    if not isConfigFile(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            json.dump({}, f, indent=4)
            print(f"Created file: {CONFIG_FILE}")
    
    if is_file_empty(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            json.dump({}, f, indent=4) 
        
    # Load config
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    
    if 'cred_key' not in config or not config['cred_key']:  
        # Append to config
        key = keygen().decode()
        config['cred_key'] = key
        
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
            
        return key
    
    else:
        return config['cred_key']
    