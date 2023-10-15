"""
This module includs some utility functions used for various purposes in other apps, modules, classes or functions.
"""

from rest_framework.serializers import ModelSerializer
from typing import Any


def remove_blank_or_null(data: dict) -> dict:
    """
    This functions removes the blank ("") or null (None) type values from the given dictionary of data.

    ARGS: data: dict
    RETURNS: cleaned_data: dict
    """

    cleaned_data = {
        key: value for key, value in data.items() if value != "" and value is not None
    }
    return cleaned_data


def get_nested_object_deserialized(
    data: dict, serializer_class: ModelSerializer
) -> Any:
    serializer: ModelSerializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    deserialized_instance = serializer.save()
    return deserialized_instance
