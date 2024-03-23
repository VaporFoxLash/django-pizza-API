from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email address is required"))

        email = self.normalize_email(email)
        new_user = self.model(email=email, **extra_fields)
        new_user.set_password(password)
        new_user.save()

        return new_user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("SuperUser should have is_staff True"))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("SuperUser should have is_superuser True"))

        if extra_fields.get('is_active') is not True:
            raise ValueError(_("SuperUser should have is_active True"))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username=models.CharField(max_length=25, unique=True)
    email=models.CharField(max_length=80, unique=True)
    phone_number=PhoneNumberField(null=False, unique=True)

    # Override the groups and user_permissions fields
    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name=_('groups'),
    #     blank=True,
    #     help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
    #     related_name="%(app_label)s_%(class)s_related",
    #     related_query_name="%(app_label)s_%(class)ss",
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name=_('user permissions'),
    #     blank=True,
    #     help_text=_('Specific permissions for this user.'),
    #     related_name="%(app_label)s_%(class)s_related",
    #     related_query_name="%(app_label)s_%(class)ss",
    # )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return f"<User {self.email}>"