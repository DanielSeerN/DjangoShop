from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from .models import CategorySpecification, ProductSpecification
from .utils import get_product


class FindSpecificationPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'product_specifications/find_specification.html')


class FindSpecification(View):
    def get(self, request, *args, **kwargs):
        slug = str(request.POST.get('unique_id'))
        product = get_product(slug)
        product_specification, created = ProductSpecification.objects.get_or_create(product=product)
        if not created:
            return HttpResponseRedirect(f'/specification/{slug}/')


class CreateSpecificationPage(View):
    def get(self, request, *args, **kwargs):
        product = get_product(slug=kwargs.get('slug'))
        category_of_product = product.category
        categories_of_specification = CategorySpecification.objects.filter(category=category_of_product).all()
        context = {
            'specifications_for_product': categories_of_specification
        }
        return render(request, '_', context)


class CreateSpecification(View):
    def get(self, request, *args, **kwargs):
        product = get_product(slug=kwargs.get('slug'))
        category_of_product = product.category
        categories_of_specification = CategorySpecification.objects.filter(category=category_of_product).all()
        for category_of_specification in categories_of_specification:
            value = str(request.POST.get(f'{category_of_specification.specification}'))
            product_specification = ProductSpecification.objects.create(value=value, categgory=category_of_product,
                                                                        product=product)
        return HttpResponseRedirect('/find_specification/')


class UpdateSpecification(View):
    def get(self, request, *args, **kwargs):
        pass
