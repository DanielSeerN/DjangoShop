from django.contrib import admin
from .models import *

models_ = [Category, CartProduct,
           Cart, Customer, Order, Product, Review]
for model in models_:
        admin.site.register(model)