'''
    - Simple Python API for retrieving credentials from an sqlite3 database - json output
    - Usage: python creds-api.py - Running locally will open a Flask server on port 5000, accessible on LAN by host machine local IP address
'''

# TODO: (1) Add more error handling and input validation
# TODO: (2) Find fix for running the script the first time (no users in db): Current workaround is to comment out the @app.login_required decorator for add_user > STARTED
# TODO: (3) Add logging

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import config_init as ci

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def set_password(self, password):
        """
        Retrieves a credential from the database based on the provided service name.

        This route handler handles the 'GET' request to '/services/{service}' endpoint. It requires the user to be authenticated using the `@auth.login_required` decorator.

        Parameters:
            service (str): The name of the service for which the credential is requested.

        Returns:
            - If a credential with the provided service name is found, a JSON response containing the message "True" is returned.
            - If no credential with the provided service name is found, a JSON response containing the message "False" is returned.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the given password matches the hashed password stored in the object.

        Parameters:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches the hashed password, False otherwise.
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """
        Returns a string representation of the User object with its username.

        :return: A string in the format "User(username={self.username})"
        :rtype: str
        """
        return f"User(username={self.username})"

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    service = db.Column(db.String(80), nullable=False)
    note = db.Column(db.String(200), nullable=True)

    def set_password(self, password):
        self.password = ci.encrypt_password(password)

    def get_password(self):
        return ci.decrypt_password(self.password)

    def __repr__(self):
        """
        Returns a string representation of the Credential object.

        :return: A string representation of the Credential object with its username, password, and service.
        :rtype: str
        """
        return f"Credential(username={self.username}, password={self.password}, service={self.service}, note={self.note})"


   
# TODO: (2) Add the initial user to users database table on first script run
# ADD INITIAL USER ON FIRST RUN   
db_path = os.path.join(app.instance_path, 'creds.db')
if not os.path.exists(db_path):
    # stub
    print("Creating initial user...")

    
    
# Initialize the database
with app.app_context():
    db.create_all()
 
@auth.verify_password
def verify_password(username, password):
    """
    Verify the provided username and password against the database.

    Args:
        username (str): The username to verify.
        password (str): The password to verify.

    Returns:
        User or None: The user object if the username and password are valid, None otherwise.
    """
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

@app.route('/users', methods=['POST'])
@auth.login_required
def add_user():
    """
    Adds a new user to the database.

    This function is a route handler for the '/users' endpoint with the 'POST' method.
    It requires the user to be authenticated using the `@auth.login_required` decorator.

    Parameters:
        None

    Returns:
        A JSON response with a message indicating the success of the user addition.
        The response has a status code of 201.
    """
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "New user added successfully!"}), 201

@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    """
    Retrieves a list of all users from the database.

    This function is a route handler for the '/users' endpoint with the 'GET' method.
    It requires the user to be authenticated using the `@auth.login_required` decorator.

    Returns:
        A JSON response containing a list of dictionaries, where each dictionary represents a user.
        Each dictionary contains the following keys:
        - 'id' (int): The unique identifier of the user.
        - 'username' (str): The username of the user.
        - 'email' (str): The email address of the user.
    """
    users = User.query.all()
    users_list = [{"id":user.id, "username":user.username, "email":user.email} for user in users]
    return jsonify(users_list)
    
@app.route('/users/<string:username>', methods=['PUT'])
@auth.login_required
def update_user_password(username):
    """
    Updates the password of a user identified by the provided username.

    Parameters:
        username (str): The username of the user whose password needs to be updated.

    Returns:
        A JSON response with a message indicating the success of the user update.
        If the user is not found, returns a JSON response with a 'User not found' message and a status code of 404.
    """
    user = User.query.filter_by(username=username).first()
    if user:
        data = request.get_json()
        user.set_password(data['password'])
        db.session.commit()
        return jsonify({"message": "User updated successfully!"})
    return jsonify({"message": "User not found!"}), 404

@app.route('/users/<string:username>', methods=['DELETE'])
@auth.login_required
def delete_user(username):
    """
    Deletes a user by the provided username.

    Parameters:
        username (str): The username of the user to be deleted.

    Returns:
        A JSON response with a message indicating the success of the user deletion.
        If the user is not found, returns a JSON response with a 'User not found' message and a status code of 404.
    """
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"})
    return jsonify({"message": "User not found!"}), 404

@app.route('/users/<string:username>', methods=['GET'])
@auth.login_required
def check_user(username):
    """
    Retrieves a user by the provided username and returns a JSON response indicating whether the user exists or not.
    Parameters:
        username (str): The username of the user to check.

    Returns:
        A JSON response containing a message 'True' if the user exists, 'False' otherwise.
    """
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "True"})
    return jsonify({"message": "False"})

@app.route('/creds', methods=['POST'])
@auth.login_required
def add_cred():
    """
    Add a new credential to the database.

    This route handler handles the 'POST' request to '/creds' endpoint. It requires the user to be authenticated using the `@auth.login_required` decorator.

    Parameters:
        None

    Returns:
        A JSON response with a message indicating the success of the credential addition.
        The response has a status code of 201.

    Raises:
        None
    """
    data = request.get_json()
    new_cred = Credential(username=data['username'], service=data['service'], note=data['note'])
    new_cred.set_password(data['password'])
    db.session.add(new_cred)
    db.session.commit()
    return jsonify({'message': "New credential added successfully!"}), 201

# NOT CURRENTLY USED. DUMPa ALL CREDS DATA. Not ideal.
# @app.route('/creds', methods=['GET'])
# @auth.login_required
# def get_creds():
#     """
#     Retrieves a list of credentials from the database.

#     This route handler handles the 'GET' request to '/creds' endpoint. It requires the user to be authenticated using the `@auth.login_required` decorator.

#     Parameters:
#         None

#     Returns:
#         A JSON response containing a list of dictionaries, where each dictionary represents a credential.
#         Each dictionary contains the following keys:
#         - 'id' (int): The unique identifier of the credential.
#         - 'username' (str): The username associated with the credential.
#         - 'password' (str): The password associated with the credential.
#         - 'service' (str): The service name for which the credential is used.
#     """
#     creds = Credential.query.all()
#     creds_list = [{"id":cred.id, "username":cred.username, "password":cred.get_password(), "service":cred.service} for cred in creds]
#     return jsonify(creds_list)

@app.route('/creds/<string:service>', methods=['GET'])
@auth.login_required
def get_cred(service):
    """
    Retrieves a credential from the database based on the provided service name.

    This route handler handles the 'GET' request to '/creds/{service}' endpoint. It requires the user to be authenticated using the `@auth.login_required` decorator.

    Parameters:
        service (str): The name of the service for which the credential is requested.

    Returns:
        - If a credential with the provided service name is found, a JSON response containing the credential details is returned.
          The response is a dictionary with the following keys:
          - 'id' (int): The unique identifier of the credential.
          - 'username' (str): The username associated with the credential.
          - 'password' (str): The password associated with the credential.
          - 'service' (str): The service name for which the credential is used.
        - If no credential with the provided service name is found, a JSON response with a message indicating that the credential was not found is returned.
          The response has a status code of 404.
    """
    cred = Credential.query.filter_by(service=service).first()
    if cred:
        return jsonify({"id":cred.id, "username":cred.username, "password":cred.get_password(), "service":cred.service, "note":cred.note})
    return jsonify({"message": "Credential not found!"}), 404

@app.route('/creds/<string:service>', methods=['PUT'])
@auth.login_required
def update_cred(service):
    """
    Updates a credential in the database based on the provided service name.

    Parameters:
        service (str): The name of the service for which the credential is to be updated.

    Returns:
        - If the credential is found and updated successfully, a JSON response with a 'Credential updated successfully!' message is returned.
        - If the credential is not found, a JSON response with a 'Credential not found!' message and a status code of 404 is returned.
    """
    cred = Credential.query.filter_by(service=service).first()
    if cred:
        data = request.get_json()
        cred.username = data['username']
        cred.set_password(data['password'])
        db.session.commit()
        return jsonify({"message": "Credential updated successfully!"})
    return jsonify({"message": "Credential not found!"}), 404

@app.route('/creds/<string:service>/note', methods=['PUT'])
@auth.login_required
def set_note(service):
    """
    Updates or adds the note of a credential in the database based on the provided service name.

    Parameters:
        service (str): The name of the service for which the credential is to be updated.

    Returns:
        - If the credential is found and the note is updated successfully, a JSON response with a 'Note updated successfully!' message is returned.
        - If the credential is not found, a JSON response with a 'Credential not found!' message and a status code of 404 is returned.
    """
    cred = Credential.query.filter_by(service=service).first()
    if cred:
        data = request.get_json()
        cred.note = data['note']
        db.session.commit()
        return jsonify({"message": "Note updated successfully!"})
    return jsonify({"message": "Credential not found!"}), 404

@app.route('/creds/<string:service>', methods=['DELETE'])
@auth.login_required
def delete_cred(service):
    """
    Deletes a credential from the database based on the provided service name.

    Parameters:
        service (str): The name of the service for which the credential is to be deleted.

    Returns:
        - If the credential is found and deleted successfully, a JSON response with a 'Credential deleted successfully!' message is returned.
        - If the credential is not found, a JSON response with a 'Credential not found!' message and a status code of 404 is returned.
    """
    cred = Credential.query.filter_by(service=service).first()
    if cred:
        db.session.delete(cred)
        db.session.commit()
        return jsonify({"message": "Credential deleted successfully!"})
    return jsonify({"message": "Credential not found!"}), 404

@app.route('/services', methods=['GET'])
@auth.login_required
def get_services():
    """
    Retrieves a list of unique services from the database and returns it as a JSON response.

    This route handler handles the 'GET' request to '/services' endpoint. It requires the user to be authenticated using the `@auth.login_required` decorator.

    Returns:
        A JSON response containing a list of unique services. Each service is represented as a string.
    """
    creds = Credential.query.all()
    services = list(set([cred.service for cred in creds]))
    return jsonify(services)

@app.route('/services/<string:service>', methods=['GET'])
@auth.login_required
def check_service(service):
    """
    Retrieves a credential from the database based on the provided service name.

    This route handler handles the 'GET' request to '/services/{service}' endpoint. It requires the user to be authenticated using the `@auth.login_required` decorator.

    Parameters:
        service (str): The name of the service for which the credential is requested.

    Returns:
        - If a credential with the provided service name is found, a JSON response containing the message "True" is returned.
        - If no credential with the provided service name is found, a JSON response containing the message "False" is returned.
    """
    service_exists = Credential.query.filter_by(service=service).first()
    if service_exists:
        return jsonify({"message": "True"})
    return jsonify({"message": "False"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')


