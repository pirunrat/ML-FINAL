from .authenticate_request import authenticate_request
from django.http import JsonResponse, HttpResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from .mongoDB import MongoDBClient
from .mysqlDB import MySQLDatabase 
from bson import ObjectId
from json import JSONEncoder
from combiner import Combiner
import json
import pickle
import pandas as pd
import os
from django.conf import settings




class MongoJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)




mongo_product5000 = MongoDBClient('mongodb+srv://Admin:1234@mlproject.obivlrq.mongodb.net/?retryWrites=true&w=majority','E-commerce','Product5000')

mongo_rating2 = MongoDBClient('mongodb+srv://Admin:1234@mlproject.obivlrq.mongodb.net/?retryWrites=true&w=majority',"E-commerce","Rating")

mongo_user = MongoDBClient('mongodb+srv://Admin:1234@mlproject.obivlrq.mongodb.net/?retryWrites=true&w=majority',"E-commerce","User")



# # Specify the relative path to the files within the 'model' directory
# csv_file_path = os.path.join(settings.BASE_DIR, 'mybackend', 'model', 'product_sims_train.csv')
# model_file_path = os.path.join(settings.BASE_DIR, 'mybackend', 'model', 'mf_factorizer_train.pkl')


# # Retrive item-to-item similarities dataframe for IBCF recommendations
# similarities = pd.read_csv(csv_file_path, index_col=0)
# product_list = similarities.columns.tolist()    # list of product IDs
# similarities = similarities.to_numpy()          # convert similarities to numpy array
# # Retrieve MF factorizer
# factorizer = pickle.load(open(model_file_path, 'rb'))
# # Combiner for aggregating both recommender scores
# combiner = Combiner(similarities, factorizer, ibcf_weight=0.5)




#  # Database connection parameters
# host = "127.0.0.1"
# user = "root"
# password = "Pirunrat37@"
# database = "mproj"

# # Create a MySQLDatabase instance
# db = MySQLDatabase(host, user, password, database)

# # Connect to the database
# db.connect()




@csrf_exempt
@authenticate_request
def landing_page(request):
    token = 'asdasewadsdsdasd3232564231dsasdasdasd'
    return JsonResponse({'token': token, 'status': 'success'})



@csrf_exempt
@authenticate_request
def product_normal(request):
    if request.method == 'GET':
        data = mongo_product5000.find({'imageURL': { "$ne": None } }).limit(12)
        data_list = list(data)
        return HttpResponse(json.dumps(data_list, cls=MongoJsonEncoder), content_type="application/json")
    


@csrf_exempt
@authenticate_request
def product_recommend(request):
    if request.method == 'GET':
        data = mongo_product5000.find({}).limit(5)
        data_list = list(data)
        return HttpResponse(json.dumps(data_list, cls=MongoJsonEncoder), content_type="application/json")
    



@csrf_exempt
@authenticate_request
def product_recommend_register(request):
    if request.method == 'GET':
        data = mongo_product5000.find({}).limit(5)
        data_list = list(data)
        return HttpResponse(json.dumps(data_list, cls=MongoJsonEncoder), content_type="application/json")
    



@csrf_exempt
def product_rated_recommend(request):
    if request.method == 'POST':
        try:
            # Check if the content type is JSON
            if request.content_type == 'application/json':
                # If the request contains JSON data
                data = json.loads(request.body.decode('utf-8'))
            else:
                # If the request contains form data
                data = request.POST  # Use request.POST for form data

            # Now you can access the data as a dictionary
            username = data['username']
            Ratedproducts = data['ratedproduct']

            # Transform the data 
            transform_ratedproducts = transform_data(username,Ratedproducts)
            
            # Insert into Rating Collection
            mongo_rating2.insert_one(transform_ratedproducts)
            

            return JsonResponse({"message": "Successfully inserted rated products by new user"},status=200)

        except Exception as e:
            # Handle exceptions here
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    



# @csrf_exempt
# def make_recommendations(request):
#     if request.method == 'POST':
#         try:
#             # Check if the content type is JSON
#             if request.content_type == 'application/json':
#                 # If the request contains JSON data
#                 data = json.loads(request.body.decode('utf-8'))
#             else:
#                 # If the request contains form data
#                 data = request.POST  # Use request.POST for form data

#             # Now you can access the data as a dictionary
#             username = data

#             transform_ratedproducts = mongo_rating2.find_one({"username": username})

#             transform_ratedproducts.pop('_id', None)
            
#             print(transform_ratedproducts)

#             ratings = pd.Series(transform_ratedproducts, index=product_list, name=username).fillna(0)
#             combiner.ingest(ratings)
#             recom_list = list(combiner.make_recommendations(username, 5).keys())
            
#             return HttpResponse(json.dumps(recom_list, cls=MongoJsonEncoder), content_type="application/json")


#         except Exception as e:
#             # Handle exceptions here
#             return JsonResponse({"error": str(e)}, status=500)

#     else:
#         return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    






@csrf_exempt
@authenticate_request
def Update_Rated_Recommend(request):
    if request.method == 'POST':
        try:
            # Check if the content type is JSON
            if request.content_type == 'application/json':
                # If the request contains JSON data
                data = json.loads(request.body.decode('utf-8'))
            else:
                # If the request contains form data
                data = request.POST  # Use request.POST for form data

             # Now you can access the data as a dictionary
            username = data['username']
            Ratedproducts = data['ratedproduct']

            # Transform the data 
            transform_ratedproducts = transform_data(username,Ratedproducts)


            query = {'username': transform_ratedproducts['username']}


            # Define the new values you want to set in the document
            new_values = {
                            '$set': transform_ratedproducts
                        }
            

            # Insert into Rating Collection
            mongo_rating2.update_many(query,new_values)
            

            return JsonResponse({"message": "Updated User data Successfully"},status=200)

        except Exception as e:
            # Handle exceptions here
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    








@csrf_exempt
def Register(request):
    if request.method == 'POST':
        try:
            # Check if the content type is JSON
            if request.content_type == 'application/json':
                # If the request contains JSON data
                data = json.loads(request.body.decode('utf-8'))
            else:
                # If the request contains form data
                data = request.POST  # Use request.POST for form data

            # Now you can access the data as a dictionary
            username = data['username']
            password = data['password']

            data_insert = {
                "username":username,
                "password":password,
            }

            print(data_insert)
            # Insert into Rating Collection
            mongo_user.insert_one(data_insert)
            

            return JsonResponse({"message": "Insert User data Successfully"},status=200)

        except Exception as e:
            # Handle exceptions here
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    





def transform_data(username, ratedproducts):
    
    dict_ratedproduct = {}

    dict_ratedproduct['username'] = username

    for obj in ratedproducts:
        productId = obj['productId']
        rateValue = obj['rateValue']
        dict_ratedproduct[productId] = rateValue

    return dict_ratedproduct
            
            
        
        