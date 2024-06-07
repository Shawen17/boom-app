import pytest
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


@pytest.mark.skip
@pytest.mark.django_db
def test_user_create(user_factory):
    user_factory.create()
    num = User.objects.all().count()
    print(user_factory.last_name)
    assert num == 1


@pytest.mark.parametrize(
    "first_name,last_name,email,password,state",
    [
        ("seun", "johnson", "test@gmail.com", "admin", "lagos"),
        # ("tammy", "johnson", "", "admin", "ontario"),
    ],
)
@pytest.mark.skip
def test_user_validation(
    db, user_factory, first_name, last_name, email, password, state
):
    test = user_factory(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        state=state,
    )
    item = User.objects.all().count()
    assert item == 1


@pytest.mark.parametrize(
    "profile, socials, organization, education,first_name,email,degree",
    [
        (
            {
                "email": "test@gmail.com",
                "bvn": 12345666,
                "firstName": "shawn",
                "lastName": "shawn",
                "phoneNumber": "78390100193",
            },
            {"facebook": "tammy", "twitter": "@tammy", "instagram": "@tammy"},
            {"orgName": "Bagco", "officeEmail": "hr@bagco.com"},
            {"level": "bsc"},
            "shawn",
            "test@gmail.com",
            "bsc",
        ),
        (
            {
                "email": "test2@gmail.com",
                "bvn": 12345666,
                "firstName": "tammy",
                "lastName": "shawn",
                "phoneNumber": "78390100193",
            },
            {"facebook": "tammy", "twitter": "@tammy", "instagram": "@tammy"},
            {"orgName": "Bagco", "officeEmail": "hr@bagco.com"},
            {"level": "bsc"},
            "tammy",
            "test2@gmail.com",
            "bsc",
        ),
    ],
)
@pytest.mark.django_db
def test_profile_create(
    insert_document_factory,
    profile,
    socials,
    organization,
    education,
    first_name,
    email,
    degree,
):

    data = {
        "profile": profile,
        "socials": socials,
        "organization": organization,
        "education": education,
    }

    id = insert_document_factory("users", data)
    db = settings.MONGO_DB
    collection = db["users"]
    inserted_doc = collection.find_one({"_id": id})
    print(inserted_doc)

    assert inserted_doc is not None
    assert inserted_doc["profile"]["firstName"] == first_name
    assert inserted_doc["profile"]["email"] == email
    assert inserted_doc["education"]["level"] == degree

    # Clean up the document after test
    collection.delete_one({"_id": id})
