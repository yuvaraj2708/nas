from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Order)
admin.site.register(WeightPrice)
admin.site.register(SecretQuestion)
admin.site.register(CustomUser)

