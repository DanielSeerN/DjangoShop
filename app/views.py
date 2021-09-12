from django.shortcuts import render
from django.views.generic import DetailView

from .models import SmartPhone
from .models import WashingMachine
from .models import LawnMover
from .models import Conditioner
from .models import VideoGameConsole
from .models import TV
from .models import PhotoCamera

class ProductDetail(DetailView):
    CT_MODELS = {
        'smartphone': SmartPhone,
        'washing_machine': WashingMachine,
        'lawnmover': LawnMover,
        'conditioner': Conditioner,
        'videogameconsole': VideoGameConsole,
        'tv': TV,
        'photocamera': PhotoCamera

    }
    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODELS[kwargs['ct_model']]
        self.queryset = self.model.objects.all()
        return super().dispatch(request, *args, **kwargs)
    context_object_name = 'product'
    template_name = 'app/product.html'
    slug_url_kwarg = 'slug'

def view(request):
    return render(request, 'app/index.html')


