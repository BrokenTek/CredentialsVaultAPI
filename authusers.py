'''
    - The User class (authusers.py * this file *) is used to store user authentication credentials, while the Credential class (credentials.py) is used to store the credentials for various services. The API also includes functionality to verify user credentials for API access and add new users.
    - The script uses the Flask-SQLAlchemy extension to interact with a SQLite database to store the user and credential information. It also uses the Flask-HTTPAuth extension for user authentication.
    - The script initializes the database and defines routes for adding new users and verifying user authentication credentials. It also defines routes for adding and deleting auth credentials for API access.
    - Overall, this script provides a secure way to manage user authentication for the API. It ensures that only authorized users can access the API and manage credentials securely.
'''

# TODO: Add more error handling and input validation
# TODO: Write Docstrings for each function


import json
import requests
from requests.auth import HTTPBasicAuth

# API Endpoints/Constants
BASE_URL = 'http://127.0.0.1:5000'    # For running locally. tmux is suggested for testing and usage!!
USERS_URL = f"{BASE_URL}/users"

def load_credentials(config_file='config/config.json'):
    with open(config_file) as f:
        config = json.load(f)
    return config['username'], config['password']

# AUTH USERS INTERACTION
def check_user_exists(username, auth_username, auth_password):
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
        
# Get all existing auth usernames, emails
def get_users(auth_username, auth_password):
    try:
        response = requests.get(f"{USERS_URL}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error getting users: {e}")
        
# Change auth user password by username
def change_user_password(username, new_password, auth_username, auth_password):
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
