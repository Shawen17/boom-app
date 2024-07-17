import json
import hashlib
from rest_framework.response import Response
from rest_framework import status
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def generate_cache_key(request):
    # Create a unique cache key based on the query parameters
    query_params = request.GET.dict()
    query_params_str = json.dumps(query_params, sort_keys=True)
    return hashlib.md5(query_params_str.encode("utf-8")).hexdigest()


# @cache_page(CACHE_TTL)
def users_portfolio(request, db):
    page = int(request.GET.get("page", 1))
    search = request.GET.get("search", "")
    per_page = int(request.GET.get("pageSize", 20))

    if search:
        regex_pattern = f".*{search}.*"
        query = {
            "$and": [
                {"guarantor": {"$exists": True}},
                {
                    "$or": [
                        {
                            "profile.email": {
                                "$regex": regex_pattern,
                                "$options": "i",
                            }
                        },
                        {
                            "profile.userName": {
                                "$regex": regex_pattern,
                                "$options": "i",
                            }
                        },
                        {
                            "profile.firstName": {
                                "$regex": regex_pattern,
                                "$options": "i",
                            }
                        },
                        {
                            "profile.lastName": {
                                "$regex": regex_pattern,
                                "$options": "i",
                            }
                        },
                        {
                            "profile.status": {
                                "$regex": regex_pattern,
                                "$options": "i",
                            }
                        },
                        {
                            "profile.address": {
                                "$regex": regex_pattern,
                                "$options": "i",
                            }
                        },
                        {
                            "organization.orgName": {
                                "$regex": regex_pattern,
                                "$options": "i",
                            }
                        },
                        {
                            "organization.employmentStatus": {
                                "$regex": regex_pattern,
                                "$options": "i",
                            }
                        },
                        {
                            "organization.sector": {
                                "$regex": regex_pattern,
                                "$options": "i",
                            }
                        },
                        {
                            "organization.officeEmail": {
                                "$regex": regex_pattern,
                                "$options": "i",
                            }
                        },
                    ]
                },
            ]
        }
        users = db["users"].find(query, {"updatedAt": 0})

    else:
        users = db["users"].find({"guarantor": {"$exists": True}})
    # per_page = 20
    start_index = (page - 1) * per_page
    end_index = page * per_page
    all_documents = [{**doc, "_id": str(doc["_id"])} for doc in users]

    users_paginated = all_documents[start_index:end_index]
    all_users = len(all_documents)
    active = len(
        [item for item in all_documents if item["profile"]["status"] == "Active"]
    )
    loan = len(
        [
            item
            for item in all_documents
            if "account" in item and int(item["account"]["loanRepayment"]) > 0
        ]
    )
    savings = len(
        [
            item
            for item in all_documents
            if "account" in item and int(item["account"]["accountBalance"]) > 0
        ]
    )
    return Response(
        {
            "users_paginated": users_paginated,
            "all_users": all_users,
            "active": active,
            "loan": loan,
            "savings": savings,
        },
        status=status.HTTP_200_OK,
    )
