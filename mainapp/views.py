from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.generic import DetailView, View
from django.http.response import HttpResponseRedirect
from mainapp.models import Category, Customer, Cart, CartProduct, Product
from .mixins import CartMixin
from django.contrib import messages
from .forms import OrderForm, LoginForm
from .utils import recount_cart
from django.db import transaction


class BaseView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart
        }
        return render(request, 'base_generic.html', context)


class ProductDetailView(CartMixin, DetailView):

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    # Информация о конкретной модели
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        # Берем нужные значения модели
        product_slug = kwargs.get('slug')
        # Вызываем родительскую модель и получаем его slug
        product = Product.objects.get(slug=product_slug)
        # Создаем новый объект
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        # Проверка был ли создан продукт
        if created:
            self.cart.products.add(cart_product)
        recount_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Товар добавлен в корзину')
        return HttpResponseRedirect('/cart/')


class DeleteCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        # Берем нужные значения модели
        product_slug = kwargs.get('slug')
        # Вызываем родительскую модель и получаем его slug
        product = Product.objects.get(slug=product_slug)
        # Создаем новый объект
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recount_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Товар удален из корзины')
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        # Берем нужные значения модели
        product_slug = kwargs.get('slug')
        # Вызываем родительскую модель и получаем его slug
        product = Product.objects.get(slug=product_slug)
        # Создаем новый объект
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recount_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Количество изменено')
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            # пример который нужно предзаполнить
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            # меняем статус корзины
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            # Список покупок
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер свяжется с Вами в ближайшее время')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class LoginView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'login.html', {'form': form, 'cart': self.cart})
