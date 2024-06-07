import pytest
from pytest_factoryboy import register
from django.conf import settings


@pytest.fixture
def insert_document_factory(db):
    def insert_new(collection_name, document):
        database = settings.MONGO_DB
        collection = database[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    return insert_new


@pytest.fixture
def new_user(db, user_factory):
    user = user_factory.create()
    return user
