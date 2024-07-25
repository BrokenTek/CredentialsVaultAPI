# For encrypting and decrypting passwords in the sqlite3 db file

import os
import json
from cryptography.fernet import Fernet

CONFIG_DIR = 'config/'
CONFIG_FILE = 'config.json'
CONFIG_PATH = CONFIG_DIR + CONFIG_FILE

def keygen():
    return Fernet.generate_key()

def is_file_empty(file_path):
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
    return os.path.exists(file_path)

def isConfigFile(file_path):
    return os.path.isfile(file_path)
        
def get_or_gen_key():
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
    