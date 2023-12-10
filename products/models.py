from django.db import models
from django.db.models.fields import SlugField
from django.urls import reverse
from django.utils import timezone

from config.settings import AUTH_USER_MODEL


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total(self):
        return f"{self.quantity} * {self.product.price}"

    def get_total_quantity(self):
        return self.quantity

    def delete_order(self):
        self.delete()

    def get_total_price(self):
        return self.product.price * self.quantity

    def get_total_quantity(self):
        return self.quantity


class Cart(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} cart"

    def get_total(self):
        total = 0
        for order in self.orders.all():
            total += order.product.price * order.quantity
        return total

    def get_total_quantity(self):
        total_quantity = 0
        for order in self.orders.all():
            total_quantity += order.quantity
        return total_quantity

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.created_at = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)





