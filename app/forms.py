# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class StaffRegistrationForm(UserCreationForm):
    # Add any additional fields for staff registration

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email', 'is_staff')

class CustomerRegistrationForm(UserCreationForm):
    secret_question = forms.ModelChoiceField(
        queryset=SecretQuestion.objects.all(),
        widget=forms.Select,
        label='Secret Question'
    )
    secret_answer = forms.CharField(max_length=255, label='Secret Answer')
    country = forms.CharField(max_length=255, label='Country/Territory')
    zip_postal = forms.CharField(max_length=20, label='ZIP/Postal')
    address1 = forms.CharField(max_length=255, label='Address 1')
    address2 = forms.CharField(max_length=255, required=False, label='Address 2')
    city = forms.CharField(max_length=255, label='City')
    state_province = forms.CharField(max_length=255, label='State/Province')
    phone = forms.CharField(max_length=20, label='Phone')

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email', 'secret_question', 'secret_answer',
                  'country', 'zip_postal', 'address1', 'address2', 'city', 'state_province', 'phone')

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['weight', 'price']

class PricingForm(forms.ModelForm):
    class Meta:
        model = Pricing
        fields = ['price_per_kg']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['material', 'weight', 'pickup_address', 'delivery_address', 'contact']


class WeightPriceForm(forms.ModelForm):
    class Meta:
        model = WeightPrice
        exclude = ['id']  # Exclude the 'id' field from the form