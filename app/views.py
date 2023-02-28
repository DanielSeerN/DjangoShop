from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Product
from .services import send_email_to_host, send_notification_email, process_search_term, process_search_slug, \
    search_products
<<<<<<< HEAD
from .forms import OrderForm, LoginForm, RegistrationForm, SendQuestionMail, ReviewForm
from .utils.order_utils import get_customer_orders
from .utils.product_utils import get_category, get_products_by_category, get_all_categories, get_all_products, \
    get_product, get_reviews, create_review, get_review_users, get_review
from .utils.cart_utils import refresh_cart, get_cart_product, create_customer
=======
from .forms import OrderForm, LoginForm, RegistrationForm, SendQuestionMail
from .utils.email_utils import clean_email_form
from .utils.order_utils import get_customer_orders, make_order_form_clean
from .utils.product_utils import get_category, get_products_by_category, get_all_categories, get_all_products, \
    get_product
from .utils.cart_utils import refresh_cart, get_cart_product
>>>>>>> 1daa6aece23b5684f5be666f6e9f8fa7053afb78
from .utils.mixins import CartMixin
from .utils.user_utils import authenticate_user, register_user

from product_specifications.utils import get_product_specifications


class ProductView(CartMixin):
    """
    Представление для продукта
    """

    def get(self, request, **kwargs):
        product = get_product(kwargs)
        categories = get_all_categories()
        specifications = get_product_specifications(product)
        reviews = get_reviews(product)
        review_users = get_review_users(reviews)
        review_form = ReviewForm(request.POST or None)
        context = {
            'product': product,
            'details': specifications,
            'reviews': reviews,
            'review_form': review_form,
            'review_users': review_users,
        }
        return render(request, 'app/product.html', context)


<<<<<<< HEAD
class ReviewView(View):
    """
    Представление для создания отзывов
    """

    def post(self, request):
        slug = str(request.POST.get('slug_hidden'))
        product = Product.objects.get(slug=slug)
        form = ReviewForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            review = create_review(product, request.user, form.cleaned_data['text'], form.cleaned_data['score'])
            review.save()
        return redirect(f'/products/{slug}')


class DeleteReview(View):
    """
    Представление для удаления отзыва
    """

    def get(self, request, **kwargs):
        slug = kwargs.get('slug')
        review = get_review(username=request.user.username)
        review.delete()
        return redirect(f'/products/{slug}')


=======
>>>>>>> 1daa6aece23b5684f5be666f6e9f8fa7053afb78
class MainPageView(CartMixin, View):
    """
    Главная страница.
    """

    def get(self, request):
        products = get_all_products()
        categories = get_all_categories()
        context = {
            'products': products,
            'cart': self.cart,
            'categories': categories,
        }

        return render(request, 'app/index.html', context)


class RegistrationView(CartMixin, View):
    """
    Регистрация пользователя.
    """

    def get(self, request):
        form = RegistrationForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form
        }
        return render(request, 'app/registration.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            user = register_user(form)
            user = authenticate(username=user.username, password=form.cleaned_data['password'])

            login(request, user)
            return redirect('/')
        context = {
            'cart': self.cart,
            'form': form
        }

        return render(request, 'app/registration.html', context)


class LoginView(CartMixin, View):
    """
    Аутентификация пользователя.
    """

    def get(self, request):
        form = LoginForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form
        }

        return render(request, 'app/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user_info = authenticate_user(form)
            user = authenticate(username=user_info[0], password=user_info[1])
            if user:
                login(request, user)
                return redirect('/')
        context = {
            'cart': self.cart,
            'form': form
        }

        return render(request, 'app/login.html', context)


class CategoryView(CartMixin, View):
    """
    Отображение продуктов, принадлежащих одной категории.
    """

    def get(self, request, **kwargs):
        category = get_category(kwargs)
        products = get_products_by_category(category)
        categories = get_all_categories()
        context = {
            'products': products,
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'app/category_products.html', context)


class CartView(CartMixin, View):
    """
    Корзина пользователя.
    """

    def get(self, request):
        categories = get_all_categories()
        if self.cart.final_price is None:
            self.cart.final_price = 0
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'app/cart.html', context)


class AddToCartView(CartMixin, View):
    """
    Добавление продукта в корзину пользователя.
    """

    def get(self, **kwargs):
        cart_product, created = get_cart_product(self, kwargs, add_to_cart=True)
        if created:
            self.cart.products.add(cart_product)
        cart_product.final_price = cart_product.product.price * cart_product.quantity
        cart_product.save()
        refresh_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class RemoveFromCartView(CartMixin, View):
    """
    Удаление продукта из корзины.
    """

    def get(self, **kwargs):
        cart_product = get_cart_product(self, kwargs)
        self.cart.products.remove(cart_product)
        cart_product.delete()
        refresh_cart(self.cart)
        return redirect('/cart/')


class ChangeProductQuantityView(CartMixin, View):
    """
    Изменение кол-ва продукта.
    """

    def post(self, request, **kwargs):
        cart_product = get_cart_product(self, kwargs)
        quantity = int(request.POST.get('qty'))
        cart_product.quantity = quantity
        cart_product.final_price = cart_product.product.price * cart_product.quantity
        cart_product.save()
        refresh_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Количество товара изменено')
        return HttpResponseRedirect('/cart/')


class OrderView(CartMixin, View):
    """
    Заполение заказа через форму.
    """

    def get(self, request):
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form
        }

        return render(request, 'app/order.html', context)


class MakeOrderView(CartMixin, View):
    """
    Представление для добавления заказа пользователя в базу.
    """

    @transaction.atomic
    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = self.customer
            new_order.customer_name = form.cleaned_data['customer_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.adress = form.cleaned_data['adress']
            new_order.customer_last_name = form.cleaned_data['customer_last_name']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            self.customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Заказ создан')
            return redirect('/')
        return redirect('/order/')


class GetSearchText(CartMixin, View):
    """
    Обработка поискового запроса
    """

    def post(self, request):
        search_term = str(request.POST.get('search_text'))
        if search_term == '':
            messages.add_message(request, messages.INFO, 'Вы ввели пустой поисковой запрос!')
            return HttpResponseRedirect('/')
        else:
            search_slug = process_search_term(search_term)
            return redirect(f'/search-results/{search_slug}')


class SearchResultPage(CartMixin, View):
    """
    Страница с результатом поиска.
    """

    def get(self, request, **kwargs):
        search_term_words = process_search_slug(kwargs)
        products = get_all_products()
        searched_products = search_products(products, search_term_words)
        context = {
            'searched_products': searched_products,
            'cart': self.cart
        }
        return render(request, 'app/search.html', context)


class CustomerOrdersView(CartMixin, View):
    """
    Заказы пользователя.
    """

    def get(self, request):
        orders = get_customer_orders(self).order_by('-date_of_order')
        context = {
            'orders': orders
        }
        return render(request, 'app/customer_orders.html', context)


<<<<<<< HEAD
=======
class MakeOrderView(CartMixin, View):
    """
    Представление для добавления заказа пользователя в базу.
    """

    @transaction.atomic
    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            make_order_form_clean(form, self)
            messages.add_message(request, messages.INFO, 'Заказ создан')
            return redirect('/')
        return redirect('/order/')


>>>>>>> 1daa6aece23b5684f5be666f6e9f8fa7053afb78
class SendEMailView(CartMixin, View):
    """
    Отправка писем с фидбеком или жалобами
    """

    def get(self, request):
        form = SendQuestionMail(request.POST)
        context = {
            'cart': self.cart,
            'form': form
        }
        return render(request, 'app/mail.html', context)

    def post(self, request):
        form = SendQuestionMail(request.POST)
        if form.is_valid():
            email_contents = clean_email_form(form)
            send_notification_email(email_contents['user_email'],
                                    email_contents['user_name'],
                                    email_contents['user_last_name'])
            send_email_to_host(email_contents['user_email'],
                               email_contents['email_text'])
            return redirect('/')
