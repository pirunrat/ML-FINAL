from combiner import Combiner
from pymongo import MongoClient
from sklearn.decomposition import NMF
from sklearn.utils.validation import check_is_fitted
import unittest
import numpy as np
import pickle
import pandas as pd


class TestRecommendations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uri = "mongodb+srv://Admin:1234@mlproject.obivlrq.mongodb.net/?retryWrites=true&w=majority"
        cls.client = MongoClient(cls.uri)
        cls.mongo_rating = cls.client['E-commerce']['Rating']
        cls.mongo_product = cls.client['E-commerce']['Product5000']
        cls.mongo_asin_list = [x['asin'] for x in cls.mongo_product.find({"asin":"B0000223SI"}, {'_id': 0, 'asin': 1})]

        # Specify the relative path to the files within the 'model' directory
        cls.csv_file_path = './model/product_sims_train.csv'
        cls.model_file_path = './model/mf_factorizer_train.pkl'

        # Load models
        cls.similarity_df = pd.read_csv(cls.csv_file_path, index_col=0)
        cls.factorizer = pickle.load(open(cls.model_file_path, 'rb'))
        cls.n_recom = 5

    # def test_IBCF_matrix(self):
    #     assert self.similarity_df.shape[0] == self.similarity_df.shape[1], "Number of rows and columns in IBCF Similarity matrix should be the same"
    #     assert self.similarity_df.shape[1] == self.similarity_df.select_dtypes(include=["float", 'int']).shape[1], "All values in IBCF similarity matrix should be numeric"
    #     assert self.similarity_df.notna().values.any(), "There must not be any missing value in IBCF similarity matrix"
    #     assert set(self.similarity_df.columns) <= set(self.mongo_asin_list), "Some products in IBCF similarity matrix are not found in the database"

    # def test_MF_factorizer(self):
    #     assert type(self.factorizer) == NMF, "NMF factorizer is not an Sklearn's NMF instance"
    #     check_is_fitted(self.factorizer, msg="NMF factorizer has yet to be fitted")
    #     assert set(self.factorizer.feature_names_in_) <= set(self.mongo_asin_list), "Some products in NMF factorizer are not found in the database"

    def test_models_compat(self):
        assert len(self.similarity_df.columns) == len(self.factorizer.feature_names_in_), "Models do not have the same number of products"
        assert (self.factorizer.feature_names_in_ == self.similarity_df.columns).all(), "Models product names do not match or are ordered incorrectly"

    # def test_recommendations(self):
    #     user_data = self.mongo_rating.find_one({}, {'_id': 0})
    #     username = user_data['username']
    #     user_ratings = pd.Series(user_data, index=self.similarity_df.columns.tolist(), name=username).fillna(0)

    #     combiner = Combiner(self.similarity_df.to_numpy(), self.factorizer)
    #     combiner.ingest(user_ratings)
    #     recom_list = list(combiner.make_recommendations(username, self.n_recom).keys())

    #     assert len(recom_list) == self.n_recom, "Number of recommended products do not match the combiner input"
    #     assert set(recom_list) <= set(self.mongo_asin_list), "Some or all recommended products are not found in the database"

if __name__ == '__main__':
    unittest.main()
