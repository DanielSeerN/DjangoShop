from django.contrib import admin
from .models import Cart, Customer, Order, Category, CartProduct, Product

models_ = [Category, CartProduct,
           Cart, Customer, Order, Product]
for model in models_:
    admin.site.register(model)
