'''
    - The Credential class (credentials.py) is used to store the credentials for various services. Uses api.py to interact with the /creds endpoint.
    - The script uses the Flask-SQLAlchemy extension to interact with a SQLite database to store credential information for different services.
    . Savable credential data: username, password, service, (auto-incrementing, unique 'id')    *Note: service means the name of the service that the credentials belong to. username could be email, username, etc.
'''

# TODO: Add more error handling and input validation

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
    """
    Check if a service exists by sending a GET request to the API endpoint for checking service existence.

    Parameters:
        service (str): The name of the service to check.
        auth_username (str): The username for authentication.
        auth_password (str): The password for authentication.

    Returns:
        bool: True if the service exists, False otherwise.

    Raises:
        requests.RequestException: If there is an error with the request.
    """
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
    """
    Adds a new credential to the credentials storage.

    Parameters:
        service (str): The name of the service for which the credential is being added.
        username (str): The username for the credential.
        password (str): The password for the credential.
        auth_username (str): The username for authentication with the API.
        auth_password (str): The password for authentication with the API.

    Returns:
        dict: The JSON response from the API containing the result of the credential addition.

    Raises:
        requests.RequestException: If there is an error with the request.

    """
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
    """
    Deletes a credential for a given service using the provided authentication credentials.

    Parameters:
        service (str): The name of the service for which the credential needs to be deleted.
        auth_username (str): The username used for authentication.
        auth_password (str): The password used for authentication.

    Returns:
        dict: A dictionary containing the result of the delete operation.
            - If the service does not exist, it returns {"message": "Credential not found!"}.
            - If the delete operation is successful, it returns the response JSON.
            - If there is an error during the delete operation, it prints an error message and returns None.

    Raises:
        requests.exceptions.RequestException: If there is an error during the HTTP request.

    """
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
        
def get_services(auth_username, auth_password):
    """
    Retrieves a list of services from the API.

    Parameters:
        auth_username (str): The username for authentication.
        auth_password (str): The password for authentication.

    Returns:
        dict: The response from the API containing the list of services.

    Raises:
        requests.RequestException: If there is an error with the request.
    """
    try:
        response = requests.get(f"{SERVICE_URL}", auth=HTTPBasicAuth(auth_username, auth_password))
        response.raise_for_status()    # Raise exception for 4xx and 5xx status codes
        result = response.json()
        return result
    except requests.RequestException as e:
        print(f"Error getting all services: {e}")
        
def get_credential(service, auth_username, auth_password):
    """
    Retrieves a credential for a given service using the provided authentication credentials.

    Args:
        service (str): The name of the service for which to retrieve the credential.
        auth_username (str): The username for authentication.
        auth_password (str): The password for authentication.

    Returns:
        dict: A dictionary containing the retrieved credential information, or a dictionary with a "message" key
            indicating that the credential was not found.

    Raises:
        requests.RequestException: If there is an error making the HTTP request.

    Prints:
        str: An error message if the service does not exist or if there is an error getting the credential.
    """
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
    """
    Updates a credential for a given service using the provided authentication credentials.

    Args:
        service (str): The name of the service for which the credential needs to be updated.
        username (str): The new username for the credential.
        password (str): The new password for the credential.
        auth_username (str): The username used for authentication.
        auth_password (str): The password used for authentication.

    Returns:
        dict: A dictionary containing the result of the update operation.
            - If the service does not exist, it returns {"message": "Credential not found!"}.
            - If the update operation is successful, it returns the response JSON.
            - If there is an error during the update operation, it prints an error message and returns None.

    Raises:
        requests.exceptions.RequestException: If there is an error during the HTTP request.

    """
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
    