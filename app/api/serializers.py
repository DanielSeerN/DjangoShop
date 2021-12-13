from ..models import Category, Product, Customer, Order
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер для категории продукта
    """
    title = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериалайзер продукта
    """
    title = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    slug = serializers.SlugField()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    image = serializers.ImageField()
    description = serializers.CharField()

    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериалайзер заказа
    """
    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    """
    Сериалайзер покупателя
    """
    orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'
