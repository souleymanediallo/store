from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('address/', views.address, name='address'),
    path('address/set-default-shipping/<int:pk>/', views.set_default_shipping, name='set-default-shipping'),
    path('address/delete/<int:pk>/', views.address_delete, name='address-delete'),
]