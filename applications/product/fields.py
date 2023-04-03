from django.db import models
from django.core import checks
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    description = "Custom Ordering Field"

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        # Check if unique_for_field is provided
        return [
            *super().check(**kwargs),
            *self._check_for_field_attribute(**kwargs),
        ]

    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [
                checks.Error(
                    "OrderField requires a 'unique_for_field' attribute",
                    obj=self,
                    id="fields.E001",
                )
            ]
        elif self.unique_for_field == "self":
            return [
                checks.Error(
                    "OrderField cannot have 'unique_for_field' attribute set to 'self'",
                    obj=self,
                    id="fields.E002",
                )
            ]
        elif self.unique_for_field not in [
            f.name for f in self.model._meta.fields
        ]:
            return [
                checks.Error(
                    "OrderField 'unique_for_field' attribute must be a field name",
                    obj=self,
                    id="fields.E003",
                )
            ]
        return []

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # No current value
            try:
                qs = self.model.objects.all()
                if self.unique_for_field:
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.unique_for_field
                    }
                    qs = qs.filter(**query)
                # Get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 1
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
