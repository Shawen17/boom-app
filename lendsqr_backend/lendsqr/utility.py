import json
import hashlib
from rest_framework.response import Response
from rest_framework import status
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings
import redis
import os
from prometheus_client import CollectorRegistry, generate_latest


r = redis.Redis(host=os.getenv("REDIS"), port=6379, db=0)
CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)
REDIS_METRICS_KEY = "prometheus_metrics"


def generate_cache_key(request):
    # Create a unique cache key based on the query parameters
    query_params = request.GET.dict()
    query_params_str = json.dumps(query_params, sort_keys=True)
    return hashlib.md5(query_params_str.encode("utf-8")).hexdigest()


def connect_and_search(db):

    collection = db["users"]

    def create_pipeline(skip, limit):
        pipeline = [
            {
                "$facet": {
                    # Stage 1: Counting logic
                    "counts": [
                        {
                            "$addFields": {
                                "isActive": {"$eq": ["$profile.status", "Active"]},
                                "hasLoan": {"$gt": ["$account.loanRepayment", 0]},
                                "hasSavings": {"$gt": ["$account.accountBalance", 0]},
                            },
                        },
                        {
                            "$group": {
                                "_id": None,
                                "totalDocuments": {"$sum": 1},
                                "totalActive": {"$sum": {"$cond": ["$isActive", 1, 0]}},
                                "totalWithLoan": {
                                    "$sum": {"$cond": ["$hasLoan", 1, 0]}
                                },
                                "totalWithSavings": {
                                    "$sum": {"$cond": ["$hasSavings", 1, 0]}
                                },
                            }
                        },
                    ],
                    # Stage 2: Retrieval logic
                    "documents": [
                        {"$match": {"guarantor": {"$exists": True}}},
                        {"$skip": skip},
                        {"$limit": limit},
                        {
                            "$project": {
                                "_id": 1,
                                "profile": 1,
                                "guarantor": 1,
                                "account": 1,
                                "organization": 1,
                                "socials": 1,
                                "education": 1,
                                # Add other fields you want to keep
                                # Exclude the updatedAt field
                            }
                        },
                    ],
                }
            },
            {
                # Combine counts and documents into a single output
                "$project": {
                    "totalDocuments": {"$arrayElemAt": ["$counts.totalDocuments", 0]},
                    "totalActive": {"$arrayElemAt": ["$counts.totalActive", 0]},
                    "totalWithLoan": {"$arrayElemAt": ["$counts.totalWithLoan", 0]},
                    "totalWithSavings": {
                        "$arrayElemAt": ["$counts.totalWithSavings", 0]
                    },
                    "documents": {
                        "$map": {
                            "input": "$documents",
                            "as": "doc",
                            "in": {
                                "_id": {"$toString": "$$doc._id"},
                                "profile": "$$doc.profile",
                                "guarantor": "$$doc.guarantor",
                                "account": "$$doc.account",
                                "socials": "$$doc.socials",
                                "organization": "$$doc.organization",
                                "education": "$$doc.education",
                            },
                        }
                    },
                }
            },
        ]
        return pipeline

    try:
        result = list(collection.aggregate(create_pipeline(20, 20)))
        return result
    except Exception as e:
        print(e)


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


def aggregate_metrics():
    data = r.get(REDIS_METRICS_KEY)
    if data:
        registry = CollectorRegistry()
        # Aggregate or process the data from Redis here
        return generate_latest(registry)
    return None


def push_metrics_to_redis():
    metrics_data = generate_latest()  # This gets the current worker's metrics
    r.set(REDIS_METRICS_KEY, metrics_data)
