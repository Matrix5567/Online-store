from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('shop/<str:key>/', views.shop, name='shop'),
    path('single/<int:id>/', views.single, name='single'),
]
