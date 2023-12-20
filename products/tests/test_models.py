from django.test import TestCase
from products.models import Product


class ProductModelTest(TestCase):
    def test_product_slug_is_automatically_generated(self):
        self.product = Product.objects.create(name='Black Tshirt', price=10, stock=10, description="New Tshirt")
        self.assertEqual(self.product.slug, 'black-tshirt')