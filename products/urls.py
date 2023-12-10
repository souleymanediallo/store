from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='product_list'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart-delete/', views.cart_delete, name='cart_delete'),
]