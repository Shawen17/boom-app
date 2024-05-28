from pymongo import MongoClient
from decouple import config
from django.conf import settings
import gridfs


# db_user = config("DB_USER")
# db_password=config("PASSWORD")
# db_cluster = config("CLUSTERNAME")

# client = MongoClient(
#     f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority")

# db = client['db_files']

# name = "rapunzel.jpg"
# # file_location = "C:/Users/Owner/Downloads/" + name
# # with open(file_location,"rb") as file_data:
# #     data = file_data.read()
# #     fs = gridfs.GridFS(db)
# #     fs.put(data,filename = name)
# #     print('uploaded completely')

# fs = gridfs.GridFS(db)
# data = db.fs.files.find_one({"filename":name})
# my_id = data['_id']
# outputdata = fs.get(my_id).read()
# download_location = "C:/Users/Owner/Documents/" + name
# with open(download_location,"wb") as output:
#     output.write(outputdata)

# print("download complete")




# db= client['user_details']

# result = db['users'].count_documents({})
# print (result)

# client = MongoClient(f"mongodb://{db_user}:{db_password}@{db_cluster}/")
# db =client['user_details']
# result = db['loans'].count_documents({})
# print(result)


# def get_mongo_client():
#     mongo_settings = settings.MONGODB_DATABASES['default']
#     client = MongoClient(
        
#         host=mongo_settings['host'],
#         port=mongo_settings['port'],
#         username=mongo_settings['username'],
#         password=mongo_settings['password']
#     )
#     # Authenticate the client
#     db = client['user_details']
#     db.authenticate(
#         mongo_settings['username'],
#         mongo_settings['password']
#     )
#     if not authenticated:
#         raise Exception("Failed to authenticate with MongoDB")
#     return client


# client = pymongo.MongoClient(
#     f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority")

# db = client['user_details']
# db['users'].update_many(
#   {},
#   {
#     "$rename":{
#       "phoneNumber":"orgNumber",
#       "guarantor.firstName":"guarantor.guaFirstName",
#       "guarantor.lastName":"guarantor.guaLastName",
#       "guarantor.phoneNumber":"guarantor.guaNumber",
#       "guarantor.gender":"guarantor.guaGender",
#       "guarantor.address":"guarantor.guaAddress"

#     }
#   }
# )