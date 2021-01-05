from django.shortcuts import render
from django.views.generic import DetailView

from mainapp.models import Resistor, Transistor, Category


def test_view(request):
    categories = Category.objects.get_categories_for_left_sidebar()

    return render(request, 'base_generic.html', {'categories': categories})


class ProductDetailView(DetailView):
    # Список моделей
    CT_MODEL_CLASS = {
        'resistor': Resistor,
        'transistor': Transistor
    }

    # Определяем какую модель будем использовать
    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'
