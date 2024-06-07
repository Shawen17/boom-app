from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from pydantic import BaseModel, Field


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    state = models.CharField(max_length=50, default="Lagos")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "state", "password"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


class BasicAttribute(BaseModel):
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    bvn: int


class LoanAttributes(BasicAttribute):
    amount: int
    loanRepayment: str
    duration: int
    accountNumber: int
    bank: str


class GuarantorAttributes(BaseModel):
    guaFirstName: str
    guaLastName: str
    guaNumber: str
    guaAddress: str
    guaGender: str
    relationship: str


class AccountAttributes(BaseModel):
    accountName: str | None = Field(default=None)
    loanRepayment: str
    accountNumber: int
    bank: str
    accountBalance: int
    monthlyIncome: list[int]


class LoanModel(BaseModel):
    account: AccountAttributes
    loan: LoanAttributes
    guarantor: GuarantorAttributes


class ProfileAttribute(BasicAttribute):
    userName: str
    address: str
    gender: str
    status: str
    avatar: str


class OrganizationAttribute(BaseModel):
    orgName: str
    orgNumber: str
    officeEmail: str
    employmentStatus: str
    sector: str
    duration: str


class EducationAttribute(BaseModel):
    level: str


class SocialAttribute(BaseModel):
    twitter: str
    facebook: str
    instagram: str


class UserProfileModel(BaseModel):
    profile: ProfileAttribute
    guarantor: GuarantorAttributes
    socials: SocialAttribute
    organization: OrganizationAttribute
    education: EducationAttribute
    account: AccountAttributes
