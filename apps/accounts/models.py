from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django_resized import ResizedImageField

from apps.accounts.utils import user_photo_directory_path


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, is_active=True, is_staff=False, is_superuser=False):
        if not first_name:
            raise ValueError("Please, type your first name.")
        if not last_name:
            raise ValueError("Please type your last name.")
        if not email:
            raise ValueError('User have to an email address!')
        if not password:
            raise ValueError('User must have a password!')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_staff(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_superuser=True,
            is_staff=True,
        )
        return user


class User(AbstractUser):

    photo = ResizedImageField(
        size=[400, 400],
        quality=100,
        upload_to=user_photo_directory_path,
        null=True,
        blank=True
    )

    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"
        db_table = "db_user"
