from django.contrib import admin
from .models import Product, Order, Cart
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'stock', 'created', 'active', 'premium')


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'ordered', 'created_at')


admin.site.register(Order, OrderAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_quantity', 'get_total', 'created_at')


admin.site.register(Cart, CartAdmin)