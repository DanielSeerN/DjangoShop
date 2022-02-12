from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View

from .services import send_email_to_host, send_notification_email, process_search_term, process_search_slug, \
    search_products
from .forms import OrderForm, LoginForm, RegistrationForm, SendQuestionMail
from .utils.order_utils import get_customer_orders
from .utils.product_utils import get_category, get_products_by_category, get_all_categories, get_all_products, \
    get_product
from .utils.utils_cart import refresh_cart, get_cart_product, create_customer
from .utils.mixins import CartMixin

from product_specifications.utils import get_product_specifications


class ProductView(CartMixin):
    """
    Представление для отображения продукта.
    """

    def get(self, request, **kwargs):
        product = get_product(kwargs)
        specifications = get_product_specifications(product)
        context = {
            'product': product,
            'details': specifications
        }
        return render(request, 'app/product.html', context)

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
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.address = form.cleaned_data['address']
            user.phone = form.cleaned_data['phone']
            user.save()
            create_customer(user)
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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
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
        if self.cart.final_price is None:
            self.cart.final_price = 0
        context = {
            'cart': self.cart
        }
        return render(request, 'app/cart.html', context)


class AddToCartView(CartMixin, View):
    """
    Добавление продукта в корзину пользователя.
    """

    def get(self, request, **kwargs):
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

    def get(self, request, **kwargs):
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


class GetSearchText(CartMixin, View):
    """
    Обработка поискового запроса
    """

    def post(self, request):
        search_term = str(request.POST.get('search_text'))
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
            user_email = form.cleaned_data['user_mail']
            email_text = form.cleaned_data['question']
            user_name = form.cleaned_data['first_name']
            user_last_name = form.cleaned_data['last_name']
            send_notification_email(user_email, user_name, user_last_name)
            send_email_to_host(user_email, email_text)
            return redirect('/')
