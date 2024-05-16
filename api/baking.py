import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.bakings import Baking

baking_api = Blueprint('baking_api', __name__,
                   url_prefix='/api/baking')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(baking_api)

class BakingAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            recpie = body.get('recpie')
            uo = Baking(recpie=recpie)
        
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {recpie}, either a format error or User ID {recpie} is duplicate'}, 400
        def get(self): # Read Method
            users = Baking.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
 
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')