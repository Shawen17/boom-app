# import pytest
# from django.contrib.auth import get_user_model

# User = get_user_model()


# @pytest.mark.parametrize(
#     "page, search,validity",
#     [
#         (1, "beau", 1),
#         (2, "", 1),
#     ],
# )
# @pytest.mark.fast
# @pytest.mark.django_db
# def test_load_user(client, page, search, validity):
#     email = "shawn@gmail.com"
#     password = "admin"

#     User.objects.create_user(
#         first_name="shawn",
#         last_name="shawn",
#         email=email,
#         password=password,
#     )
#     login_url = "/auth/jwt/create/"
#     data = {"email": email, "password": password}
#     # client = APIClient()
#     print("========login initiated===========")
#     response = client.post(login_url, data, format="json")
#     token = response.data["access"]

#     print("========login successful===========")
#     url = f"/api/users?page={page}&search={search}"

#     headers = {"content_type": "application/json", "Authorization": token}
#     print("========fetching users===========")
#     response = client.get(url, headers=headers)
#     assert len(response.data["users_paginated"]) >= validity
#     print("========users loaded successfully===========")
