from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart
from . common import cart_total_price, fetch_single_product


@receiver(user_logged_in)
def user_logged_in_handler(sender,request,user,**kwargs):
    # print(f"User{user.username}just logged in")
    cart = request.session.get('cart', {})
    total = cart_total_price(cart,request=False)
    for items in cart.values():
        product = fetch_single_product(id=items['product_id'],product_type=False)
        Cart(user=request.user,product=product,
                    quantity=items['product_quantity'],product_total_price=items['prod_total_price'],
                    cart_total_price=total).save()
    print("db synced successfully")