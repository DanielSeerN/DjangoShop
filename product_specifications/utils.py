from app.models import Product

from .models import ProductSpecification, CategorySpecification


def get_product(slug):
    """
    Получение продукта
    """
    product = Product.objects.get(slug=slug)
    return product


def get_product_specification(product, specification_category):
    """
    Получение спецификации продукта по категории спефикации
    """
    specification = ProductSpecification.objects.get(product=product,
                                                     specification=specification_category,
                                                     )
    return specification


def get_product_specifications(product):
    """
    Получение всех спецификация продукта
    """
    specifications = ProductSpecification.objects.filter(product=product).all()
    return specifications


def get_specification_categories(product_category):
    """
    Получение всех категорий специфификаций по категории продукта
    """
    specification_categories = CategorySpecification.objects.filter(category=product_category).all()
    return specification_categories


def create_product_specification(value, product, specification_category):
    """
    Создание спецификации для продукта
    """
    product_specification = ProductSpecification.objects.create(value=value,
                                                                category=product.category,
                                                                product=product,
                                                                specification=specification_category)
    return product_specification

