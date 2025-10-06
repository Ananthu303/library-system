# Create your models here.
from .managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserType(models.IntegerChoices):
        SUPERADMIN = 1, "SuperAdmin"
        LIBRARIAN = 2, "Librarian"
        USER = 3, "User"

    name = models.CharField(max_length=150)
    user_type = models.PositiveSmallIntegerField(choices=UserType.choices, default=UserType.USER)
    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "A user with this email already exists.",
            "invalid": "Enter a valid email address.",
        },
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_user_type_display()})"
