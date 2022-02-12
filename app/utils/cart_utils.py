from django.db import models
from ..models import Product, CartProduct, Customer


def refresh_cart(cart):
    """
    Обновление цены продукта и его количества.
    """
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Sum('quantity'))
    if cart_data.get('quantity__sum'):
        cart.total_products = cart_data['quantity__sum']
    else:
        cart.total_products = 0
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.save()


def get_cart_product(self, kwargs, add_to_cart=False):
    """
    Получение или создание продукта для корзины
    """
    product_slug = kwargs.get('slug')
    product = Product.objects.get(slug=product_slug)
    if add_to_cart:
        cart_product, created = CartProduct.objects.get_or_create(user=self.cart.owner, cart=self.cart,
                                                                  product=product
                                                                  )
        return cart_product, created
    else:
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart,
                                               product=product
                                               )
    return cart_product


def create_customer(user):
    """
    Создание покупателя
    """
    customer = Customer.objects.create(user=user, phone=user.phone, adress=user.address)
    return customer
