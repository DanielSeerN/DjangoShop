from ..models import Product, Category, Review, User


def get_category(kwargs):
    """
    Получение категории
    """
    slug = kwargs.get('slug')
    category = Category.objects.get(slug=slug)
    return category


def get_product(kwargs):
    """
    Получение продукта
    """
    slug = kwargs.get('slug')
    product = Product.objects.get(slug=slug)
    return product


def get_review_users(reviews):
    """
    Получение пользователей, оставивших отзыв
    """
    users = []
    for review in reviews:
        user = review.user
        users.append(user)
    return users


def get_review(username):
    """
    Получение отзыва
    """
    user = User.objects.get(username=username)
    review = Review.objects.get(user=user)
    return review


def create_review(product, user, text, score):
    """
    Создание отзыва
    """
    review = Review.objects.create(product=product, user=user, text=text, score=score)
    return review


def get_reviews(product):
    """
    Получение отзывов для продукта
    """
    reviews = Review.objects.filter(product=product)
    return reviews


def get_products_by_category(category):
    """
    Получние всех продуктов по категории
    """
    products = Product.objects.filter(category=category)
    return products


def get_all_products():
    """
    Получение всех продуктов
    """
    all_products = Product.objects.all()
    return all_products


def get_all_categories():
    """
    Получение всех категорий
    """
    all_categories = Category.objects.all()
    return all_categories
