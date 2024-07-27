'''
    - The User class (authusers.py  <this file>) is used to store user authentication credentials (security for accessing the functionality), while the Credential class (credentials.py) is used to store the credentials for various services (the core functionality). The API also includes functionality to verify user credentials for API access and add new users.
    - The script uses the Flask-SQLAlchemy extension to interact with a SQLite database to store the user and credential information. It also uses the Flask-HTTPAuth extension for user authentication.
    - The script initializes the database and defines routes for adding new users and verifying user authentication credentials. It also defines routes for adding and deleting auth credentials for API access.
    - Overall, this script provides a secure way to manage user authentication for the API. It ensures that only authorized users can access the API and manage credentials securely.
'''

# TODO: Add more error handling and input validation


import json
import requests
from requests.auth import HTTPBasicAuth

# API Endpoints/Constants
BASE_URL = 'http://127.0.0.1:5000'    # For running locally on same physical machine. tmux is suggested for testing and usage!!
USERS_URL = f"{BASE_URL}/users"

def load_config(config_file='config/config.json'):
    """
    Load config authentication credentials from a JSON configuration file.

    Args:
        config_file (str, optional): The path to the configuration file. Defaults to 'config/config.json'.

    Returns:
        tuple: A tuple containing the username and password loaded from the configuration file.
    """
    with open(config_file) as f:
        config = json.load(f)
    return config['username'], config['password']

# AUTH USERS INTERACTION
def check_user_exists(username, auth_username, auth_password):
    """
    Check if a user exists by sending a GET request to the API endpoint for checking user existence.

    Parameters:
        username (str): The username of the user to check.
        auth_username (str): The username for authentication.
        auth_password (str): The password for authentication.

    Returns:
        bool: True if the user exists, False otherwise.

    Raises:
        requests.RequestException: If there is an error with the request.
    """
    try:
        response = requests.get(f"{USERS_URL}/{username}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        if result['message'] == "True":
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error checking user exists: {e}")

# Add new auth user
def add_user(username, email, password, auth_username, auth_password):
    """
    Adds a new user to the system.

    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
        auth_username (str): The username for authentication.
        auth_password (str): The password for authentication.

    Returns:
        dict: The response from the API containing the result of the user creation.

    Raises:
        requests.RequestException: If there is an error with the request.
    """
    if check_user_exists(username, auth_username, auth_password):
        print(f"User '{username}' already exists.")
        return
    try:
        headers = {'Content-Type': 'application/json'}
        post_user_data = {'username': username, 'email': email, 'password': password}
        response = requests.post(f"{USERS_URL}", headers=headers, data=json.dumps(post_user_data), auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error adding user: {e}")

# Delete existing auth user
def delete_user(username, auth_username, auth_password):
    """
    Deletes a user from the system.

    Args:
        username (str): The username of the user to delete.
        auth_username (str): The username for authentication.
        auth_password (str): The password for authentication.

    Returns:
        dict: The response from the API containing the result of the user deletion.
            If the user does not exist, returns None.

    Raises:
        requests.RequestException: If there is an error with the request.
    """   
    if not check_user_exists(username, auth_username, auth_password):
        print(f"User '{username}' does not exist.")
        return
    try:
        response = requests.delete(f"{USERS_URL}/{username}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error deleting user: {e}")
        
# Get all existing auth usernames, emails, indexed by auto-incrementing primary key
def get_users(auth_username, auth_password):
    """
    Retrieves a list of users from the API.

    Args:
        auth_username (str): The username for authentication.
        auth_password (str): The password for authentication.

    Returns:
        dict: The response from the API containing the list of users.

    Raises:
        requests.RequestException: If there is an error with the request.
    """
    try:
        response = requests.get(f"{USERS_URL}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error getting users: {e}")
        
# Change auth user password by username
def change_user_password(username, new_password, auth_username, auth_password):
    """
    Change the password of a user.

    Args:
        username (str): The username of the user.
        new_password (str): The new password for the user.
        auth_username (str): The username for authentication.
        auth_password (str): The password for authentication.

    Returns:
        dict: The response from the API containing the result of the password change.
            If the user does not exist, returns None.

    Raises:
        requests.RequestException: If there is an error with the request.
    """
    if not check_user_exists(username, auth_username, auth_password):
        print(f"User '{username}' does not exist.")
        return
    try:
        headers = {'Content-Type': 'application/json'}
        put_user_data = {'password': new_password}
        response = requests.put(f"{USERS_URL}/{username}", headers=headers, data=json.dumps(put_user_data), auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error changing user password: {e}")
