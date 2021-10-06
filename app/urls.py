from django.contrib import admin
from django.urls import path

from .views import CartView, MainView, ProductDetail, AddToCartView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetail.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart')

]
