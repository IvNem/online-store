from django.shortcuts import render
from django.views.generic import DetailView

from mainapp.models import Product


def test_view(request):
    return render(request, 'base_generic.html', {})


class ProductDetailView(DetailView):
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'
