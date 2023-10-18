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

    nested_dictionaries = []
    cleaned_data = {}

    for key, value in data.items():
        if type(value) is dict:
            nested_dictionaries.append((key, value))
            continue

        if "." in key or (value != "" and value is not None):
            cleaned_data[key] = value

    for name, dictionary in nested_dictionaries:
        flattened_dictionary = {
            f"{name}.{key}": value for key, value in dictionary.items()
        }
        cleaned_data.update(flattened_dictionary)

    cleaned_data_ = QueryDict("", mutable=True)  # Research QueryDict
    cleaned_data_.update(cleaned_data)
    return cleaned_data_


def exclude_fields_from_data(data: dict, fields: tuple | list):
    excluded_data = {field: data.pop(field, None) for field in fields}
    return data


def replace_nested_dict_with_objects(
    data: dict, fields: tuple | list, serializer_classes: tuple | list
) -> dict:
    for field, serializer_class in zip(fields, serializer_classes):
        data_to_replace = data.pop(field, None)
        if data_to_replace is None:
            data[field] = None
        elif type(data_to_replace) is list:
            data[field] = _get_nested_object_deserialized(
                data=data_to_replace, serializer_class=serializer_class, many=True
            )
        else:
            data[field] = _get_nested_object_deserialized(
                data=data_to_replace, serializer_class=serializer_class
            )

    return data


def _get_nested_object_deserialized(
    data: dict | list, serializer_class: ModelSerializer, many: bool = False
) -> list | Any:
    serializer: ModelSerializer = serializer_class(data=data, many=many)
    serializer.is_valid(raise_exception=True)
    deserialized_instance = serializer.save()
    return deserialized_instance
