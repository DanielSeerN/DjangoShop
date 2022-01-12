from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

User = get_user_model()  # Для пользователя используем встроенную модель


class Category(models.Model):
    """
    Модель для категории продкутов
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    """
    Модель для продукта
    """
    title = models.CharField(max_length=255, verbose_name='Имя продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)

    def get_absolute_url(self):
        """
        Функция для формирования url продукта
        :return:
        """
        return reverse('product', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    """
    Модель для добавления продукта в корзину
    """
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, )
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Конечная цена', null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    """
    Модель для корзины
    """
    owner = models.ForeignKey(
        'Customer',
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
        null=True
    )

    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Финальная цена', null=True)
    in_order = models.BooleanField(default=False)
    for_anonym_user = models.BooleanField(default=False)


class Customer(models.Model):
    """
    Модель для покупателя
    """
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, verbose_name='Номер телефона', null=True, blank=True)
    adress = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return f'Покупатель {self.user.first_name, self.user.last_name}'


class Order(models.Model):
    """
    Модель для заказа
    """
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (  # Статусы заказа
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (  # Тип оплаты заказы
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=255, verbose_name='Имя покупателя', null=True, blank=True)
    customer_last_name = models.CharField(max_length=255, verbose_name='Имя покупателя', null=True, blank=True)
    adress = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    phone = models.CharField(max_length=255, verbose_name='Номер телефона', null=True, blank=True)
    order_status = models.CharField(max_length=255, verbose_name='Статус заказа', choices=STATUS_CHOICES,
                                    default=STATUS_NEW)
    type_of_order = models.CharField(max_length=255, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES,
                                     default=BUYING_TYPE_DELIVERY)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    date_of_order = models.DateTimeField(verbose_name='Время создания заказа', default=timezone.now)
    date_of_receiveing = models.DateField(verbose_name='Время получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)
