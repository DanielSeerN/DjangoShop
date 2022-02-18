import unittest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory

from unittest import mock, main

from .models import Product, Category, User, Customer, Cart, CartProduct, Order
from .utils.cart_utils import refresh_cart
from .views import AddToCartView, MainPageView, RemoveFromCartView, ChangeProductQuantityView, LoginView, CartView, \
    OrderView, CustomerOrdersView, RegistrationView


class AppTest(TestCase):
    """
    Тесты приложения
    """

    def setUp(self) -> None:
        """
        Функция для создания необходимых объектов для тестирования
        """
        image = SimpleUploadedFile('pngwing.png', content=b'', content_type='image/png')
        self.factory = RequestFactory()
        self.category = Category.objects.create(title='Стиральные машины', slug='peifanpief')
        self.product = Product.objects.create(
            title='Dishwasher',
            price=30000,
            description='whatever',
            image=image,
            slug='dishwasher',
            category=self.category
        )
        self.user = User.objects.create_user(username='кто-то', password='password')
        self.user1 = User.objects.create(username='что-то', password='password')
        self.customer = Customer.objects.create(phone='+79187233289',
                                                adress='спб',
                                                user=self.user
                                                )
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(product=self.product, user=self.customer, cart=self.cart)
        self.order = Order.objects.create(cart=self.cart, customer=self.customer)

    def test_add_to_cart(self):
        """
        Функция тестирования добавления продукта в корзину
        """
        self.cart.products.add(self.cart_product)
        refresh_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count(), 1)

    def test_response_from_add_to_cart(self):
        """
        Функция тестирования ответа от представления добавления продукта в корзину
        """
        request = self.factory.get('')
        request.user = self.user
        response = AddToCartView.as_view()(request, slug='dishwasher')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')

    def test_mock_homepage(self):
        """
        Функция тестирования ответа от главной страницы
        """
        mock_data = mock.Mock(status_code=555)
        with mock.patch('app.views.MainPageView.get', return_value=mock_data) as mock_:
            request = self.factory.get('')
            request.user = self.user
            response = MainPageView.as_view()(request)
            self.assertEqual(response.status_code, 555)

    def test_remove_from_cart(self):
        """
        Функция тестирования удаления продукта из корзины
        """
        self.cart.products.add(self.cart_product)
        refresh_cart(self.cart)
        self.assertEqual(self.cart.products.count(), 1)
        self.cart.products.remove(self.cart_product)
        refresh_cart(self.cart)
        self.assertEqual(self.cart.products.count(), 0)

    def test_response_from_remove_from_cart(self):
        """
        Функция тестирования ответа от представления удаления продукта из корзины
        """
        request = self.factory.get('')
        request.user = self.user
        response = RemoveFromCartView.as_view()(request, slug='dishwasher')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')

    def test_product_quantity_change(self):
        """
        Функция тестирования изменения количества продуктов
        """
        self.cart.products.add(self.cart_product)
        self.cart_product.quantity = 2
        self.assertEqual(self.cart_product.quantity, 2)
        self.cart_product.quantity -= 1
        self.assertEqual(self.cart_product.quantity, 1)

    def response_from_product_quantity_change(self):
        """
        Функция тестирования ответа от представления изменения количества продуктов
        """
        request = self.factory.get('')
        request.user = self.user
        response = ChangeProductQuantityView.as_view()(request, slug='dishwasher')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')

    def test_response_from_cart(self):
        """
        Функция тестирования ответа от представления корзины:
        """
        request = self.factory.get('/cart')
        request.user = self.user
        response = CartView.as_view()(request, )
        self.assertEqual(response.status_code, 200)

    def test_response_from_orders(self):
        """
        Функция тестирования ответа от представления заказа:
        """
        request = self.factory.get('')
        request.user = self.user
        response = OrderView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_response_customer_orders(self):
        """
        Функция тестирования ответа от представления заказов покупателя
        """
        request = self.factory.get('/orders/')
        request.user = self.user
        response = CustomerOrdersView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_response_from_login(self):
        """
        Функция тестирования ответа от представления входа в аккаунт
        """
        request = self.factory.get('/login/')
        request.user = self.user
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        """
        Функция тестирования регистрации
        """
        user = User.objects.create_user(username='никто', password='password')
        user.phone = '+123214514'
        user.adress = 'spb'
        customer = Customer.objects.create(user=user, phone=user.phone, adress=user.adress)
        self.assertTrue(self.client.login(username='никто', password='password'))
        self.assertTrue(customer)

    def test_login(self):
        """
        Функция тестирования входа
        """
        self.assertTrue(self.client.login(username='кто-то', password='password'))

    def test_response_from_registration(self):
        """
        Функция тестирования ответа от представления регистрации
        """
        request = self.factory.get('/registration/')
        request.user = self.user
        response = RegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)
