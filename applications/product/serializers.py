from rest_framework import serializers

from .models import Category, Product, Brand, ProductImage, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    # category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ["id"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["id"]


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ["price", "sku", "stock_quantity", "product_image", "order"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    brand_name = serializers.CharField(source="brand.name")
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "category_name",
            "brand_name",
            "product_line",
        ]
