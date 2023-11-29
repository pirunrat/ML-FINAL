from combiner import Combiner
from pymongo import MongoClient
from sklearn.decomposition import NMF
from sklearn.utils.validation import check_is_fitted

import numpy as np
import pickle
import pandas as pd
import os
from django.conf import settings

uri = "mongodb+srv://Admin:1234@mlproject.obivlrq.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and access database collection
client = MongoClient(uri)
mongo_rating = client['E-commerce']['Rating']
mongo_product = client['E-commerce']['Product5000']
mongo_asin_list = [x['asin'] for x in mongo_product.find({}, {'_id': 0, 'asin': 1})]


# Specify the relative path to the files within the 'model' directory
csv_file_path = os.path.join(settings.BASE_DIR, 'mybackend', 'model', 'product_sims_train.csv')
model_file_path = os.path.join(settings.BASE_DIR, 'mybackend', 'model', 'mf_factorizer_train.pkl')


# Load models
similarity_df = pd.read_csv(csv_file_path, index_col=0)
factorizer = pickle.load(open(model_file_path, 'rb'))
n_recom = 5

def test_IBCF_matrix():
    assert similarity_df.shape[0] == similarity_df.shape[1], "Number of rows and columns in IBCF Similarity matrix should be the same"
    assert similarity_df.shape[1] == similarity_df.select_dtypes(include=["float", 'int']).shape[1], "All values in IBCF similarity matrix should be numeric"
    assert similarity_df.notna().values.any(), "There must not be any missing value in IBCF similarity matrix"
    assert set(similarity_df.columns) <= set(mongo_asin_list), "Some products in IBCF similarity matrix are not found in the database"

def test_MF_factorizer():
    assert type(factorizer) == NMF, "NMF factorizer is not an Sklearn's NMF instance"
    check_is_fitted(factorizer, msg="NMF factorizer has yet to be fitted")
    assert set(factorizer.feature_names_in_) <= set(mongo_asin_list), "Some products in NMF factorizer are not found in the database"

def test_models_compat():
    assert len(similarity_df.columns) == len(factorizer.feature_names_in_), "Models do not have the same number of products"
    assert (factorizer.feature_names_in_ == similarity_df.columns).all(), "Models products names do not match or are ordered incorrectly"

def test_recommendations():
    user_data = mongo_rating.find_one({}, {'_id': 0})
    username = user_data['username']
    user_ratings = pd.Series(user_data, index=similarity_df.columns.tolist(), name=username).fillna(0)

    combiner = Combiner(similarity_df.to_numpy(), factorizer)
    combiner.ingest(user_ratings)
    recom_list = list(combiner.make_recommendations(username, n_recom).keys())

    assert len(recom_list) == n_recom, "Number of recommended products do not match the combiner input"
    assert set(recom_list) <= set(mongo_asin_list), "Some or all recommended products are not found in the database"