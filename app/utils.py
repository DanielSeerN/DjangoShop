from django.db import models


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
