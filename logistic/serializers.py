from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class StockProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = StockProduct
        fields = ("id", "product", "quantity", "price")


class StockSerializer(serializers.ModelSerializer):
    positions = StockProductSerializer(many=True)

    class Meta:
        model = Stock
        fields = "__all__"

    def create(self, validated_data):
        positions_data = validated_data.pop("positions")
        stock = Stock.objects.create(**validated_data)
        for position_data in positions_data:
            product_data = position_data.pop("product")
            product, created = Product.objects.get_or_create(**product_data)
            StockProduct.objects.create(stock=stock, product=product, **position_data)
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop("positions")
        stock = super().update(instance, validated_data)
        for position_data in positions_data:
            product_data = position_data.pop("product")
            product, created = Product.objects.get_or_create(**product_data)
            position, created = StockProduct.objects.get_or_create(
                stock=stock,
                product=product,
                defaults={
                    "quantity": position_data["quantity"],
                    "price": position_data["price"],
                },
            )
            if not created:
                position.quantity = position_data["quantity"]
                position.price = position_data["price"]
                position.save()
        return stock
