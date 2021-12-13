from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView, View

from .forms import OrderForm, LoginForm, RegistrationForm
from .utils import refresh_cart
from .models import CartProduct, Customer, Product, Category, Order
from .mixins import CartMixin

import logging

logger = logging.getLogger(__name__)  # Подключение логгера


class ExceptionCheck(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as ex:
            pass
        return response


class ProductView(CartMixin, DetailView):
    """
    Представление для отображения продукта и его характеристик.
    """
    model = Product
    context_object_name = 'product'
    template_name = 'app/product.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class MainPageView(CartMixin, View):
    """
    Главная страница.
    """

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.all()
        slider = products[:3]
        logger.warning('WARNING')
        context = {
            'products': products,
            'cart': self.cart,
            'categories': categories,
            'slider': slider
        }
        return render(request, 'app/index.html', context)


class RegistrationView(CartMixin, View):
    """
    Регистрация пользователя.
    """

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form
        }
        return render(request, 'app/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.address = form.cleaned_data['address']
            user.phone = form.cleaned_data['phone']
            user.save()
            create_customer = Customer.objects.create(user=user, phone=user.phone, adress=user.address)
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

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form
        }

        return render(request, 'app/login.html', context)

    def post(self, request, *args, **kwargs):
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


class CartView(CartMixin, View):
    """
    Корзина пользователя.
    """

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart
        }
        return render(request, 'app/cart.html', context)


class AddToCartView(CartMixin, View):
    """
    Добавление продукта в корзину пользователя.
    """

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(user=self.cart.owner, cart=self.cart,
                                                                  product=product
                                                                  )
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

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart,
                                               product=product
                                               )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        refresh_cart(self.cart)
        return redirect('/cart/')


class ChangeProductQuantityView(CartMixin, View):
    """

    Изменение кол-ва продукта.

    """

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart,
                                               product=product
                                               )
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

    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form
        }

        return render(request, 'app/order.html', context)


class CustomerOrdersView(CartMixin, View):
    """
    Заказы пользователя.
    """

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(customer=self.customer).order_by('-date_of_order')
        context = {
            'orders': orders
        }
        return render(request, 'app/customer_orders.html', context)


class MakeOrderView(CartMixin, View):
    """
    Представление для добавления заказа пользователя в базу.
    """

    @transaction.atomic
    def post(self, request, *args, **kwargs):
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
