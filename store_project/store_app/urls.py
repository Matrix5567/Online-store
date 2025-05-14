from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logged-in-check',views.check_is_logged_in,name='logged_in_check'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('shop/<str:key>/', views.shop, name='shop'),
    path('single/<int:id>/', views.single, name='single'),
    path('cart/', views.cartpage, name='cartpage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('onload/', views.onload, name='onload'),
    path('quantity/<str:action>/<int:id>/',views.quantity,name='quantity'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('create-checkout-session/',views.checkout,name='checkout'),
    path('success/', views.success, name='success'),
    path('search/', views.search, name='search'),
    path('filter/', views.filter, name='filter'),
    path('cancel/', views.cancel, name='cancel'),
    path('admindash/', views.admin_dash, name='admin_dash'),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('admin_add_product/', views.addproduct, name='admin_add_product'),
    # path('stripe/webhook/', views.stripe_webhook, name='stripe-webhook'),
]
