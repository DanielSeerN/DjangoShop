from django.shortcuts import render, redirect
from django.views.generic import View
from .utils import get_product, get_product_specifications, get_specification_categories, create_product_specification, \
    get_product_specification


class FindSpecificationPage(View):
    """
    Страница для поиска спецификаций
    """
    def get(self, request):
        return render(request, 'product_spec/find_specification.html')


class FindSpecification(View):
    """
    Поиск специфицификации
    """
    def post(self, request):
        slug = str(request.POST.get('product_slug'))
        return redirect(f'/specification/product-specification/{slug}')


class SpecificationPage(View):
    """
    Страничка для создания спецификации
    """
    def get(self, request,  **kwargs):
        product = get_product(slug=kwargs.get('slug'))
        categories_of_specification = get_specification_categories(product.category)
        product_specifications = get_product_specifications(product)
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
    """
    Создание спецификации
    """
    def post(self, request, **kwargs):
        product = get_product(slug=kwargs.get('slug'))
        categories_of_specification = get_specification_categories(product.category)
        for category_of_specification in categories_of_specification:
            value = str(request.POST.get(f'{category_of_specification.specification}'))
            product_specification = create_product_specification(value, product, category_of_specification)
            product_specification.save()
        return redirect('/specification/')


class UpdateSpecification(View):
    """
    Изменить спецификацию
    """
    def post(self, request, **kwargs):
        product = get_product(slug=kwargs.get('slug'))
        categories_of_specification = get_specification_categories(product.category)
        for category_of_specification in categories_of_specification:
            value = str(request.POST.get(f'{category_of_specification.specification}'))
            product_specification = get_product_specification(product, category_of_specification)
            product_specification.value = value
            product_specification.save()
        return redirect('/specification/')
