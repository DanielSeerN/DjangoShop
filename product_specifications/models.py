from django.db import models


class CategorySpecification(models.Model):
    category = models.ForeignKey('app.Category', verbose_name='category', on_delete=models.CASCADE)
    specification = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)


class ProductSpecification(models.Model):
    category = models.ForeignKey('app.Category', verbose_name='category', on_delete=models.CASCADE)
    product = models.ForeignKey('app.Product', verbose_name='product', on_delete=models.CASCADE)
    specification = models.ForeignKey(CategorySpecification, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)