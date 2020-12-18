# Используем для того чтобы узнать длину и высоту загружаемого изображения
from PIL import Image

from django.contrib import admin
from django.forms import ModelForm, ValidationError

from .models import *


class ProductAdminForm(ModelForm):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)
    MAX_IMAGE_SIZE = 3145728

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Загружайте изображения с минимальным разрешением {}x{}'.format(
            *self.MIN_RESOLUTION
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if img.size > self.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен превышать 3 MB')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Слишком маленькое разрешение изображения')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Слишком большое разрешение изображения')
        return image


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(CartProduct)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
