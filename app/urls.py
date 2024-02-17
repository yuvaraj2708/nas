# urls.py

from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',index,name="index"),
    path('staff/login/', StaffLoginView.as_view(), name='staff_login'),
    path('customer/login/', CustomerLoginView.as_view(), name='customer_login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Assuming you are using Django's built-in LogoutView
    path('staff/register/', staff_register, name='staff_register'),
    path('customer/register/', customer_register, name='customer_register'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('customer_dashboard/', customer_dashboard, name='customer_dashboard'),
    path('track-orders/', track_orders, name='track_orders'),
    path('customer/place_order/', place_order, name='place_order'),
    path('customer/confirm_order/', confirm_order, name='confirm_order'),
    path('customer/confirm_order/<int:order_id>/', confirm_order, name='confirm_order'),
    path('staff/change_status/<int:order_id>/', change_status, name='change_status'),
    path('register-weight/', register_weight, name='register_weight'),
    path('delete-weight/<int:weight_price_id>/', delete_weight_price, name='delete_weight_price'),
    path('weight-calculator/', weight_calculator, name='weight_calculator'),
    path('contact/',contact,name='contact'),
    path('about/',about,name='about'),
    path('customclearance/',customclearance,name='customclearance'),
    path('services/', services, name='services'),
    path('order_history/', order_history, name='order_history'),
    path('analytics_reports/',analytics_reports,name="analytics_reports"),
    path('customer-list/', customer_list, name='customer_list'),
    path('customer/<int:customer_id>/', customer_detail, name='customer_detail'),

    # Add other URLs as needed
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)