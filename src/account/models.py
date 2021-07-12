from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, PermissionsMixin,AbstractBaseUser
from django.utils import timezone

class AccountManager(BaseUserManager):

    def create_user(self, email, password, firstname, lastname, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, firstname, lastname, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, firstname, lastname, **extra_fields)



class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = AccountManager()

    def __str__(self):
        return self.email