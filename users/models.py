from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default='user')
    bio = models.TextField(null=True, blank=True)

    def is_admin(self):
        return self.role.lower() == 'admin'

    def is_moderator(self):
        return self.role.lower() == 'moderator'
