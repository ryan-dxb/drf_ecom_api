from rest_framework import serializers

from .models import (
    Category,
    Product,
    Brand,
    ProductImage,
    ProductLine,
    Attribute,
    AttributeValue,
)


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


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        exclude = ["name", "id"]


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        exclude = ["id"]


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_values = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = [
            "price",
            "sku",
            "stock_quantity",
            "product_image",
            "order",
            "attribute_values",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        att_data = data.pop("attribute_values")

        print(att_data)
        attr_values = {}

        for key in att_data:
            print("Key: " + str(key["attribute"]))
            attr_values.update({key["attribute"]: key["attribute_value"]})

        print(attr_values)

        data.update({"specification": attr_values})

        return data


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
