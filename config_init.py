# config_init.py is a snippet that initializes the config directory and config.json file if they do not exist. This snippet is useful for ensuring that the configuration directory and file are present before writing or reading configuration data. The snippet defines a function ensure_config() that creates the config directory and config.json file if they do not exist. The snippet can be used in scripts that require configuration data to ensure that the necessary configuration files are available.

import os
import json

CONFIG_DIR = 'config'
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

def ensure_config():
    # If config dir doesnt exist, create it
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        print("Created config directory.")
    
    # If config.json file doesnt exist, create it within config dir
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({}, f, indent=4)  # Create an empty JSON object
        print("Created config.json file. Path: config/config.json")
