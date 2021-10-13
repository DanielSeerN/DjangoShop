from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone

USER = get_user_model()


def get_url_for_product(object, viewname):
    ct_model = object.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': object.slug})


class LatestProductsManager:
    @staticmethod
    def get_mainpage_products(*args, **kwargs):
        priority_models = kwargs.get('priority_models')
        products = []
        if priority_models:
            ct_models = ContentType.objects.filter(model=priority_models)
            if ct_models.exists():
                for ct_model in ct_models:
                    needed_products = ct_model.model_class()._base_manager.all().order_by('id')[:5]
                    products.extend(needed_products)
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatestProducts:
    objects = LatestProductsManager()


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255, verbose_name='Имя продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)

    def get_ct_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return get_url_for_product(self, 'product')

    def __str__(self):
        return self.title


class SmartPhone(Product):
    os = models.CharField(max_length=255, verbose_name='ОС')
    diagonal = models.CharField(max_length=30, verbose_name='Диагональ')
    processor = models.CharField(max_length=255, verbose_name='Процессор')
    ram = models.CharField(max_length=30, verbose_name='Оперативная память')

    class Meta:
        verbose_name_plural = 'Smartphones'


class TV(Product):
    diagonal = models.CharField(max_length=30, verbose_name='Диагональ')
    resolution = models.CharField(max_length=30, verbose_name='Разрешение')
    brightness = models.CharField(max_length=30, verbose_name='Частота обновления')

    class Meta:
        verbose_name_plural = 'TVs'


class WashingMachine(Product):
    version = models.CharField(max_length=30, verbose_name='Модель')
    type_of_machine = models.CharField(max_length=30, verbose_name='Вид')
    weight = models.CharField(max_length=30, verbose_name='Вес')

    class Meta:
        verbose_name_plural = 'Washing machines'


class Conditioner(Product):
    version = models.CharField(max_length=30, verbose_name='Модель')
    type_of_conditioner = models.CharField(max_length=30, verbose_name='Вид')
    weight = models.CharField(max_length=30, verbose_name='Вес')
    filters = models.CharField(max_length=30, verbose_name='Фильтры')

    class Meta:
        verbose_name_plural = 'Conditioners'


class PhotoCamera(Product):
    version = models.CharField(max_length=30, verbose_name='Модель')
    type_of_matrix = models.CharField(max_length=30, verbose_name='Тип матрицы')
    megapixels = models.CharField(max_length=30, verbose_name='Мегапиксели')

    class Meta:
        verbose_name_plural = 'Photocameras'


class VideoGameConsole(Product):
    four_k_support = models.CharField(max_length=20)
    SSD = models.CharField(max_length=5, verbose_name='Объём SSD')
    warranty = models.CharField(max_length=10, verbose_name='Гарантия')

    class Meta:
        verbose_name_plural = 'Videogame consoles'


class LawnMover(Product):
    cutting_system = models.CharField(max_length=30, verbose_name='Режущая система')
    rotational_moment = models.CharField(max_length=30, verbose_name='Обороты')
    engine_capacity = models.CharField(max_length=30, verbose_name='Мощность двигателя')

    class Meta:
        verbose_name_plural = 'Lawnmovers'


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Конечная цена', null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Финальная цена', null=True)
    in_order = models.BooleanField(default=False)
    for_anonym_user = models.BooleanField(default=False)
    #
    # def __str__(self):
    #     return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(USER, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, verbose_name='Номер телефона', null=True, blank=True)
    adress = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return f'Покупатель {self.user.first_name, self.user.last_name}'


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=255, verbose_name='Имя покупателя', null=True, blank=True)
    customer_last_name = models.CharField(max_length=255, verbose_name='Имя покупателя', null=True, blank=True)
    adress = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    phone = models.CharField(max_length=255, verbose_name='Номер телефона', null=True, blank=True)
    order_status = models.CharField(max_length=255, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    type_of_order = models.CharField(max_length=255, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_DELIVERY)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    date_of_order = models.DateTimeField(verbose_name='Время создания заказа', default=timezone.now)
    date_of_receiveing = models.DateField(verbose_name='Время получения заказа', default=timezone.now)
    def __str__(self):
        return str(self.id)

