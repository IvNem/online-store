"""Mixin представляет собой набор свойств и методов ,
    которые могут быть использованы в различных классах,
    которые не приходят из базового класса. """
from django.views import View
from .models import Customer, Cart


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
