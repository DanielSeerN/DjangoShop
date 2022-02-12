from ..models import Order


def get_customer_orders(self):
    """
    Получение заказов покупателя
    """
    orders = Order.objects.filter(customer=self.customer)
    return orders
