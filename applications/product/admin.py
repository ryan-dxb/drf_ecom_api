from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Category,
    Product,
    Brand,
    ProductLine,
    ProductImage,
    ProductType,
    AttributeValue,
    Attribute,
)


class EditLinkInline(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=(instance.pk,),
        )

        if instance.pk:
            link = mark_safe(f'<a href="{url}">Edit</a>')
        else:
            link = ""

        return link


class ProductLineImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductLineInline(EditLinkInline, admin.TabularInline):
    model = ProductLine
    readonly_fields = ["edit"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue.product_line_attribute_values.through


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductLineImageInline, AttributeValueInline]


class AttributeInline(admin.TabularInline):
    model = Attribute.product_type_attributes.through


@admin.register(ProductType)
class ProductTypeInline(admin.ModelAdmin):
    inlines = [AttributeInline]


admin.site.register(Category)


admin.site.register(Brand)

admin.site.register(Attribute)
admin.site.register(AttributeValue)
