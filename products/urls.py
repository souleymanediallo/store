from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='product_list'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart-delete/', views.cart_delete, name='cart_delete'),
    path('update-quantity/', views.update_quantity, name='update-quantity'),
    # stripe
    path('checkout/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.checkout_success, name='checkout-success'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe-webhook'),
]