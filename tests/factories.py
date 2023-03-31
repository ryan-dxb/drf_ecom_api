import factory
import pytest

from applications.product.models import Category

pytestmark = pytest.mark.django_db


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "Test Category"
