from rest_framework import serializers

from .models import Category, Product, Brand, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ["id"]


class ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLine
        exclude = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"
