from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView, View

from .forms import OrderForm
from .utils import refresh_cart
from .models import SmartPhone, Cart, CartProduct, WashingMachine, LawnMover, Conditioner, VideoGameConsole, TV, \
    PhotoCamera, LatestProducts, Customer
from .mixins import CartMixin


class MainView(View):
    def get(self, request, *args, **kwargs):
        products = LatestProducts.objects.get_mainpage_products('smartphone', 'washing_machine', 'lawnmover',
                                                                'photocamera', 'videogameconsole', 'tv',
                                                                priority_models='conditioner')

        context = {
            'products': products,
        }
        return render(request, 'app/index.html', context)


class ProductDetail(CartMixin, DetailView):
    CT_MODELS = {
        'smartphone': SmartPhone,
        'washing_machine': WashingMachine,
        'lawnmover': LawnMover,
        'conditioner': Conditioner,
        'videogameconsole': VideoGameConsole,
        'tv': TV,
        'photocamera': PhotoCamera

    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODELS[kwargs['ct_model']]
        self.queryset = self.model.objects.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'app/product.html'
    slug_url_kwarg = 'slug'


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(user=self.cart.owner, cart=self.cart,
                                                                  content_type=content_type, object_id=product.id,
                                                                  )
        if created:
            self.cart.products.add(cart_product)

        messages.add_message(request, messages.INFO, 'Товар добавлен в корзину')
        return HttpResponseRedirect('/cart/')


class RemoveFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart,
                                               content_type=content_type, object_id=product.id
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

class ChangeProductQuantityView(CartMixin ,View):
    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart,
                                               content_type=content_type, object_id=product.id
                                               )
        quantity = int(request.POST.get('qty'))
        cart_product.quantity = quantity
        cart_product.final_price = cart_product.content_object.price * cart_product.quantity
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