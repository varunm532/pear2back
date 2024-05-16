from flask import Flask, request, jsonify
from flask import Blueprint
from flask_restful import Api, Resource
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

house_price_api = Blueprint('house_price_api', __name__, url_prefix='/api/house_price')
api = Api(house_price_api)

class HousePriceAPI(Resource):
    def __init__(self):
        # Load the dataset
        data = pd.read_csv('house_prices.csv')
        
        # Preprocessing and feature selection/engineering
        # Remove the 'furnishingstatus' column
        X = data.drop(['price', 'furnishingstatus'], axis=1)
        y = data['price']
        
        # Train the model     
        # trains the model according to linear regression
        # the model will be trained to predict healtime based on the other categories

        self.model = LinearRegression()
        self.model.fit(X, y)

    def preprocess_inputs(self, area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea):
        # Convert 'yes' or 'no' inputs to 1 or 0
        mainroad = 1 if mainroad.lower() == 'yes' else 0
        guestroom = 1 if guestroom.lower() == 'yes' else 0
        basement = 1 if basement.lower() == 'yes' else 0
        hotwaterheating = 1 if hotwaterheating.lower() == 'yes' else 0
        airconditioning = 1 if airconditioning.lower() == 'yes' else 0
        parking = 1 if parking.lower() == 'yes' else 0
        prefarea = 1 if prefarea.lower() == 'yes' else 0
        
        return area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea

    def predict_house_price(self, area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea):
        # Prepare input data
        input_data = pd.DataFrame({
            'area': [area],
            'bedrooms': [bedrooms],
            'bathrooms': [bathrooms],
            'stories': [stories],
            'mainroad': [mainroad],
            'guestroom': [guestroom],
            'basement': [basement],
            'hotwaterheating': [hotwaterheating],
            'airconditioning': [airconditioning],
            'parking': [parking],
            'prefarea': [prefarea]
        })
        
        # Make prediction
        predicted_price = self.model.predict(input_data)
        return predicted_price[0]

    def post(self):
        try:
            # Get data from request
            data = request.json
            # Extract features
            area = data['area']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            stories = data['stories']
            mainroad = data['mainroad']
            guestroom = data['guestroom']
            basement = data['basement']
            hotwaterheating = data['hotwaterheating']
            airconditioning = data['airconditioning']
            parking = data['parking']
            prefarea = data['prefarea']
            # Preprocess inputs
            area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea = self.preprocess_inputs(area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea)
            # Predict house price
            predicted_price = self.predict_house_price(area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea)
            predicted_price = predicted_price/10
            predicted_price = round(predicted_price, 2)

            return jsonify({'predicted_price': predicted_price })
        except Exception as e:
            return jsonify({'error': str(e)})

api.add_resource(HousePriceAPI, '/predict')


