from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='product_list'),
]