from django.test import TestCase
from django.urls import reverse
from api.models import CustomUser, Order, Product
from rest_framework import status
from rest_framework.test import APITestCase


class ProductDetailTestCase(APITestCase):

    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(username='yuta', password='yuta()11')
        self.user = CustomUser.objects.create_user(username='ali', password='!2345678')
        self.product = Product.objects.create(
            name='product',
            description='description 1',
            stock=12,
            price=184.35

        )
        self.url = reverse('product-detail', kwargs={'id': self.product.pk})

    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)
        self.assertEqual(response.data['description'], self.product.description)
        self.assertEqual(response.data['stock'], self.product.stock)

    def test_unauthorized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_only_admin_can_delete(self):
        # ordinary users
        self.client.login(username='ali', password='!2345678')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

        # admin users
        self.client.login(username='yuta', password='yuta()11')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_only_admin_can_put(self):
        # ordinary users
        self.client.login(username='ali', password='!2345678')
        data = {'name': 'product 1 updated'}
        product = self.client.get(self.url)
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(product.data['name'], data['name'])

        # admin users
        self.client.login(username='yuta', password='yuta()11')
        response = self.client.patch(self.url, data)
        product_updated = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product_updated.data['name'], data['name'])

    def test_only_admins_put(self):
        self.client.login(username='ali', password='!2345678')
        data = {
            'name': 'product 1 updated',
            'description': 'description 1 updated',
            'stock': 4,
            'price': 46.88
        }
        product = self.client.get(self.url)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(product.data['name'], data['name'])

        # admin users
        self.client.login(username='yuta', password='yuta()11')
        response = self.client.put(self.url, data)
        product = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product.data['name'], data['name'])
