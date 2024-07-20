# This script is used to interact with the credentials vault Flask API. It has the following functionalities:
# (1) Functions for user authentication credential storage (for accessing the API) - /users
# (2) Functions for credentials storage setting and retrieval - /creds

'''
    - The User class is used to store user authentication credentials, while the Credential class is used to store the credentials for various services. The API also includes functionality to verify user credentials for API access and add new users.
    - The script uses the Flask-SQLAlchemy extension to interact with a SQLite database to store the user and credential information. It also uses the Flask-HTTPAuth extension for user authentication.
    - The script initializes the database and defines routes for adding new users and verifying user credentials for API access.
    - Overall, this script provides a secure way to manage user authentication and credentials for accessing the API. It ensures that only authorized users can access the API and manage credentials securely.
'''

import json
import requests
from requests.auth import HTTPBasicAuth

# API endpoints     
BASE_URL = 'http://127.0.0.1:5000'
USERS_URL = f"{BASE_URL}/users"
CREDENTIALS_URL = f"{BASE_URL}/creds"

# Grab credentials for user authentication
def load_credentials(config_file='config/config.json'):
    with open(config_file) as f:
        config = json.load(f)
    return config['username'], config['password']

# AUTH USERS INTERACTION
# Check if auth user exists by username
def check_user_exists(username, auth_username, auth_password):
    try:
        response = requests.get(f"{USERS_URL}/{username}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        print(f"GET /users/{username} response: ")
        print(json.dumps(result, indent=4))
    except requests.RequestException as e:
        print(f"Error checking user exists: {e}")

# Add new auth user
def add_user(username, email, password, auth_username, auth_password):
    try:
        headers = {'Content-Type': 'application/json'}
        post_user_data = {'username': username, 'email': email, 'password': password}
        response = requests.post(f"{USERS_URL}", headers=headers, data=json.dumps(post_user_data), auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        print('POST /users response: ')
        print(json.dumps(result, indent=4))
    except requests.RequestException as e:
        print(f"Error adding user: {e}")

# Delete existing auth user
def delete_user(username, auth_username, auth_password):
    try:
        response = requests.delete(f"{USERS_URL}/{username}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        print('DELETE /users response: ')
        print(json.dumps(result, indent=4))
    except requests.RequestException as e:
        print(f"Error deleting user: {e}")
        
# Get all existing auth usernames
def get_users(auth_username, auth_password):
    try:
        response = requests.get(f"{USERS_URL}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        print('GET /users response: ')
        print(json.dumps(result, indent=4))
    except requests.RequestException as e:
        print(f"Error getting users: {e}")
        
# Change auth user password by username
def change_user_password(username, new_password, auth_username, auth_password):
    try:
        headers = {'Content-Type': 'application/json'}
        put_user_data = {'password': new_password}
        response = requests.put(f"{USERS_URL}/{username}", headers=headers, data=json.dumps(put_user_data), auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        print('PUT /users response: ')
        print(json.dumps(result, indent=4))
    except requests.RequestException as e:
        print(f"Error changing user password: {e}")



# CREDENTIALS INTERACTION












def main():
    # Get user auth creds
    username, password = load_credentials()
    
    ## Tests
    # add_user('testuser', 'testmail@gmail.com', 'testpassword', username, password)
    # change_user_password('testuser', 'newtestpassword', username, password)
    get_users(username, password)
    print()
    check_user_exists('testuser', username, password)
    # get_users(username, password)
    # delete_user('testuser', username, password)
    
if __name__=='__main__':
    main()

