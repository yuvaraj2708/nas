# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    is_staff = models.BooleanField(default=False)
    # Add other fields as needed

class SecretQuestion(models.Model):
    question = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.question

class Shipment(models.Model):
    track_id = models.CharField(max_length=10, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # Other shipment-related fields

class Pricing(models.Model):
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

class Address(models.Model):
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)

class TrackingStatus(models.Model):
    status_choices = [
        ('ORDER_PLACED', 'Order Placed'),
        ('ORDER_TAKEN', 'Order Taken'),
        ('PARCEL_IN_WAREHOUSE', 'Parcel in Warehouse'),
        ('DISPATCHED_TO_DELIVERY', 'Dispatched to Delivery'),
        ('ORDER_DELIVERED', 'Order Delivered'),
    ]
    status = models.CharField(max_length=30, choices=status_choices)
    order = models.ForeignKey('Order', related_name='tracking_statuses', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    track_id = models.CharField(max_length=10, unique=True)
    material = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    pickup_address = models.CharField(max_length=255, null=True, blank=True)
    delivery_address = models.CharField(max_length=255, null=True, blank=True)
    status = models.OneToOneField('TrackingStatus', related_name='order_status', on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Material: {self.material} - Customer: {self.customer.username}"
    
class WeightPrice(models.Model):
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.weight} kg - Rs. {self.price}"
    

class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}: {self.content}'