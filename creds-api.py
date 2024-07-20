# Simple Python API for local use to retrieve credentials from an sqlite3 database - json output
# Usage: python creds-api.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# AUTH
# (1) Class for user authentication credential storage (for accessing the API)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Password setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    # Password hash comparison (for auth)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"User(username={self.username})"

# FUNCTIONALITY
# (2) Class for credentials storage
class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    service = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Credential(username={self.username}, password={self.password}, service={self.service})"



# Init the database only once
with app.app_context():
    db.create_all()



# AUTH API FUNCTIONALITY
# Verify user creds for API access
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    
# Add new user
@app.route('/users', methods=['POST'])
@auth.login_required
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "New user added successfully!"}), 201

# Get all users
@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    users = User.query.all()
    users_list = [{"id":user.id, "username":user.username, "email":user.email} for user in users]
    return jsonify(users_list)

# # Get user email by username
# @app.route('/users/<string:username>', methods=['GET'])
# @app.login_required
# def get_email(username):
#     user = User.query.filter_by(username=username).first()
#     if user:
#         return jsonify({"username":user.username, "email":user.email})
    
# Update auth user password
@app.route('/users/<string:username>', methods=['PUT'])
@auth.login_required
def update_user_password(username):
    user = User.query.filter_by(username=username).first()
    if user:
        data = request.get_json()
        user.set_password(data['password'])
        db.session.commit()
        return jsonify({"message": "User updated successfully!"})
    return jsonify({"message": "User not found!"}), 404

# Delete user by username
@app.route('/users/<string:username>', methods=['DELETE'])
@auth.login_required
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"})
    return jsonify({"message": "User not found!"}), 404


# CREDENTIAL API FUNCTIONALITY
# Add new credential
@app.route('/creds', methods=['POST'])
@auth.login_required
def add_cred():
    data = request.get_json()
    new_cred = Credential(username=data['username'], password=data['password'], service=data['service'])
    db.session.add(new_cred)
    db.session.commit()
    return jsonify({'message': "New credential added successfully!"}), 201

# Get all credentials
@app.route('/creds', methods=['GET'])
@auth.login_required
def get_creds():
    creds = Credential.query.all()
    creds_list = [{"id":cred.id, "username":cred.username, "password":cred.password, "service":cred.service} for cred in creds]
    return jsonify(creds_list)

# TODO - Next methods different than convention learned **********************************************************************************************
# Get credential by service
@app.route('/creds/<string:service>', methods=['GET'])
@auth.login_required
def get_cred(service):
    cred = Credential.query.filter_by(service=service).first()
    if cred:
        return jsonify({"id":cred.id, "username":cred.username, "password":cred.password, "service":cred.service})
    return jsonify({"message": "Credential not found!"}), 404

# Update credential defined by service
@app.route('/creds/<string:service>', methods=['PUT'])
@auth.login_required
def update_cred(service):
    cred = Credential.query.filter_by(service=service).first()
    if cred:
        data = request.get_json()
        cred.username = data['username']
        cred.password = data['password']
        db.session.commit()
        return jsonify({"message": "Credential updated successfully!"})
    return jsonify({"message": "Credential not found!"}), 404

# Delete credential defined by service
@app.route('/creds/<string:service>', methods=['DELETE'])
@auth.login_required
def delete_cred(service):
    cred = Credential.query.filter_by(service=service).first()
    if cred:
        db.session.delete(cred)
        db.session.commit()
        return jsonify({"message": "Credential deleted successfully!"})
    return jsonify({"message": "Credential not found!"}), 404

# Get all services
@app.route('/services', methods=['GET'])
@auth.login_required
def get_services():
    creds = Credential.query.all()
    services = list(set([cred.service for cred in creds]))
    return jsonify(services)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')


