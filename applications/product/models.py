from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError


# class ActiveManager(models.Manager):
#     # def get_queryset(self):
#     #     return super().get_queryset().filter(is_active=True)

#     def is_active(self):
#         return self.get_queryset().filter(is_active=True)


class ActiveQuerySet(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.slug

    # Change plural name
    class Meta:
        verbose_name_plural = "Categories"


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.CASCADE, related_name="product_line_product_type"
    )
    is_active = models.BooleanField(default=False)
    objects = ActiveQuerySet.as_manager()
    # isActive = ActiveManager()

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    # Change plural name
    class Meta:
        verbose_name_plural = "Attributes"


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value"
    )

    # def __str__(self):
    #     return self.attribute.attribute_value

    # Change plural name
    class Meta:
        verbose_name_plural = "Attribute Values"


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100)
    stock_quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_line")
    order = OrderField(unique_for_field="product")
    attribute_values = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValues",
        related_name="product_line_attribute_values",
    )

    is_active = models.BooleanField(default=False)

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)

        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Order must be unique for each product.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    # def __str__(self):
    #     return self.sku

    # Change plural name
    class Meta:
        verbose_name_plural = "Product Lines"


class ProductLineAttributeValues(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue, on_delete=models.CASCADE, related_name="product_line_attribute_value"
    )
    product_line = models.ForeignKey(
        ProductLine,
        on_delete=models.CASCADE,
        related_name="product_line_attribute_product_line",
    )

    # def __str__(self):
    #     return self.attribute_value

    # Change plural name
    # Unique together
    class Meta:
        verbose_name_plural = "Product Line Attribute Values"
        unique_together = ("attribute_value", "product_line")

    def clean(self):
        qs = (
            ProductLineAttributeValues.objects.filter(attribute_value=self.attribute_value)
            .filter(product_line=self.product_line)
            .exists()
        )

        if not qs:
            iqs = Attribute.objects.filter(
                attribute_value__product_line_attribute_values=self.product_line
            ).values_list("pk", flat=True)

            if self.attribute_value.attribute.id in list(iqs):
                raise ValidationError("Attribute already exists for this product line.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLineAttributeValues, self).save(*args, **kwargs)


class ProductImage(models.Model):
    alt_text = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to=None, default="test.jpg")
    productline = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="productline")

    def clean(self):
        qs = ProductImage.objects.filter(productline=self.productline)

        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Order must be unique for each product.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.alt_text

    # Change plural name
    class Meta:
        verbose_name_plural = "Product Images"


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    attributes = models.ManyToManyField(
        Attribute, through="ProductTypeAttribute", related_name="product_type_attributes"
    )

    # def __str__(self):
    #     return self.name

    # Change plural name
    class Meta:
        verbose_name_plural = "Product Types"


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_product_type",
    )
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="product_type_attribute"
    )

    # Unique together
    # Change plural name
    class Meta:
        verbose_name_plural = "Product Type Attributes"
        unique_together = ("product_type", "attribute")
