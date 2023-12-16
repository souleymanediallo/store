import stripe
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

from iso3166 import countries

from config import settings

ADDRES_FORMAT = """
{name}
{address_1}
{city}, {zip_code}
{country}
"""

stripe.api_key = settings.STRIPE_API_KEY


class MyUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    stripe_id = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def update_strip_id(self, new_stripe_id):
        self.stripe_id = new_stripe_id
        self.save()

    @property
    def is_staff(self):
        return self.is_admin


class ShippingAddress(models.Model):
    user: MyUser = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=2, choices=[(country.alpha2.lower(), country.name) for country in countries], default='fr')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        data = self.__dict__.copy()
        data.update(country=self.get_country_display().upper())
        return ADDRES_FORMAT.format(**data).strip("\n")

    def as_dict(self):
        return {
            "line1": self.address_1,
            "line2": self.address_2,
            "city": self.city,
            "country": self.country,
            "postal_code": self.zip_code,
        }

    def set_default(self):
        if not self.user.stripe_id:
            raise ValueError("Can't set default shipping address: no Stripe ID")

        stripe.Customer.modify(
            self.user.stripe_id,
            shipping={
                "name": self.name,
                "address": self.as_dict()
            },
            address=self.as_dict()
        )
        self.default = True
        self.save()



# countries : pip install iso3166
# https://pypi.org/project/django-countries/
