from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, View

from .models import SmartPhone, Cart, CartProduct, WashingMachine, LawnMover, Conditioner, VideoGameConsole, TV, PhotoCamera, LatestProducts, Customer
from .mixins import CartMixin


class MainView(View):
    def get(self, request, *args, **kwargs):
        products = LatestProducts.objects.get_mainpage_products('smartphone', 'washing_machine', 'lawnmover', 'conditioner', 'videogameconsole', 'tv', 'photocamera')

        context = {
            'products': products,
        }
        return render(request, 'app/index.html', context)


class ProductDetail(CartMixin,DetailView):
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


class AddToCartView(CartMixin,View):
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get_or_create(user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id, final_price=0)
        self.cart.products.add(cart_product)
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):

        context = {
             'cart': self.cart
        }
        return render(request, 'app/cart.html', context)
