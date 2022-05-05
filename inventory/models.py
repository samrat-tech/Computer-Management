from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Part(models.Model):
    name = models.CharField(max_length=25)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} — {self.quantity} available — Rs ${self.unit_price}"

class ComputerItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    details_image = models.URLField(blank=True, null=True)
    details_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Rs {self.price})"

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    timestamp = models.DateTimeField(default=timezone.now)
    computer_item = models.ForeignKey(ComputerItem, on_delete=models.CASCADE, related_name="sales")
    
    def __str__(self):
        return f"{self.user} sold {self.computer_item} — {self.timestamp}"