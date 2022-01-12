from django.urls import path
from .views import (CreateSpecificationPage,
                    UpdateSpecification,
                    CreateSpecification,
                    FindSpecificationPage,
                    FindSpecification)

urlpatterns_specifications = [
    path('specification/', FindSpecificationPage.as_view(), name='specification_search_page'),
    path('specification/<str:slug>', CreateSpecificationPage.as_view(), name='create_specification'),
    path('specification/add-specification/<str:slug>', CreateSpecification.as_view(), name='add_specification'),
    path('specification/find-specification/', FindSpecification.as_view(), name='find_specification')
]
