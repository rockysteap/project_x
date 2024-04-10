from typing import Any
from django.db import models


class Validator:
    @staticmethod
    def is_value_present_in_db(value: Any, model: models, field: str) -> bool:
        return model.objects.filter(**dict({field: value})).first() is not None

    @staticmethod
    def is_two_values_present_in_same_entry(values: list[Any], model: models, fields: list[str]) -> bool:
        value1, value2 = values[0], values[1]
        field1, field2 = fields[0], fields[1]
        entry = model.objects.filter(**dict({field1: value1})).first()
        if entry:
            return (model.objects.filter(**dict({field1: value1})).all()
                    .filter(**dict({field2: value2})).first()
                    is not None)
        return False
