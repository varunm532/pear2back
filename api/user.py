import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from werkzeug.security import check_password_hash
from auth_middleware import token_required

from model.users import User, db

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            password = body.get('password')
            dob = body.get('dob')
            favoritefood = body.get('favoritefood')
            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, 
                      uid=uid, favoritefood=favoritefood)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

    
        def get(self): # Read Method
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        
        @token_required(roles=["Admin","User"])
        def delete(self, current_user):
            body = request.get_json()
            uid = body.get('uid')
            users = User.query.all()
            
            for user in users:
                if user.uid == uid:
                    user.delete()
            return jsonify(user.read())

        def put(self):
            body = request.get_json() # get the body of the request
            uid = body.get('uid') # get the UID (Know what to reference)
            dob = body.get('dob')
            items = body.get('items')
            favoritefood = body.get('favoritefood')
            points = body.get('points')
            if dob is not None:
                try:
                    fdob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            users = User.query.all()
            for user in users:
                if user.uid == uid:
                    print(items)
                    user.update(uid,'','','','', items, points)
            return f"{user.read()} Updated"
    
    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')
                
                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400
                if user:
                    try:
                        token_payload = {
                            "_uid":user._uid,
                            "role": user.role
                        }
                        token = jwt.encode(
                            token_payload,
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None'  # This is the key part for cross-site requests

                                # domain="frontend.com"
                                )
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500
    
    class _Send(Resource):
        def post(self):
            body = request.get_json()
            uid = body.get('uid')
            item = body.get('items')
            users = User.query.all()
            for user in users:
                if user.uid == uid:
                    user.items = json.loads(user.items)
                    user.items.append(item)
                    user.items = json.dumps(user.items)
                    db.session.commit() 
                    return(f"you just gave {user.name} an item")

    class _Friendrq(Resource):
        def post(self):
            body = request.get_json()
            users = User.query.all()
            sender = body.get('sender')
            receiver = body.get('receiver')
            if sender == receiver:
                return {"message": "Cannot send friend request to yourself"}, 400
            for user in users:
                if user.uid == receiver:
                    user.friendrq = json.loads(user.friendrq)
                    if sender in user.friendrq:
                        return "Friend request already sent", 400
                    if sender in user.friends:
                        return "Already friends", 400
                    user.friendrq.append(sender)
                    user.friendrq = json.dumps(user.friendrq)
                    db.session.commit() 
                    return(f"You sent a friend request to {user.name}")
        def delete(self):
            body = request.get_json()
            action = body.get('action')
            sender = body.get('sender')
            receiver = body.get('receiver')
            users = User.query.all()
            for user in users:
                if user.uid == receiver:
                    user.friendrq = user.friendrq = json.loads(user.friendrq)
                    if sender not in user.friendrq:
                        return "Sender is not in the friend request list", 400
                    user.friendrq.remove(sender)
                    user.friendrq = json.dumps(user.friendrq)
                    db.session.commit()
                    if action == "accepted":
                        user.friends = json.loads(user.friends)
                        user.friends.append(sender)
                        user.friends = json.dumps(user.friends)
                        db.session.commit()
                        return(f"You accepted {sender}'s friend request")
                    else:
                        return(f"You denied {sender}'s friend request")
    
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Send, '/send')
    api.add_resource(_Friendrq, '/friendrq')