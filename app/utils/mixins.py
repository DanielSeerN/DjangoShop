from django.views.generic import View
from ..models import Cart, Customer


class CartMixin(View):
    """
    Миксины для корзины
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(user=request.user)
            self.customer = customer
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonym_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonym_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)