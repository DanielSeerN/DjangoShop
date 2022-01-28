from django.shortcuts import render, redirect
from django.views.generic import View
from .models import CategorySpecification, ProductSpecification
from .utils import get_product


class FindSpecificationPage(View):
    """
    Страница для поиска спецификаций
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'product_spec/find_specification.html')


class FindSpecification(View):
    """

    """
    def post(self, request, *args, **kwargs):
        slug = str(request.POST.get('product_slug'))
        return redirect(f'/specification/product-specification/{slug}')


class CreateSpecificationPage(View):
    def get(self, request, *args, **kwargs):
        product = get_product(slug=kwargs.get('slug'))
        categories_of_specification = CategorySpecification.objects.filter(category=product.category).all()
        product_specifications = ProductSpecification.objects.filter(product=product).all()
        specifications_existence = False
        if product_specifications:
            specifications_existence = True
        context = {
            'specifications_for_product': categories_of_specification,
            'product': product,
            'specifications_existence': specifications_existence
        }
        return render(request, 'product_spec/create_specification.html', context)


class CreateSpecification(View):
    def post(self, request, *args, **kwargs):
        product = get_product(slug=kwargs.get('slug'))
        category_of_product = product.category
        categories_of_specification = CategorySpecification.objects.filter(category=category_of_product).all()
        for category_of_specification in categories_of_specification:
            value = str(request.POST.get(f'{category_of_specification.specification}'))
            product_specification = ProductSpecification.objects.create(value=value,
                                                                        category=category_of_product,
                                                                        product=product,
                                                                        specification=category_of_specification)
            product_specification.save()
        return redirect('/specification/')


class UpdateSpecification(View):
    def post(self, request, *args, **kwargs):
        product = get_product(slug=kwargs.get('slug'))
        category_of_product = product.category
        categories_of_specification = CategorySpecification.objects.filter(category=category_of_product).all()
        for category_of_specification in categories_of_specification:
            value = str(request.POST.get(f'{category_of_specification.specification}'))
            product_specification = ProductSpecification.objects.get(category=category_of_product,
                                                                     product=product,
                                                                     specification=category_of_specification)
            product_specification.value = value
            product_specification.save()
        return redirect('/specification/')
