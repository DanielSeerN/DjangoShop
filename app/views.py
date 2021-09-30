from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, View

from .models import SmartPhone, Cart
from .models import WashingMachine
from .models import LawnMover
from .models import Conditioner
from .models import VideoGameConsole
from .models import TV
from .models import PhotoCamera
from .models import LatestProducts, Customer


class MainView(View):
    def get(self, request, *args, **kwargs):
        products = LatestProducts.objects.get_mainpage_products('photocamera', 'smartphone',
                                                                'conditioner')

        context = {
            'products': products,
        }
        return render(request, 'app/index.html', context)


class ProductDetail(DetailView):
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


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        return HttpResponseRedirect('/cart/')


class CartView(View):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)

        context = {
             'cart': cart
        }
        return render(request, 'app/cart.html', context)
