import json
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.conf import settings

User = get_user_model()


@pytest.mark.parametrize(
    "loan, guarantor, account,password, login_validity, loan_validity",
    [
        (
            {
                "email": "test@gmail.com",
                "bvn": 12345666,
                "amount": 6000,
                "loanRepayment": "60666",
                "duration": 11,
                "accountNumber": 87382992,
                "bank": "providus",
                "firstName": "shawn",
                "lastName": "shawn",
                "phoneNumber": "78390100193",
            },
            {
                "guaFirstName": "Active",
                "guaLastName": "shawen",
                "guaNumber": "462889999",
                "guaAddress": "manufachi",
                "guaGender": "Male",
                "relationship": "Colleague",
            },
            {
                "loanRepayment": "1277781889",
                "accountNumber": 878887889,
                "bank": "Providus",
                "accountBalance": 782882,
                "monthlyIncome": [35356266, 57748990],
            },
            "testpassword1",
            200,
            201,
        ),
        (
            {
                "email": "test2@gmail.com",
                "bvn": "wrong type",
                "amount": 6000,
                "loanRepayment": "60666",
                "duration": 11,
                "accountNumber": 87382992,
                "bank": "providus",
                "firstName": "shawn",
                "lastName": "shawn",
                "phoneNumber": "78390100193",
            },
            {
                "guaFirstName": "Active",
                "guaLastName": "shawen",
                "guaNumber": "462889999",
                "guaAddress": "manufachi",
                "guaGender": "Male",
                "relationship": "Colleague",
            },
            {
                "loanRepayment": "1277781889",
                "accountNumber": 878887889,
                "bank": "Providus",
                "accountBalance": 782882,
                "monthlyIncome": [35356266, 57748990],
            },
            "testpassword1",
            200,
            500,
        ),
    ],
)
@pytest.mark.django_db
def test_user_login_loan_apply(
    client,
    loan,
    guarantor,
    account,
    password,
    login_validity,
    loan_validity,
):

    User.objects.create_user(
        first_name=loan["firstName"],
        last_name=loan["lastName"],
        email=loan["email"],
        password=password,
    )

    login_url = "/auth/jwt/create/"
    data = {"email": loan["email"], "password": password}
    client = APIClient()
    print("========login initiated===========")
    response = client.post(login_url, data, format="json")

    assert response.status_code == login_validity
    assert "access" in response.data
    assert "refresh" in response.data
    token = response.data["access"]

    print("========login successful===========")

    url = "/api/loan/"  # Modify the URL according to your API endpoint
    data = {
        "loan": json.dumps(loan),
        "guarantor": json.dumps(guarantor),
        "account": json.dumps(account),
    }
    headers = {"content_type": "multipart/form-data", "Authorization": token}
    print("========loan application initiated===========")
    response = client.post(url, data=data, headers=headers)

    assert response.status_code == loan_validity
    print("========loan application successful===========")
    db = settings.MONGO_DB
    collection = db["users"]
    collection.delete_one({"loan.email": loan["email"]})
