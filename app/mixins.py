from django.views.generic import View
from .models import SmartPhone, Cart, Customer, WashingMachine, LawnMover, Conditioner, TV, VideoGameConsole, \
    CartProduct


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user)
            if not customer:
                customer = Customer.objects.create(user=request.user)
            # cart = Cart.objects.filter(owner=customer, in_order=False).last()
            cart = 0
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonym_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonym_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)