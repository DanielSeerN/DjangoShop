from django.db import models
from app.models import Product, Category


class CategorySpecification(models.Model):
    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE)
    specification = models.CharField(max_length=255)
    unit = models.CharField(max_length=255, blank=True)


class ProductSpecification(models.Model):
    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', on_delete=models.CASCADE)
    specification = models.ForeignKey(CategorySpecification, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
