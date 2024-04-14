from rest_framework import serializers
from .models import *


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'pk',
            'FIO_customer',
            'delivery_address',
            'delivery_type',
            'date_create',
            'date_finish',
            'books'
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'pk',
            'name',
            'description',
            'price',
            'create_date',
            'update_date',
            'photo',
            'exists',
            'category',
            'tag',
            'parametr'
        ]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'name',
            'agent_firstname',
            'agent_name',
            'agent_patronymic',
            'agent_telephone'
        ]

class ProductSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'price'
        ]

class Pos_supplySerializer(serializers.ModelSerializer):
    product = ProductSupplySerializer(read_only=True)

    class Meta:
        model = Pos_supply
        fields=[
            'product',
            'count',
            'price_pos_supply'
        ]

class SupplySerializer(serializers.ModelSerializer):
    supplier = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='supplier-detail'
    )

    pos_supply_set = Pos_supplySerializer(many=True, read_only=True)

    class Meta:
        model = Supply
        fields = [
            'pk',
            'date_supply',
            'supplier',
            'price_supply',
            'pos_supply_set'
        ]