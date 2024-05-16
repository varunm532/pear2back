from auth_middleware import token_required
import jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from model.users import User
from __init__ import db, app
from werkzeug.security import check_password_hash,generate_password_hash


from flask import Blueprint

# Create a Blueprint for the paint API with a URL prefix
paint_api = Blueprint('paint_api', __name__, url_prefix='/api/paint_api')

# Create a RESTful API instance
api = Api(paint_api)

# Import Flask and Flask-RESTful modules again (redundant)
from flask import request, jsonify
from flask_restful import Api, Resource
from model.painting import Painting  # Import your model


# Define a Resource for uploading a painting
class UploadPainting(Resource):
    def post(self):
        # Retrieve JSON data from the request
        data = request.get_json()
        user_id = data.get('user_id')
        
        
        # Check if user ID is provided in the request
        if user_id is None:
            return jsonify({"error": "User ID is required in the request"})

        # Create a new Painting instance and add it to the database        
        painting = Painting(userID=User.query.filter_by(_uid=user_id).first().id, image=data["painting"])
        db.session.add(painting)
        db.session.commit()
        return "Success"

# Define a Resource for getting paintings
class GetPainting(Resource):
    def get(self):
        # Retrieve all paintings from the database
        paintings = Painting.query.all()
        imglist = []
        
        # Construct a list of dictionaries containing image data and associated usernames
        for img in paintings:
            imglist.append({
                'image': img.image,
                'username': User.query.get(img.userID).name
            })
            
        # Return JSON response containing the list of paintings        
        return jsonify({"paintings": imglist})

api.add_resource(UploadPainting, '/uploadPainting/')
api.add_resource(GetPainting,"/getPainting/")