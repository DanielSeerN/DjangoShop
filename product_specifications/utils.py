from ..app.models import Product
from .models import CategorySpecification, ProductSpecification


def get_product(slug):
    product = Product.objects.get(slug=slug)
    return product
