from dotenv import load_dotenv

import os
import smtplib

from .models import Product

load_dotenv()
EMAIL = os.getenv('email_host_user')
PASSWORD = os.getenv('email_host_password')


def send_notification_email(user_email, user_name, user_last_name):
    """
    Прислать письмо-оповещение
    """
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, f'{user_email}', 'Hello! We have received your message')
    server.quit()


def send_email_to_host(user_email, email_text):
    """
    Прислать письмо в почтовый хост-ящик
    """
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, EMAIL, f'{email_text} from {user_email}')
    server.quit()


def process_search_term(search_term):
    """
    Формирование поискового запроса
    """
    search_term_words = search_term.split(' ')
    search_slug = '*'.join(search_term_words)
    return search_slug


def process_search_slug(kwargs):
    """
    Обработка поискового запроса
    """
    search_slug = kwargs.get('slug')
    search_term_words = search_slug.split('*')
    return search_term_words


def search_products(all_products, search_words):
    """
    Поиск продуктов по запросу
    """
    searched_products = []
    for product in all_products:
        for search_word in search_words:
            if search_word in product.title:
                searched_product = Product.objects.get(title=product.title)
                searched_products.append(searched_product)
    return searched_products
