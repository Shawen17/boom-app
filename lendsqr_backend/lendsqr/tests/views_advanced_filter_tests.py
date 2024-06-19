import pytest
import json
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.parametrize(
    "profile, organization,password, query, validity,page",
    [
        (
            {
                "email": "test@gmail.com",
                "bvn": 12345666,
                "firstName": "shawn",
                "lastName": "shawn",
                "phoneNumber": "78390100193",
                "status": "Active",
            },
            {},
            "admin",
            {"email": "test@gmail.com", "status": "Active"},
            0,
            1,
        ),
        # (
        #     {
        #         "email": "test2@gmail.com",
        #         "bvn": 12345666,
        #         "firstName": "tammy",
        #         "lastName": "johnson",
        #         "phoneNumber": "78390100193",
        #         "status": "Inactive",
        #     },
        #     {},
        #     "admin",
        #     {"userName": "jaycee", "status": "Active"},
        #     1,
        #     1,
        # ),
        (
            {
                "email": "test3@gmail.com",
                "bvn": 12345666,
                "firstName": "tammy",
                "lastName": "johnson",
                "phoneNumber": "78390100193",
                "status": "Inactive",
            },
            {"orgName": "knorr"},
            "admin",
            {},
            0,
            1,
        ),
        # (
        #     {
        #         "email": "test4@gmail.com",
        #         "bvn": 12345666,
        #         "firstName": "tammy",
        #         "lastName": "johnson",
        #         "phoneNumber": "78390100193",
        #         "status": "Inactive",
        #     },
        #     {},
        #     "admin",
        #     {"status": "Blacklisted"},
        #     1,
        #     1,
        # ),
        # Add more test cases if needed
    ],
)
@pytest.mark.fast
@pytest.mark.django_db
def test_advanced_filter(
    client, profile, organization, password, query, validity, page
):
    User.objects.create_user(
        first_name=profile["firstName"],
        last_name=profile["lastName"],
        email=profile["email"],
        password=password,
    )
    login_url = "/auth/jwt/create/"
    data = {"email": profile["email"], "password": password}
    # client = APIClient()
    print("========login initiated===========")
    response = client.post(login_url, data, format="json")

    assert "access" in response.data
    assert "refresh" in response.data
    token = response.data["access"]

    print("========login successful===========")
    url = f"/api/advance-filter?page={page}"  # Modify the URL according to your API endpoint
    data = {
        "profile": json.dumps(query),
        "organization": json.dumps(organization),
    }
    headers = {"content_type": "multipart/form-data", "Authorization": token}
    print("========filter initiated===========")
    response = client.post(url, data=data, headers=headers)
    assert len(response.data) >= validity
    print("========filter successful===========")
