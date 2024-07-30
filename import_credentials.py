# This file is used to load credentials from a JSON loader file that contains credential objects.

'''
JSON format: Incrementing key with credential object data attributes key:value pairs as value
[
    {
        "username": "username1",
        "password": "password1",
        "service": "service1",
        "note": "note1"
        },
    {
        "username": "username2",
        "password": "password2",
        "service": "service2",
        "note": "note2"
        }
]
'''

import json
from credentials import add_credential
from authusers import load_config
from crypto_utils import isFile

def load_credentials(file_path):
    """
    Load credentials from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing the credentials.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the credentials. Each dictionary contains the following keys:
            - 'username' (str): The username associated with the credential.
            - 'password' (str): The password associated with the credential.
            - 'service' (str): The service name for which the credential is used.

    Raises:
        None

    This function loads credentials from a JSON file and returns them as a list of dictionaries. It assumes that each object in the JSON file contains the following data attributes: 'username', 'password', and 'service'. If any of these attributes are missing, default values ('default_username', 'default_password') are used. If the file does not exist, a message is printed and None is returned.
    """
    if not isFile(file_path):
        print(f"File not found: {file_path}")
        return None
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    credentials = []
    
    try:
        # this assumes that each object contains all 3 data attributes (username, password, service)
        for obj in data:
            # credential = data[key]
            username = obj.get('username', 'default_username')
            password = obj.get('password', 'default_password')
            service = obj.get('service')
            note = obj.get('note', '')
            
            credentials.append({
                'username': username,
                'password': password,
                'service': service,
                'note': note
            })
    except:
        print(f"\nError parsing JSON file: {file_path}\nNo data imported.\n")

    return credentials

def write_credentials(credential_list, username, password):
    """
    Writes a list of credentials to the database.

    Args:
        credential_list (list): A list of dictionaries representing the credentials to be written. Each dictionary should have the following keys:
            - username (str): The username associated with the credential.
            - password (str): The password associated with the credential.
            - service (str): The service associated with the credential.
        username (str): The username of the user writing the credentials.
        password (str): The password of the user writing the credentials.

    Returns:
        bool: True if the credentials are written to the database successfully, False otherwise.
    """
    if credential_list is None:
        return False

    try:
        for credential in credential_list:
            add_credential(credential['service'], credential['username'], credential['password'], credential['note'], username, password)
        return True
    except:
        return False

def import_credentials(file_path):
    """
    Imports credentials from a file and writes them to a database.

    Args:
        file_path (str): The path to the file containing the credentials.

    Returns:
        None

    Raises:
        None
    """
    username, password = load_config()

    credentials = load_credentials(file_path)

    # write
    success = write_credentials(credentials, username, password)
    
    # feedback
    if success:
        print("\nCredentials written to database successfully!\n")
    else:
        print("\nError writing credentials to database.\n")
    