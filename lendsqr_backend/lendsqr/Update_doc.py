# import pymongo
# import random
# import string
from decouple import config

# import threading
# import queue


db_user = config("DB_USER")
db_password = config("PASSWORD")
db_cluster = config("CLUSTERNAME")


# client = pymongo.MongoClient(
#     f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority")

# client2 = pymongo.MongoClient("mongodb://shawen:Shawenbaba1@localhost:27017/user_details")

# result_queue = queue.Queue()

# # db = client['user_details']
# # collection2 = client2['user_details']

# def get_data():
#     client = pymongo.MongoClient(
#     f"mongodb+srv://shawen17:{db_password}@shawencluster.jzsljb4.mongodb.net/?retryWrites=true&w=majority")
#     db = client['user_details']
#     query = db['loans'].find()
#     result_queue.put(query)

# def move_data():
#     result2=result_queue.get()
#     client2 = pymongo.MongoClient(f"mongodb://shawen:{db_password}@localhost:27017/")
#     collection2 = client2['user_details']
#     [collection2['loans'].insert_one(doc) for doc in result2]


# thread1 = threading.Thread(target=get_data)
# thread1.start()

# # Create and start the second thread
# thread2 = threading.Thread(target=move_data)
# thread2.start()

# thread1.join()
# thread2.join()


# documents = db['users'].find({"education.level": {"$exists": True}})
# for doc in documents:
#     field_value = doc.pop("education.level")
#     doc["profile.userName"] = field_value
#     db['users'].update_one({"_id": doc["_id"]}, {"$set": {"profile.userName":field_value}})
# db['users'].update_many({}, {"$unset": {"userName": ""}})


def add_new_field_with_nested_value(new_field_name, nested_field_names):
    # Query documents where the existing field exists
    documents = db["users"].find({nested_field_names[0]: {"$exists": True}})

    for doc in documents:
        # Extract the nested field values and remove them from the document
        nested_values = {}
        for nested_field_name in nested_field_names:
            print(doc["education"][nested_field_name])
            nested_values[nested_field_name] = doc.pop(
                "education" + "." + nested_field_name
            )

        # Add the new field with the extracted values as nested fields
        doc[new_field_name] = nested_values

        db["users"].update_one({"_id": doc["_id"]}, {"$set": doc})


def update_field_with_nested_values(
    source_field_name, target_field_name, nested_field_names
):
    # Query documents where the source field exists
    documents = db["users"].find({source_field_name: {"$exists": True}})

    for doc in documents:
        # Extract the specific nested field values from the source field
        nested_values_to_add = {
            nested_field: doc.get(source_field_name, {}).get(nested_field)
            for nested_field in nested_field_names
        }

        # Get existing nested values of the target field
        existing_nested_values = doc.get(target_field_name, {})

        # Merge the existing nested values with the extracted nested values
        updated_nested_values = {**existing_nested_values, **nested_values_to_add}

        # Update the target field with the merged nested values
        db["users"].update_one(
            {"_id": doc["_id"]}, {"$set": {target_field_name: updated_nested_values}}
        )


def remove_all_nested_fields_except(source_field_name, nested_field_to_keep):
    # Query documents where the source field exists
    documents = db["users"].find({source_field_name: {"$exists": True}})

    for doc in documents:
        # Create a list of nested fields to remove
        fields_to_remove = []
        for nested_field in doc.get(source_field_name, {}).keys():
            if nested_field != nested_field_to_keep:
                fields_to_remove.append(nested_field)

        # Remove nested fields except for the particular one to keep
        for field_to_remove in fields_to_remove:
            del doc[source_field_name][field_to_remove]

        # Update the document in the collection
        db["users"].update_one(
            {"_id": doc["_id"]}, {"$set": {source_field_name: doc[source_field_name]}}
        )


def generate_random_status(random_values):
    return random.choice(random_values)


def generate_random_loan_repayment():
    # Generate a random loan repayment amount between 200 and 500
    return round(random.uniform(5000.0, 200000), 2)


def generate_random_min_income():
    # Generate a random account balance between 400.0 and 100,000.0
    return round(random.uniform(30000.0, 80000.0), 2)


def generate_random_max_income():
    # Generate a random account balance between 400.0 and 100,000.0
    return round(random.uniform(100000.0, 3000000.0), 2)


def generate_random_number():
    # Generate a random number with length ten
    random_num = random.randint(10 ** (10 - 1), (10**10) - 1)
    return random_num


banks = [
    "Access",
    "Citibank",
    "Ecobank",
    "Fidelity",
    "First Bank",
    "FCMB",
    "Globus",
    "GTB",
    "Heritage",
    "Keystone",
    "Parallex",
    "Polaris",
    "Premium Trust",
    "Providus",
    "Stanbic IBTC",
    "Standard Chartered",
    "Sterling",
    "SunTrust",
    "Titan Trust",
    "Union Bank",
    "UBA",
    "Unity Bank",
    "Wema",
    "Zenith",
]


def add_random_nested_field_values():
    # Retrieve all documents in the collection
    documents = db["users"].find({"account": {"$exists": True}})
    # random_status=banks
    for doc in documents:
        # Generate random nested field values
        status = generate_random_number()
        # Update the document with the generated nested field values
        db["users"].update_one(
            {"_id": doc["_id"]}, {"$set": {"account.accountNumber": status}}
        )


# Example usage: Add random nested field values to the "account" field in all documents

# documents = db['users'].find({"status":{"$exists":True}})
# for doc in documents:
#     db['users'].update_one({"_id": doc["_id"]},{"$unset":{"status":""}})
# add_random_nested_field_values()
