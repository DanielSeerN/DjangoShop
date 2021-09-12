from django.contrib import admin
from django.urls import path

from .views import view, ProductDetail

urlpatterns = [
    path('', view, name='main'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetail.as_view(), name='product')

]
