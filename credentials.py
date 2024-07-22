'''
    - The Credential class (credentials.py) is used to store the credentials for various services. Uses api.py to interact with the /creds endpoint.
    - The script uses the Flask-SQLAlchemy extension to interact with a SQLite database to store credential information for different services.
    . Savable credential data: username, password, service, (auto-incrementing, unique 'id')    *Note: service means the name of the service that the credentials belong to. username could be email, username, etc.
'''

# TODO: Add more error handling and input validation
# TODO: Write Docstrings for each function

import json
import requests
from requests.auth import HTTPBasicAuth
from authusers import BASE_URL

# API Endpoints/Constants
BASE_URL = BASE_URL
CREDENTIALS_URL = f"{BASE_URL}/creds"
SERVICE_URL = f"{BASE_URL}/services"

# CREDENTIAL STORAGE INTERACTION
def check_service_exists(service, auth_username, auth_password):
    try:
        response = requests.get(f"{SERVICE_URL}/{service}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        if result['message'] == "True":
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error checking service exists: {e}")
        
def add_credential(service, username, password, auth_username, auth_password):
    if check_service_exists(service, auth_username, auth_password):
        print(f"Service '{service}' already exists.")
        return
    try:
        headers = {'Content-Type': 'application/json'}
        post_credential_data = {'username': username, 'password': password, 'service': service}
        response = requests.post(f"{CREDENTIALS_URL}", headers=headers, data=json.dumps(post_credential_data), auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error adding credential: {e}")
        
def delete_credential(service, auth_username, auth_password):
    if not check_service_exists(service, auth_username, auth_password):
        print(f"Service '{service}' does not exist.")
        return {"message": "Credential not found!"}
    try:
        response = requests.delete(f"{CREDENTIALS_URL}/{service}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error deleting credential: {e}")
        
def get_all_services(auth_username, auth_password):
    try:
        response = requests.get(f"{SERVICE_URL}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error getting all services: {e}")
        
def get_credential(service, auth_username, auth_password):
    if not check_service_exists(service, auth_username, auth_password):
        print(f"Service '{service}' does not exist.")
        return {"message": "Credential not found!"}
    try:
        response = requests.get(f"{CREDENTIALS_URL}/{service}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error getting credential by service: {e}")
        
def update_credential(service, username, password, auth_username, auth_password):
    if not check_service_exists(service, auth_username, auth_password):
        print(f"Service '{service}' does not exist.")
        return {"message": "Credential not found!"}
    try:
        headers = {'Content-Type': 'application/json'}
        data = {'username': username, 'password': password}
        response = requests.put(f"{CREDENTIALS_URL}/{service}", headers=headers, data=json.dumps(data), auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error updating credential: {e}")
    