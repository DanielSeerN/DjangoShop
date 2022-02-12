from ..models import Order


def get_customer_orders(self):
    """
    Получение заказов покупателя
    :param self:
    :return:
    """
    orders = Order.objects.filter(customer=self.customer)
    return orders
