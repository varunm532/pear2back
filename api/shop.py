from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Allow requests from all origins

# Route for purchasing ingredients
@app.route('/purchase-ingredient', methods=['POST'])
def purchase_ingredient():
    data = request.json
    ingredient = data.get('ingredient')
    quantity = data.get('quantity', 1)  # Default quantity is 1 if not provided
    # Validate data
    if not ingredient:
        return jsonify({'error': 'Invalid ingredient'}), 400

    # Purchase the ingredient
    try:
        connection = sqlite3.connect('ingredients.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM purchased_ingredients WHERE ingredient = ?', (ingredient,))
        existing_ingredient = cursor.fetchone()

        if existing_ingredient:
            # If the ingredient exists, update the quantity
            new_quantity = existing_ingredient[2] + quantity
            cursor.execute('UPDATE purchased_ingredients SET quantity = ? WHERE ingredient = ?', (new_quantity, ingredient))
        else:
            # If the ingredient is new, insert it into the table
            cursor.execute('INSERT INTO purchased_ingredients (ingredient, quantity) VALUES (?, ?)', (ingredient, quantity))

        connection.commit()
        connection.close()

        return jsonify({'message': f'You have purchased {quantity} {ingredient}(s).'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for retrieving purchased ingredients
@app.route('/purchased-ingredients', methods=['GET'])
def get_purchased_ingredients():
    try:
        connection = sqlite3.connect('sqlite.db')
        cursor = connection.cursor()
        cursor.execute('SELECT ingredient, quantity FROM purchased_ingredients')
        purchased_ingredients = cursor.fetchall()
        connection.close()
        ingredients_data = [{'ingredient': ingredient, 'quantity': quantity} for ingredient, quantity in purchased_ingredients]
        return jsonify(ingredients_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8028)