from django.contrib import admin
from django.forms import ModelForm, ValidationError

from .models import *


class ProductAdminForm(ModelForm):
    MAX_RESOLUTION = (800, 800)
    MAX_IMAGE_SIZE = 3145728

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            'image'].help_text = 'Загружайте изображения с разрешением не более{}x{}, иначе оно будет обрезано'.format(
            *self.MAX_RESOLUTION
        )


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(CartProduct)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Resistor, ProductAdmin)
admin.site.register(Transistor, ProductAdmin)
admin.site.register(Order)
