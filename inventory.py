from flask import Flask, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import json


app = Flask(__name__)

# Set the MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"

# Initialize PyMongo
mongo = PyMongo(app)

# Model class definition (from step 2)
class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"

@app.route("/insert_product")
def insert_product():
    # Create an instance of the Product class
    new_product = Product(name="Sample Product2", price=2.99, quantity=50)

    # Access the MongoDB collection
    db = mongo.db.products

    # Insert the product object as a document into the collection
    db.insert_one({
        "name": new_product.name,
        "price": new_product.price,
        "quantity": new_product.quantity
    })

    return "Product inserted successfully!"

# Route to fetch an item by ID
@app.route("/get_product/<string:item_id>")
def get_product(item_id):
    # Access the MongoDB collection
    db = mongo.db.products

    try:
        # Convert the item_id string to a MongoDB ObjectId
        item_id = ObjectId(item_id)

        # Query the collection to find the item by its ID
        product = db.find_one({"_id": item_id})

        if product:
            # Convert the ObjectId to a string for JSON serialization
            product['_id'] = str(product['_id'])

            # Return the product as JSON response
            return jsonify(product), 200
        else:
            return "Product not found", 404

    except Exception as e:
        return str(e), 400
    


# Define a custom JSON encoder that handles ObjectId
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to a string
        return super().default(obj)

app.json_encoder = CustomJSONEncoder  # Set the custom JSON encoder for the app

# Route to fetch all items
@app.route("/get_all_products")
def get_all_products():
    # Access the MongoDB collection
    db = mongo.db.products

    try:
        # Query the collection to retrieve all items
        products = list(db.find())

        if products:
            # Convert ObjectId fields to strings in the list of products
            for product in products:
                product['_id'] = str(product['_id'])

            # Return the list of products as JSON
            return jsonify(products), 200
        else:
            return "No products found", 404

    except Exception as e:
        return str(e), 400



if __name__ == '__main__':
    app.run()
