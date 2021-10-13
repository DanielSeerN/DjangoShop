from django.contrib import admin
from django.urls import path

from .views import CartView, MainView, ProductDetail, AddToCartView, RemoveFromCartView, OrderView, \
    ChangeProductQuantityView, MakeOrderView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetail.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('order/', OrderView.as_view(), name='order'),
    path('change-product-quantity/<str:ct_model>/<str:slug>/', ChangeProductQuantityView.as_view(), name='change_product_quantity'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
]
