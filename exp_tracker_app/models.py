from django.db import models
from django.contrib.auth.models import User

import uuid

class Item(models.db):
    name = models.CharField(required=True, max_length=30)
    price = models.DecimalField(required=True, max_digits=10, decimal_places=2)
    quantity = models.IntegerField(required=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    expense_incurred_on = models.DateField()
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.Datefield(auto_now=True)
