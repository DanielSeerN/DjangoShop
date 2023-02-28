from django.contrib import admin
from .models import CategorySpecification, ProductSpecification


admin.site.register(CategorySpecification)
admin.site.register(ProductSpecification)