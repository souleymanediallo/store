from django.test import TestCase
from products.models import Product


class ProductViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Black Tshirt', price=10, stock=10, description="New Tshirt")

    def test_product_are_shown_on_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_connexion_link_shown_when_not_logged_in(self):
        response = self.client.get('/')
        self.assertIn('Connexion', response.content.decode())