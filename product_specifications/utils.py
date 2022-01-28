from app.models import Product


def get_product(slug):
    product = Product.objects.get(slug=slug)
    return product
