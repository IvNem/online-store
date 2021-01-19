from rest_framework import serializers

from ..models import Category, Resistor, Customer, Order


# Валидация данных
class CategorySerializers(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug'
        ]


class BaseProductSerializer:
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    title = serializers.CharField(required=True)
    manufacture = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    image = serializers.ImageField(required=True)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=9, decimal_places=2, required=True)


class ResistorSerializer(BaseProductSerializer, serializers.ModelSerializer):
    res_type = serializers.CharField(required=True)
    resistance = serializers.FloatField(required=True)
    unit = serializers.CharField(required=True)
    presicion = serializers.FloatField(required=True)
    capacity = serializers.CharField(required=True)

    class Meta:
        model = Resistor
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    # Детальная информация заказов пользователя
    orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'

