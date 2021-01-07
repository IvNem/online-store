"""Mixin представляет собой набор свойств и методов ,
    которые могут быть использованы в различных классах,
    которые не приходят из базового класса. """
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from .models import Category, Customer, Cart, Transistor, Resistor


class CategoryDetailMixin(SingleObjectMixin):
    CATEGORY_PRODUCT_MODEL = {
        'transistors': Transistor,
        'resistors': Resistor
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_left_sidebar()
            context['category_products'] = model.objects.all()
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_left_sidebar()
        return context

class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonimus_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonimus_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
