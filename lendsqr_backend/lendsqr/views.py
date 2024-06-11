from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
import json
from .models import User, LoanModel
import os
from django.conf import settings
from datetime import datetime
from bson.objectid import ObjectId
from rest_framework.permissions import IsAuthenticated
import boto3
from dotenv import load_dotenv
from typing import Any


load_dotenv()
db = settings.MONGO_DB


@permission_classes([IsAuthenticated])
@api_view(["POST", "GET"])
def new_loan(request: dict[str, Any]) -> dict[str, str]:
    try:
        if request.method == "POST":
            account = (
                json.loads(request.POST.get("account"))
                if "account" in request.POST
                else None
            )
            guarantor = (
                json.loads(request.POST.get("guarantor"))
                if "guarantor" in request.POST
                else None
            )
            loan = (
                json.loads(request.POST.get("loan")) if "loan" in request.POST else None
            )
            email = loan["email"]
            result = db["users"].find_one(
                {
                    "profile.email": email,
                    "$or": [
                        {"profile.status": "Active"},
                        {"profile.status": "Blacklisted"},
                    ],
                }
            )
            if result:
                return Response(
                    {
                        "message": "Cannot make a new loan request while you have an active loan."
                    },
                    status=status.HTTP_409_CONFLICT,
                )
            data = {
                "account": account,
                "guarantor": guarantor,
                "loan": loan,
                "createdAt": datetime.now(),
            }

            LoanModel.model_validate(data)
            db["loans"].insert_one(data)

            return Response(
                {"message": "Loan request submitted successfully."},
                status=status.HTTP_201_CREATED,
            )

        email = request.GET.get("email")
        loans = db["loans"].find({"loan.email": email})
        all_documents = [{**doc, "_id": str(doc["_id"])} for doc in loans]
        return Response(all_documents, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def get_staff_status(request: dict[str, Any]) -> dict[str, str]:
    email = request.GET.get("email")
    user = User.objects.get(email=email)
    is_staff = user.is_staff
    return Response({"is_staff": is_staff})


@permission_classes([IsAuthenticated])
@api_view(["GET", "POST", "PUT"])
def users(request: dict[str, Any]) -> dict[str, Any]:
    try:
        if request.method == "GET":
            page = int(request.GET.get("page", 1))
            search = request.GET.get("search", "")

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
                users = db["users"].find(query)

            else:
                users = db["users"].find({"guarantor": {"$exists": True}})
            per_page = 20
            start_index = (page - 1) * per_page
            end_index = page * per_page
            all_documents = [{**doc, "_id": str(doc["_id"])} for doc in users]

            users_paginated = all_documents[start_index:end_index]
            all_users = len(all_documents)
            active = len(
                [
                    item
                    for item in all_documents
                    if item["profile"]["status"] == "Active"
                ]
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
        if request.method == "POST":
            avatar = request.FILES.get("avatar") if "avatar" in request.FILES else None
            account = (
                json.loads(request.POST.get("account"))
                if "account" in request.POST
                else None
            )
            organization = (
                json.loads(request.POST.get("organization"))
                if "organization" in request.POST
                else None
            )
            education = (
                json.loads(request.POST.get("education"))
                if "education" in request.POST
                else None
            )
            socials = (
                json.loads(request.POST.get("socials"))
                if "socials" in request.POST
                else None
            )
            guarantor = (
                json.loads(request.POST.get("guarantor"))
                if "guarantor" in request.POST
                else None
            )
            profile = (
                json.loads(request.POST.get("profile"))
                if "profile" in request.POST
                else None
            )

            if avatar:
                s3 = boto3.client(
                    "s3",
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                )
                try:
                    s3.upload_fileobj(
                        avatar,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        f"media/avatars/{avatar.name}",
                        ExtraArgs={
                            "ContentType": "image/jpeg",
                            "ContentDisposition": "inline",
                        },
                    )
                except Exception as e:
                    return Response({"error": str(e)}, status=500)
                file_dir = os.path.normpath(
                    os.path.join(settings.MEDIA_URL, "avatars", avatar.name)
                )
                file_dir = file_dir.replace("\\", "/")
                profile["avatar"] = file_dir
            data = {
                "profile": profile,
                "account": account,
                "organization": organization,
                "education": education,
                "socials": socials,
                "guarantor": guarantor,
                "createdAt": datetime.now(),
            }
            db["users"].insert_one(data)
            return Response(status=status.HTTP_201_CREATED)

        if request.method == "PUT":
            data = request.data
            user_id = data.get("user_id")
            user_id = ObjectId(user_id)
            query_criteria = {
                key: json.loads(data.get(key))
                for key in data
                if key != "user_id" and key != "avatar"
            }

            if "avatar" in data:
                avatar = request.FILES.get("avatar")
                s3 = boto3.client(
                    "s3",
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                )
                try:
                    s3.upload_fileobj(
                        avatar,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        f"media/avatars/{avatar.name}",
                        ExtraArgs={
                            "ContentType": "image/jpeg",
                            "ContentDisposition": "inline",
                        },
                    )
                except Exception as e:
                    return Response(
                        {"message": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                file_dir = os.path.normpath(
                    os.path.join(settings.MEDIA_URL, "avatars", avatar.name)
                )
                file_dir = file_dir.replace("\\", "/")

                if "profile" in data:
                    query_criteria["profile"]["avatar"] = file_dir
                else:
                    db["users"].update_one(
                        {"_id": user_id}, {"$set": {"profile.avatar": file_dir}}
                    )

            query = {}
            for key, value in query_criteria.items():
                for i, j in value.items():
                    query_key = f"{key}.{i}"
                    query[query_key] = j

            db["users"].update_one({"_id": user_id}, {"$set": query})
            document = db["users"].find({"_id": user_id})
            user = [{**doc, "_id": str(doc["_id"])} for doc in document][0]

            return Response(user, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@permission_classes([IsAuthenticated])
@api_view(["PUT"])
def update_status(request: dict[str, Any], id: str, action: str) -> dict[str, str]:
    user_id = ObjectId(id)
    db["users"].update_one({"_id": user_id}, {"$set": {"profile.status": action}})
    return Response(status=status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def advance_filter(request: dict[str, Any]) -> dict[str, Any]:
    try:
        page = int(request.GET.get("page", 1))
        organization = (
            json.loads(request.GET.get("organization"))
            if "organization" in request.GET
            else None
        )
        profile = (
            json.loads(request.GET.get("profile")) if "profile" in request.GET else None
        )
        combined = {}
        if profile:
            combined = {**profile}
        if organization:
            combined = {**combined, **organization}
        query = {"guarantor": {"$exists": True}}
        for key, value in combined.items():
            if key == "profile" and len(value) > 0:
                for i, j in value.items():
                    if j != "":
                        query_key = f"profile.{i}"
                        query[query_key] = j
            if key == "organization" and len(value) > 0:
                for i, j in value.items():
                    if j != "":
                        query_key = f"organization.{i}"
                        query[query_key] = j
        users = db["users"].find({"$and": [query]})
        per_page = 20
        start_index = (page - 1) * per_page
        end_index = page * per_page
        all_documents = [{**doc, "_id": str(doc["_id"])} for doc in users if users]
        users_paginated = all_documents[start_index:end_index]
        all_users = len(all_documents)
        active = len(
            [item for item in all_documents if item["profile"]["status"] == "Active"]
        )
        loan = len(
            [
                item
                for item in all_documents
                if int(item["account"]["loanRepayment"]) > 0
            ]
        )
        savings = len(
            [
                item
                for item in all_documents
                if int(item["account"]["accountBalance"]) > 0
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
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST", "GET"])
def assign_user_to_portfolio(request: dict[str, Any]) -> dict[str, Any]:
    try:
        if request.method == "POST":
            organization = (
                json.loads(request.POST.get("organization"))
                if "organization" in request.POST
                else None
            )
            education = (
                json.loads(request.POST.get("education"))
                if "education" in request.POST
                else None
            )
            socials = (
                json.loads(request.POST.get("socials"))
                if "socials" in request.POST
                else None
            )
            profile = (
                json.loads(request.POST.get("profile"))
                if "profile" in request.POST
                else None
            )
            data = {
                "profile": profile,
                "organization": organization,
                "education": education,
                "socials": socials,
                "createdAt": datetime.now(),
            }
            db["users"].insert_one(data)
            return Response(status=status.HTTP_201_CREATED)
        if request.method == "GET":
            email = request.GET.get("email")
            document = db["users"].find({"profile.email": email})
            portfolio = [{**doc, "_id": str(doc["_id"])} for doc in document][0]
            return Response(portfolio, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
