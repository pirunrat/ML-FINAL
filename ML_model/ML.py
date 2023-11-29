from flask import Flask, Response, request, jsonify
import json
from mongoDB import MongoDBClient
from combiner import Combiner
import os
import pandas as pd
import pickle
from bson import ObjectId
from json import JSONEncoder
from flask_cors import CORS



class MongoJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

app = Flask(__name__)

# Allow requests from 'http://localhost:3000' to the '/make_recommendations' route
CORS(app, resources={r"/make_recommendations": {"origins": "http://localhost:3000"}})


# MongoDB connection configuration
mongo_product5000 = MongoDBClient('mongodb+srv://Admin:1234@mlproject.obivlrq.mongodb.net/?retryWrites=true&w=majority', 'E-commerce', 'Product5000')
mongo_rating2 = MongoDBClient('mongodb+srv://Admin:1234@mlproject.obivlrq.mongodb.net/?retryWrites=true&w=majority', 'E-commerce', 'Rating')
mongo_user = MongoDBClient('mongodb+srv://Admin:1234@mlproject.obivlrq.mongodb.net/?retryWrites=true&w=majority', 'E-commerce', 'User')

# Specify the relative path to the files within the 'model' directory
csv_file_path = './model/product_sims_train.csv'
model_file_path = './model/mf_factorizer_train.pkl'

# Retrieve item-to-item similarities dataframe for IBCF recommendations
similarities = pd.read_csv(csv_file_path, index_col=0)
product_list = similarities.columns.tolist()  # list of product IDs
similarities = similarities.to_numpy()  # convert similarities to a numpy array

# Retrieve MF factorizer
factorizer = pickle.load(open(model_file_path, 'rb'))

# Combiner for aggregating both recommender scores
combiner = Combiner(similarities, factorizer, ibcf_weight=0.5)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

@app.route('/make_recommendations', methods=['POST'])
def make_recommendations():
    try:
        # Check if the content type is JSON
        if request.content_type == 'application/json':
            # If the request contains JSON data
            data = request.get_json()  # Parse JSON data
            username = data.get('username', '')  # Replace 'username' with the actual key in your JSON data
        else:
            # If the request contains form data
            username = request.form.get('username', '')  # Replace 'username' with the actual form field name

        transform_ratedproducts = mongo_rating2.find_one({"username": username})
        if transform_ratedproducts is None:
            return jsonify({"error": "User not found"}), 404

        transform_ratedproducts.pop('_id', None)

        ratings = pd.Series(transform_ratedproducts, index=product_list, name=username).fillna(0)
        combiner.ingest(ratings)
        recom_list = list(combiner.make_recommendations(username, 5).keys())

        recommended_products = []
        for item in recom_list:
            if item:
                recommended_products.append(mongo_product5000.find_one({'asin': item}))
            else:
                continue
        recommended_products = list(recommended_products)
        return Response(json.dumps(recommended_products, cls=MongoJsonEncoder), content_type="application/json")  # Return JSON array

    except Exception as e:
        # Handle exceptions here and provide a meaningful error response
        print(str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
