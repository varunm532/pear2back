from flask import Blueprint, request
from flask_restful import Api, Resource
import base64
from model.users import User
from werkzeug.security import check_password_hash
from __init__ import db

settings_api = Blueprint('settings_api', __name__, url_prefix='/api/settings')
api = Api(settings_api)

class ChangeUsername(Resource):
    def put(self):
        body = request.get_json()
        current_name = body.get('_name')
        user_uid = body.get('_uid')
        password = body.get('_password')
        new_name = body.get('new_name')
        if not all([current_name, user_uid, password, new_name]):
            return {'message': 'All fields are required'}, 400
        user = User.query.filter_by(_uid=user_uid).first()
        if user and user._name == current_name and check_password_hash(user._password, password):
            user._name = new_name
            db.session.commit()
            return {'message': 'Name updated successfully'}, 200
        else:
            return {'message': 'Invalid credentials or user not found'}, 404

class ChangeUID(Resource):
    def put(self):
        body = request.get_json()
        current_name = body.get('_name')
        user_uid = body.get('_uid')
        password = body.get('_password')
        new_uid = body.get('new_uid')
        if not all([current_name, user_uid, password, new_uid]):
            return {'message': 'All fields are required'}, 400
        user = User.query.filter_by(_uid=user_uid).first()
        if user and user._name == current_name and check_password_hash(user._password, password):
            user._uid = new_uid
            db.session.commit()
            return {'message': 'User ID updated successfully'}, 200
        else:
            return {'message': 'Invalid credentials or user not found'}, 404

class UploadProfilePicture(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400
        user_uid = request.form.get('uid')
        user = User.query.filter_by(_uid=user_uid).first()
        if user:
            img_data = file.read()
            base64_encoded = base64.b64encode(img_data).decode('utf-8')
            user._pfp = base64_encoded
            db.session.commit()
            return {'message': 'Profile picture updated successfully'}, 200
        else:
            return {'message': 'User not found'}, 404

api.add_resource(ChangeUsername, '/change-name')
api.add_resource(ChangeUID, '/change-uid')
api.add_resource(UploadProfilePicture, '/profile-picture')
