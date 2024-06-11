# import pymongo
# import os
# from contextlib import contextmanager


# @contextmanager
# def pymongo_client():
#     db_user = os.getenv("DB_USER")
#     db_password = os.getenv("PASSWORD")
#     db_cluster = os.getenv("CLUSTERNAME")

#     client = pymongo.MongoClient(
#         f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority"
#     )

#     try:
#         yield client
#     finally:
#         client.close()


# db_user = os.getenv("DB_USER")
# db_password = os.getenv("PASSWORD")
# db_cluster = os.getenv("CLUSTERNAME")


# try:
#     client = pymongo.MongoClient(
#         f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority"
#     )

#     db = client["user_details"]
#     search = "shawen"
#     regex_pattern = f".*{search}.*"
#     query = {
#         "$and": [
#             {"guarantor": {"$exists": True}},
#             {
#                 "$or": [
#                     {
#                         "profile.email": {
#                             "$regex": regex_pattern,
#                             "$options": "i",
#                         }
#                     },
#                     {
#                         "profile.userName": {
#                             "$regex": regex_pattern,
#                             "$options": "i",
#                         }
#                     },
#                     {
#                         "profile.firstName": {
#                             "$regex": regex_pattern,
#                             "$options": "i",
#                         }
#                     },
#                     {
#                         "profile.lastName": {
#                             "$regex": regex_pattern,
#                             "$options": "i",
#                         }
#                     },
#                     {
#                         "profile.status": {
#                             "$regex": regex_pattern,
#                             "$options": "i",
#                         }
#                     },
#                     {
#                         "profile.address": {
#                             "$regex": regex_pattern,
#                             "$options": "i",
#                         }
#                     },
#                     {
#                         "organization.orgName": {
#                             "$regex": regex_pattern,
#                             "$options": "i",
#                         }
#                     },
#                     {
#                         "organization.employmentStatus": {
#                             "$regex": regex_pattern,
#                             "$options": "i",
#                         }
#                     },
#                     {
#                         "organization.sector": {
#                             "$regex": regex_pattern,
#                             "$options": "i",
#                         }
#                     },
#                     {
#                         "organization.officeEmail": {
#                             "$regex": regex_pattern,
#                             "$options": "i",
#                         }
#                     },
#                 ]
#             },
#         ]
#     }

#     users = db["users"].find(query)
#     all_documents = [{**doc, "_id": str(doc["_id"])} for doc in users]
#     print(len(all_documents))

# except Exception as e:
#     print(f"An error occurred: {e}")

# finally:
#     client.close()
