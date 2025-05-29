import pandas as pd
from .models import OrderItem

def get_top_products(limit=5):
    qs = OrderItem.objects.select_related('product').all()

    data = []
    for item in qs:
        data.append({
            'product_name': item.product.product_name,
            'quantity': item.quantity,
            'total_price': item.price_of_purchase
        })

    df = pd.DataFrame(data)
    top_products = df.groupby('product_name').sum().sort_values(by='quantity', ascending=False).head(limit)
    return top_products.reset_index()