from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart
from . common import fetch_single_product, loged_in_cart_save, user_total


@receiver(user_logged_in)
def user_logged_in_handler(sender,request,user,**kwargs):
    # print(f"User{user.username}just logged in")
    cart = request.session.get('cart', {})
    total = user_total(cart,request)
    for items in cart.values():
        product = fetch_single_product(id=items['product_id'],product_type=False)
        exists=Cart.objects.filter(user=request.user, product=product).exists()
        if not exists:
            loged_in_cart_save(request.user,product,items['product_quantity'],items['prod_total_price'],total)