from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from . common import cart_total_price, fetch_single_product, loged_in_cart_save


@receiver(user_logged_in)
def user_logged_in_handler(sender,request,user,**kwargs):
    # print(f"User{user.username}just logged in")
    cart = request.session.get('cart', {})
    total = cart_total_price(cart,request)
    for items in cart.values():
        product = fetch_single_product(id=items['product_id'],product_type=False)
        loged_in_cart_save(request.user,product,items['product_quantity'],items['prod_total_price'],total)
    print("db synced successfully")