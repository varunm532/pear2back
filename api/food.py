from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pandas as pd
from model.foods import food
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from flask_restful import Resource
from flask import Blueprint, jsonify, request 
from flask_restful import Api, Resource

food_api = Blueprint('food_api', __name__, url_prefix='/api/food')
api = Api(food_api)

class PredictItem(Resource):
    
    def __init__(self):
        self.model = food()  
    def post(self):
        try:
            # get JSON data from the request
            payload = request.get_json()
            print(payload)
            foodModel = food.get_instance()
            # Predict the item purchased from bakery
            response = foodModel.predict(payload)
            print(response)
            
            return jsonify(response)

        except Exception as e:
            return jsonify({'error': str(e)})
        
api.add_resource(PredictItem, '/predict')