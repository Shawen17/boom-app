from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime,date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.utils import timezone



class User(AbstractUser):
    username = None
    email=models.EmailField(_('email address'),unique=True)
    state=models.CharField(max_length=50,default='Lagos')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','state','password']

    class Meta:
        verbose_name=_('user')
        verbose_name_plural=_('users')

    objects=UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name