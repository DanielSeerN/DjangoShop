from django.contrib import admin
from .models import *
from django import forms

models_ = [Category, CartProduct,
           Cart, Customer, Order, Product]
for model in models_:
        admin.site.register(model)