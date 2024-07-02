from django.db import models

import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

from django.contrib.auth.models import BaseUserManager
from django.db.models import Q


class CustomUserManager(BaseUserManager):
    def get_by_username_or_email(self, identifier):
        print(f"Attempting to find user with identifiers: {identifier}")
        
        user = self.get(
            Q(username=identifier) | 
            Q(email=identifier)
        )
        return user
        
        

class User(AbstractUser):
    name = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)  # Ensure unique email for registration

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Add 'email' to required fields


User = get_user_model()

class Item(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    expense_incurred_on = models.DateField()
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)

class ItemDocument(models.Model):
    document = models.FileField(upload_to='documents')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
