from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import ProductSpecification, CategorySpecification
from .views import FindSpecification, CreateSpecification, UpdateSpecification, FindSpecificationPage, \
    SpecificationPage

from app.models import Product, Category, User


class ProductSpecificationTest(TestCase):
    def setUp(self) -> None:
        """
        Функция для создания необходимых объектов для тестирования
        """
        image = SimpleUploadedFile('pngwing.jpg', content=b'', content_type='image/jpg')
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
        self.specification_category = CategorySpecification(category=self.category,
                                                            specification='Вес',
                                                            unit='кг'
                                                            )
        self.product_specification = ProductSpecification(category=self.category,
                                                          product=self.product,
                                                          specification=self.specification_category,
                                                          value='54'
                                                          )
        self.user = User.objects.create_user(username='кто-то', password='password')

    def response_from_FindSpecificationPage(self):
        request = self.factory.get('')
        request.user = self.user
        response = FindSpecificationPage.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'specification/')

    def response_from_SpecificationPage(self):
        request = self.factory.get('')
        request.user = self.user
        response = SpecificationPage.as_view()(request, slug=self.product.slug)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'specification/')

    def response_from_FindSpecification(self):
        request = self.factory.get('')
        request.user = self.user
        response = FindSpecification.as_view()(request, slug=self.product.slug)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'specification/')

    def response_from_CreateSpecification(self):
        request = self.factory.get('')
        request.user = self.user
        response = CreateSpecification.as_view()(request, slug=self.product.slug)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'specification/')

    def response_from_UpdateSpecification(self):
        request = self.factory.get('')
        request.user = self.user
        response = UpdateSpecification.as_view()(request, slug=self.product.slug)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'specification/')

