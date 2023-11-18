from rest_framework import serializers
from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields  = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']



class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
                (StockProduct.objects.create(product=position['product'], stock=stock, quantity=position['quantity'], price=position['price']))
        return stock

    def update(self, instance, validated_data):
            positions = validated_data.pop('positions')
            stock = super().update(instance, validated_data)
            for position in positions:
                StockProduct.objects.update_or_create(defaults={'quantity': position['quantity'], 'price': position['price']}, product=position['product'], stock=stock)
            return stock
    
    class Meta:
            model = Stock
            fields = ['id', 'positions', 'address']
