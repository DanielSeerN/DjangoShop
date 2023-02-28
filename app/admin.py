from django.contrib import admin
<<<<<<< HEAD
from .models import *
=======
from .models import Cart, Customer, Order, Category, CartProduct, Product
>>>>>>> 1daa6aece23b5684f5be666f6e9f8fa7053afb78

models_ = [Category, CartProduct,
           Cart, Customer, Order, Product, Review]
for model in models_:
    admin.site.register(model)
