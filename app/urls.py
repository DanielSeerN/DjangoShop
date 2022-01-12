from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (CartView,
                    MainPageView,
                    ProductView,
                    AddToCartView,
                    RemoveFromCartView,
                    OrderView,
                    ChangeProductQuantityView,
                    MakeOrderView,
                    LoginView,
                    RegistrationView,
                    CustomerOrdersView,
                    CategoryView)

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('products/<str:slug>/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('order/', OrderView.as_view(), name='order'),
    path('change-product-quantity/<str:slug>/', ChangeProductQuantityView.as_view(), name='change_product_quantity'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('orders/', CustomerOrdersView.as_view(), name='orders'),
    path('category/<str:slug>/', CategoryView.as_view(), name='category'),


]
