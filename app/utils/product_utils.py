from ..models import Product, Category


def get_category(kwargs):
    """
    Получение категории
    :param kwargs:
    :return:
    """
    slug = kwargs.get('slug')
    category = Category.objects.get(slug=slug)
    return category


def get_product(kwargs):
    """
    Получение продукта
    :param kwargs:
    :return:
    """
    slug = kwargs.get('slug')
    product = Product.objects.get(slug=slug)
    return product


def get_products_by_category(category):
    """
    Получние всех продуктов по категории
    :param category:
    :return:
    """
    products = Product.objects.filter(category=category)
    return products


def get_all_products():
    """
    Получение всех продуктов
    :return:
    """
    all_products = Product.objects.all()
    return all_products


def get_all_categories():
    """
    Получение всех категорий
    :return:
    """
    all_categories = Category.objects.all()
    return all_categories
