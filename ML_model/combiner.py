import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.decomposition import NMF

class Combiner(object):

    """
    Combiner combines results of similarity_mtx for IBCF recommendation and factorizer for MF recommendation.
    similarity_mtx: square numpy array (rows and columns must be of equal length).
    factorizer: fitted Sklearn NMF model (sklearn.decomposition.NMF).
    ibcf_weight: it determines the weight ratio between IBCF and MF models and must range between 0 and 1.
    """
    
    def __init__(self, similarity_mtx: np.ndarray, factorizer: NMF, ibcf_weight = 0.5):
        if (similarity_mtx.shape[0] != similarity_mtx.shape[1] or
            factorizer.n_features_in_ != similarity_mtx.shape[0] or
            ibcf_weight < 0 or ibcf_weight > 1):
            raise ValueError
        
        self.similarity_mtx = similarity_mtx
        self.factorizer = factorizer
        self.ibcf_weight = ibcf_weight
        self.combiner_ratings = None

    """
    Functions for IBCF and MF rating predictions include the for_eval argument.
    It specifies whether we want to predict the missing ratings (for making recommendations)
    or predict the known ratings of purchased products (for model evaluations).
    """

    def _predict_ibcf(self, ratings, for_eval=False):
        ratings = ratings.T

        if for_eval == False:
            ibcf_ratings = pd.DataFrame(index=ratings.index, columns=ratings.columns)

            for user_id in ratings.columns:
                user_rating = ratings.loc[:, user_id]
                # numerators are the sum of product of rated products similarities and ratings of such products given by a user
                numerators = np.dot(self.similarity_mtx, user_rating)
                # corr_sim = self.similarity_mtx[:, user_rating > 0]
                pred_user_rating = []

                # Calculate rating for each product
                for i, ix in enumerate(user_rating):
                            
                    # Predict missing ratings only (value is zero)
                    if ix == 0:
                        numer = numerators[i]
                        # Denominator is a sum of product similarities excluding itself
                        denom = np.delete(self.similarity_mtx[i, :], i, -1).sum()
                        if numer == 0 or denom == 0:
                            pred = 0
                        else:
                            pred = numer / denom
                        pred_user_rating.append(pred)

                    # set ratings of product already purchased by user as null
                    else:
                        pred_user_rating.append(np.nan)
                        
                ibcf_ratings[user_id] = pred_user_rating

            return ibcf_ratings.T
        
        else:
            known_ibcf_ratings = pd.DataFrame(index=ratings.index, columns=ratings.columns)

            for user_id in ratings.columns:
                user_rating = ratings.loc[:, user_id]
                pred_user_rating = []

                # Calculate rating for each product
                for i, ix in enumerate(user_rating):
                    # Predict known ratings only (value is not zero)
                    if ix != 0:
                        # Get user ratings and set the current product rating to zero
                        dummy_rating = user_rating.copy(deep=True)
                        dummy_rating[i] = 0
                        numerators = np.dot(self.similarity_mtx, user_rating)
                        numer = numerators[i]
                        # Denominator is a sum of product similarities excluding itself
                        denom = np.delete(self.similarity_mtx[i, :], i, -1).sum()
                        if numer == 0 or denom == 0:
                            pred = 0
                        else:
                            pred = numer / denom
                        pred_user_rating.append(pred)

                    # set ratings of non-purchased product as null
                    else:
                        pred_user_rating.append(np.nan)
                        
                known_ibcf_ratings[user_id] = pred_user_rating

            return known_ibcf_ratings.T

    def _predict_mf(self, ratings, for_eval=False):
        user_comp = self.factorizer.transform(ratings)
        prod_comp = self.factorizer.components_
        mf_array = np.dot(user_comp, prod_comp)
        mf_ratings = pd.DataFrame(mf_array, index=ratings.index, columns=ratings.columns)

        # If making recommendations, mask the ratings of purchased products so that they are null
        if for_eval == False:
            return mf_ratings.where(ratings == 0)
        # If making evaluations, mask the ratings of non-purchased products so that they are null
        else:
            return mf_ratings.where(ratings != 0)
        
    # Ingest the rating data and return the predicted missing ratings matrices for each model
    def ingest(self, ratings):
        if isinstance(ratings, pd.Series):
            ratings = ratings.to_frame().T
        
        self.ibcf_ratings = self._predict_ibcf(ratings, for_eval=False)
        self.mf_ratings = self._predict_mf(ratings, for_eval=False)
        self.combiner_ratings = self.ibcf_weight * self.ibcf_ratings + (1 - self.ibcf_weight) * self.mf_ratings

        return self.ibcf_ratings, self.mf_ratings, self.combiner_ratings
    
    """ 
    In order to call the below methods for recommendations,
    first ingest the user-product rating matrix into the Combiner using ingest() method.
    """
    
    def make_mf_recommendations(self, user_id, top_n):
        user_pred = self.mf_ratings.loc[user_id]
        return user_pred.sort_values(ascending=False)[:top_n]
    
    def make_ibcf_recommendations(self, user_id, top_n):
        user_pred = self.ibcf_ratings.loc[user_id]
        return user_pred.sort_values(ascending=False)[:top_n]
    
    def make_recommendations(self, user_id, top_n):
        if self.combiner_ratings is None:
            self.combine_ratings()

        user_pred = self.combiner_ratings.loc[user_id]
        return user_pred.sort_values(ascending=False)[:top_n]

    # Evaluating each model using RMSE and MAE scores
    def evaluate_models(self, ratings):
        if isinstance(ratings, pd.Series):
            ratings = ratings.to_frame().T

        true_ratings_array = ratings.where(ratings != 0).stack().values

        to_eval = {
            "IBCF": self._predict_ibcf(ratings, for_eval=True).stack().values,
            "MF": self._predict_mf(ratings, for_eval=True).stack().values
        }
        
        for model in to_eval.keys():
            print(f"====={model}=====")
            print(f"RMSE: {mean_squared_error(true_ratings_array, to_eval[model], squared=True)}")
            print(f"MAE: {mean_absolute_error(true_ratings_array, to_eval[model])}\n")