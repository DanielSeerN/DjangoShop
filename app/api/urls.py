from django.urls import path
from .views_api import CategoryAPIView, ProductAPIView, CustomerAPIView

urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='categories_api'),
    path('products/', ProductAPIView.as_view(), name='products_api'),
    path('customers/', CustomerAPIView.as_view())
]
