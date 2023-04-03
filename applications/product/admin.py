from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Category, Product, Brand, ProductLine, ProductImage


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


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductLineImageInline]


admin.site.register(Category)


admin.site.register(Brand)
