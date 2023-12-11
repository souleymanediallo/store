from django.contrib import admin
from .models import MyUser, ShippingAddress


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')
    list_filter = ('is_admin', 'is_active', 'last_login', 'date_joined')
    search_fields = ('email',)
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)


admin.site.register(MyUser, MyUserAdmin)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    list_display = ('address_1', 'address_2', 'city', 'zip_code', 'country', 'created_at')


admin.site.register(ShippingAddress, ShippingAddressAdmin)