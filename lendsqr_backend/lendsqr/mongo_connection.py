import pymongo
import os
from contextlib import contextmanager


# def connect_and_search():
#     db_user = "shawen17"  # os.getenv("DB_USER")
#     db_password = "Shawenbaba1"  # os.getenv("PASSWORD")
#     db_cluster = "shawencluster"  # os.getenv("CLUSTERNAME")

#     client = pymongo.MongoClient(
#         f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority"
#     )

#     db = client["user_details"]
#     collection = db["loans"]


# Example usage


# try:
#     result = list(collection.aggregate(create_pipeline(20, 20)))
#     return result
# except Exception as e:
#     print(e)

# finally:
#     client.close()


def add_nested_field_with_default_value(field_path, default_value="111111111111"):
    try:
        # Connect to MongoDB
        db_user = "shawen17"  # os.getenv("DB_USER")
        db_password = "Shawenbaba1"  # os.getenv("PASSWORD")
        db_cluster = "shawencluster"  # os.getenv("CLUSTERNAME")

        client = pymongo.MongoClient(
            f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority"
        )

        db = client["user_details"]
        collection = db["loans"]

        # Create the update query
        # update_query = {"$set": {field_path: default_value}}
        # result = collection.update_many(
        #     {
        #         field_path: {"$exists": False}
        #     },  # Match documents where the field does not exist
        #     update_query,
        # )

        update_query = {"$unset": {field_path: ""}}

        # Update all documents to remove the nested field
        result = collection.update_many({}, update_query)

        print(
            f"Matched {result.matched_count} documents and modified {result.modified_count} documents."
        )
    except Exception as e:
        print(e)

    finally:
        client.close()


def remove_duplicate_loans():
    db_user = "shawen17"  # os.getenv("DB_USER")
    db_password = "Shawenbaba1"  # os.getenv("PASSWORD")
    db_cluster = "shawencluster"  # os.getenv("CLUSTERNAME")

    client = pymongo.MongoClient(
        f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority"
    )

    db = client["user_details"]
    collection = db["users"]

    try:

        # Find duplicates by grouping based on loan.email
        pipeline = [
            {
                "$group": {
                    "_id": "$profile.email",
                    "uniqueIds": {"$addToSet": "$_id"},
                    "count": {"$sum": 1},
                }
            },
            {"$match": {"count": {"$gt": 1}}},
        ]

        duplicates = list(collection.aggregate(pipeline))

        for doc in duplicates:
            # Remove all but one of the duplicate documents
            doc["uniqueIds"].pop(0)  # Keep one document and remove the rest
            collection.delete_many({"_id": {"$in": doc["uniqueIds"]}})

        print("Duplicate documents removed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()


remove_duplicate_loans()


# add_nested_field_with_default_value("loan.bvn")
# try:
#     db = client["user_details"]
#     search = "seun"
#     # collection = db["users"]
#     # Create the index if it doesn't exist
#     index_name = "profile.firstName_text_profile.lastName_text_organization.orgName_text_organization.officeEmail_text"
#     # collection.drop_index(index_name)
#     if index_name not in db.users.index_information():
#         db.users.create_index(
#             {
#                 "profile.firstName": "text",
#                 "profile.lastName": "text",
#                 "organization.orgName": "text",
#                 "organization.officeEmail": "text",
#             }
#         )

#     # Perform the search
#     result = db.users.find({"$text": {"$search": search}})

#     # Print the results
#     for doc in result:
#         print(doc)


# Run the function


# @contextmanager
# def pymongo_client():
#     db_user = "shawen17"  # os.getenv("DB_USER")
#     db_password = "Shawenbaba1"  # os.getenv("PASSWORD")
#     db_cluster = "shawencluster"  # os.getenv("CLUSTERNAME")

#     client = pymongo.MongoClient(
#         f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority"
#     )

#     try:
#         yield client
#     finally:
#         client.close()


# with pymongo_client() as client:
#     db = client["user_details"]
#     search = "johnson"

#     # Check if the index exists, and create it if it doesn't
#     index_info = db.users.index_information()
#     if (
#         "profile.firstname_text_profile.lastname_text_profile.avatar_text_organization.company_text_organization.email_text"
#         not in index_info
#     ):
#         db.users.create_index(
#             {
#                 "profile.firstname": "text",
#                 "profile.lastname": "text",
#                 "profile.avatar": "text",
#                 "organization.company": "text",
#                 "organization.email": "text",
#             }
#         )

#     # Search the collection
#     result = db.users.find({"$text": {"$search": search}})

#     # Iterate over and print the results
#     for doc in result:
#         print(doc)


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
