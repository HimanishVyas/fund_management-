from django.db import models
from django.contrib.auth.models import AbstractUser
from users.usermanager import UserManager

# Create your models here.


class User(AbstractUser):
    username = None  # 🔑 Remove the default username field
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    email = models.EmailField(verbose_name="email", unique=True)

    REQUIRED_FIELDS = ["first_name", "last_name"]
    USERNAME_FIELD = "email"

    objects = UserManager()  # 🔧 Attach the custom manager

    def __str__(self):
        return self.email
