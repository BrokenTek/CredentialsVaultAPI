# Initialize newly created username and password for config/config.json if those values are missing. Checks at the start of api.py each time.

import os
import json

CONFIG_DIR = 'config/'
CONFIG_FILE = 'config.json'
CONFIG_PATH = CONFIG_DIR + CONFIG_FILE

# Will be changed to a graphical form in the future
def add_config_creds():
    """
    Reads the configuration file at `CONFIG_PATH` and checks if the 'username' and 'password' keys are present and not empty.
    If either of them is missing or empty, it prompts the user to enter the values and updates the configuration file.
    
    Parameters:
        None
    
    Returns:
        None
    """
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
        if 'username' not in config or not config['username']:
            config['username'] = input("Enter config username: ")
        if 'password' not in config or not config['password']:
            config['password'] = input("Enter config password: ")

    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
