import uuid
from .models import * 

def generate_unique_track_id():
    # Generate a unique track ID using uuid
    return str(uuid.uuid4())[:10]


def calculate_price(weight):
    # Assuming weight is in kg
    weight_prices = WeightPrice.objects.filter(weight__gte=weight).order_by('weight')
    
    if weight_prices.exists():
        # Use the price from the first matching weight or implement your own logic
        return weight_prices.first().price
    
    return 0.0