from django.shortcuts import render
from django.views.generic import DetailView, View

from mainapp.models import Resistor, Transistor, Category
from .mixins import CategoryDetailMixin


class BaseView(View):
    def get(self, request, *args,**kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        return render(request, 'base_generic.html', {'categories': categories})


class ProductDetailView(CategoryDetailMixin, DetailView):
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


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'
