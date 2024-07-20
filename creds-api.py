# Simple Python API for local use to retrieve credentials from an sqlite3 database - json output
# Usage: python creds-api.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

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

# Add new credential
@app.route('/creds', methods=['POST'])
def add_cred():
    data = request.get_json()
    new_cred = Credential(username=data['username'], password=data['password'], service=data['service'])
    db.session.add(new_cred)
    db.session.commit()
    return jsonify({'message': "New credential added successfully!"}), 201

# Get all credentials
@app.route('/creds', methods=['GET'])
def get_creds():
    creds = Credential.query.all()
    creds_list = [{"id":cred.id, "username":cred.username, "password":cred.password, "service":cred.service} for cred in creds]
    return jsonify(creds_list)

# TODO - Next methods different than convention learned **********************************************************************************************
# Get credential by service
@app.route('/creds/<string:service>', methods=['GET'])
def get_cred(service):
    cred = Credential.query.filter_by(service=service).first()
    if cred:
        return jsonify({"id":cred.id, "username":cred.username, "password":cred.password, "service":cred.service})
    return jsonify({"message": "Credential not found!"}), 404

# Update credential defined by service
@app.route('/creds/<string:service>', methods=['PUT'])
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
def delete_cred(service):
    cred = Credential.query.filter_by(service=service).first()
    if cred:
        db.session.delete(cred)
        db.session.commit()
        return jsonify({"message": "Credential deleted successfully!"})
    return jsonify({"message": "Credential not found!"}), 404

# Get all services
@app.route('/services', methods=['GET'])
def get_services():
    creds = Credential.query.all()
    services = list(set([cred.service for cred in creds]))
    return jsonify(services)

if __name__ == '__main__':
    app.run(debug=False)


