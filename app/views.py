from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView, View

from .forms import OrderForm
from .utils import refresh_cart
from .models import Cart, CartProduct, Customer, Product, Category
from .mixins import CartMixin


class ProductView(CartMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'app/product.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart

        return context


class MainView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.all()
        context = {
            'products': products,
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'app/index.html', context)


class LoginView(CartMixin, View):
    pass


class AddToCartView(CartMixin, View):
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
        messages.add_message(request, messages.INFO, 'Товар добавлен в корзину')
        refresh_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class RemoveFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')

        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart,
                                               product=product
                                               )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        refresh_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Товар удалён из корзины')
        return redirect('/cart/')


class OrderView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form
        }

        return render(request, 'app/order.html', context)


class ChangeProductQuantityView(CartMixin, View):
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


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart
        }
        return render(request, 'app/cart.html', context)


class MakeOrderView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.customer_name = form.cleaned_data['customer_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.adress = form.cleaned_data['adress']
            new_order.customer_last_name = form.cleaned_data['customer_last_name']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Заказ создан')
            return redirect('/')
        return redirect('/order/')
