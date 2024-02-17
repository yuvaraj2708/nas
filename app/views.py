# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .utils import generate_unique_track_id
from django.db.models import Q
import matplotlib.pyplot as plt
from io import BytesIO
import base64


class StaffLoginView(LoginView):
    template_name = 'staff_login.html'

    def get_success_url(self):
        return reverse_lazy('staff_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())

class CustomerLoginView(LoginView):
    template_name = 'customer_login.html'

    def get_success_url(self):
        return reverse_lazy('customer_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())


@user_passes_test(lambda u: u.is_staff)
def staff_dashboard(request):
    # Filter orders excluding 'ORDER_DELIVERED' status
    orders = Order.objects.exclude(status__status='ORDER_DELIVERED')
    return render(request, 'staff_dashboard.html', {'orders': orders})

@login_required
def customer_dashboard(request):
    user_instance = None

    # Check if the user is authenticated
    if request.user.is_authenticated:
        user_instance = get_user_model().objects.get(pk=request.user.pk)

    # Filter orders based on the user instance
    orders = Order.objects.filter(customer=user_instance) if user_instance else []

    return render(request, 'customer_dashboard.html', {'orders': orders})

def staff_register(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('customer_dashboard')  # Redirect to the home page
    else:
        form = StaffRegistrationForm()

    return render(request, 'staff_register.html', {'form': form})

def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or login page
            return redirect('customer_login')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'customer_register.html', {'form': form})

@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            if 'preview' in request.POST:
                # If 'Preview Details' button is clicked, render a preview template
                return render(request, 'preview_order.html', {'form': form})
            else:
                # If 'Place Order' button is clicked, save the order and redirect
                order = form.save(commit=False)
                order.customer = request.user
                order.track_id = generate_unique_track_id()
                order.save()
                return redirect('confirm_order', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'place_order.html', {'form': form})


def change_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order = Order.objects.get(pk=order_id)

        # Create a new tracking status entry for the order
        tracking_status = TrackingStatus.objects.create(status=new_status, order=order)

        # Update the order status to the latest tracking status
        order.status = tracking_status
        order.save()

        messages.success(request, 'Order status changed successfully.')
        return redirect('staff_dashboard')

    # Redirect to staff dashboard if the request method is not POST
    return redirect('staff_dashboard')


def track_orders(request):
    if request.method == 'POST':
        track_id = request.POST.get('track_id')
        try:
            order = Order.objects.get(track_id=track_id)
            tracking_statuses = TrackingStatus.objects.filter(order=order)
            return render(request, 'track_orders.html', {'order': order, 'statuses': tracking_statuses})
        except Order.DoesNotExist:
            messages.error(request, 'Invalid tracking ID or order not found.')
    return render(request, 'track_orders.html')

def confirm_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    # Perform actions related to confirming the order, if needed

    # Redirect to the customer dashboard
    return redirect('customer_dashboard')


def register_weight(request):
    if request.method == 'POST':
        form = WeightPriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_weight')
    else:
        form = WeightPriceForm()

    # Fetch all registered weight details for display and deletion
    weight_prices = WeightPrice.objects.all()

    return render(request, 'register_weight.html', {'form': form, 'weight_prices': weight_prices})


def weight_calculator(request):
    if request.method == 'POST':
        weight = float(request.POST['weight'])
        price = WeightPrice.objects.filter(weight__lte=weight).order_by('-weight').first().price
        return render(request, 'weight_calculator.html', {'weight': weight, 'price': price})
    return render(request, 'weight_calculator.html')

def delete_weight_price(request, weight_price_id):
    weight_price = get_object_or_404(WeightPrice, id=weight_price_id)
    weight_price.delete()
    return redirect('register_weight')


def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'service.html')

def customclearance(request):
    return render(request,'customclearance.html')

def order_history(request):
    # Get all orders excluding the ones with status 'ORDER_DELIVERED'
    orders = Order.objects.all()

    # Search functionality
    query = request.GET.get('q')
    if query:
        # Perform case-insensitive search on customer name and order status
        orders = orders.filter(Q(customer__username__icontains=query) | Q(status__status__icontains=query))

    context = {'orders': orders}
    return render(request, 'order_history.html', context)

@user_passes_test(lambda u: u.is_staff)
def customer_list(request):
    customers = get_user_model().objects.filter(is_staff=False)
    return render(request, 'customer_list.html', {'customers': customers})

def customer_detail(request, customer_id):

    # Assuming staff_user is the logged-in staff user
    staff_user = request.user

    # Get the customer object
    customer = get_object_or_404(get_user_model(), id=customer_id)

    # Get the messages between staff and customer
    messages = Message.objects.filter(
        (Q(sender=staff_user, receiver=customer) | Q(sender=customer, receiver=staff_user))
    ).order_by('timestamp')

    context = {
        'customer': customer,
        'messages': messages,
        'staff_user': staff_user,
    }

    return render(request, 'customer_detail.html', {'customer': customer})





def get_total_customers():
    # Query the database to get the total number of customers
    return get_user_model().objects.count()

def get_total_orders():
    # Query the database to get the total number of orders
    return Order.objects.count()

def get_order_statuses():
    # Query the database to get the count of each order status
    order_statuses = Order.objects.values('status__status').annotate(count=models.Count('id'))
    return {status['status__status']: status['count'] for status in order_statuses}

@user_passes_test(lambda u: u.is_staff)
def analytics_reports(request):
    # Your analytics logic here
    total_customers = get_total_customers()
    total_orders = get_total_orders()
    order_statuses = get_order_statuses()

    # Visualization using Matplotlib
    labels = ['Total Customers', 'Total Orders'] + list(order_statuses.keys())
    values = [total_customers, total_orders] + list(order_statuses.values())

    plt.figure(figsize=(8, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Analytics Report')
    
    # Convert plot to bytes
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convert bytes to base64 encoding
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return render(request, 'analytics_reports.html', {'image_base64': image_base64})