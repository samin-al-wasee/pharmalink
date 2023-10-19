"""
This module includs some utility functions used for various purposes in other apps, modules, classes or functions.
"""

from typing import Any

from django.http import QueryDict
from rest_framework.serializers import ModelSerializer


def remove_blank_or_null(data: QueryDict | dict) -> QueryDict | dict:
    """
    This functions removes the blank ("") or null (None) type values from the given QueryDict of data.

    ARGS: data: QuerydDict | dict
    RETURNS: cleaned_data: QueryDict
    """

    nested_data = []
    clean_data = {}

    for key, value in data.items():
        if type(value) is dict:
            nested_data.append((key, value))
            continue

        if "." in key or (value != "" and value is not None):
            clean_data[key] = value

    for name, dictionary in nested_data:
        flat_data = {f"{name}.{key}": value for key, value in dictionary.items()}
        clean_data.update(flat_data)

    clean_data_ = QueryDict("", mutable=True)  # Research QueryDict
    clean_data_.update(clean_data)
    return clean_data_


def exclude_fields(data: dict, fields: tuple | list):
    excluded = {field: data.pop(field, None) for field in fields}
    return data


def create_nested_objects(
    data: dict, fields: tuple | list, serializer_classes: tuple | list
) -> dict:
    for field, serializer_class in zip(fields, serializer_classes):
        replacable = data.pop(field, None)
        if replacable is None:
            data[field] = None
        elif type(replacable) is list:
            data[field] = _get_object(
                data=replacable, serializer_class=serializer_class, many=True
            )
        else:
            data[field] = _get_object(
                data=replacable, serializer_class=serializer_class
            )

    return data


def _get_object(
    data: dict | list, serializer_class: ModelSerializer, many: bool = False
) -> list | Any:
    serializer: ModelSerializer = serializer_class(data=data, many=many)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    return instance
