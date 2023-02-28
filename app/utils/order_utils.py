from ..models import Order


def get_customer_orders(self):
    """
    Получение заказов покупателя
    """
    orders = Order.objects.filter(customer=self.customer)
    return orders


def make_order_form_clean(form, self):
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
