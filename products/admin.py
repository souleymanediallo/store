from django.contrib import admin
from .models import Product, Order, Cart
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)


class CartAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cart, CartAdmin)