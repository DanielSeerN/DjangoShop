from django.urls import path
from .views import (SpecificationPage,
                    UpdateSpecification,
                    CreateSpecification,
                    FindSpecificationPage,
                    FindSpecification)

urlpatterns = [
    path('', FindSpecificationPage.as_view(), name='specification_search_page'),
    path('product-specification/<str:slug>', SpecificationPage.as_view(), name='create_specification'),
    path('add-specification/<str:slug>', CreateSpecification.as_view(), name='add_specification'),
    path('find-specification/', FindSpecification.as_view(), name='find_specification'),
    path('update-specification/<str:slug>', UpdateSpecification.as_view(), name='update_specification')
]
