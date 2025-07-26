from django.db import transaction
from rest_framework import serializers

from api.models import Product, Order, OrderItem, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'stock',
            'price'
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price should be positive number')
        return value


class CreateOrderSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')

    items = OrderItemCreateSerializer(many=True)
    order_id = serializers.UUIDField(read_only=True)

    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if orderitem_data is not None:
                instance.items.all().delete()

                for item in orderitem_data:
                    OrderItem.objects.create(order=instance, **item)

        return instance


    def save(self, validated_data):
        orderitem_data = validated_data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in orderitem_data:
                OrderItem.objects.create(order=order, **item)

        return order

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items',
            )
        extra_kwargs = {
            'user': {'read_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.CharField(source='product.price')

    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_price', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = ('order_id', 'user', 'created_at', 'status', 'items', 'total_price')


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
    total_price = serializers.FloatField()
