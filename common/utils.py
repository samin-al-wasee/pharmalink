"""
This module includs some utility functions used for various purposes in other apps, modules, classes or functions.
"""

from collections import OrderedDict
from typing import Any

from django.http import Http404, QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.serializers import ModelSerializer


def remove_blank_or_null(data: QueryDict | dict) -> QueryDict:
    """
    Remove the blank ("", []) or null (None) type values from given data.
    """

    nested_data = []
    clean_data = {}

    for key, value in data.items():
        if isinstance(value, dict):
            nested_data.append((key, value))
            continue

        if "." in key or value:
            clean_data[key] = value

    for name, dictionary in nested_data:
        flat_data = {f"{name}.{key}": value for key, value in dictionary.items()}
        clean_data.update(flat_data)

    clean_data_ = QueryDict("", mutable=True)  # Research QueryDict
    clean_data_.update(clean_data)
    return clean_data_


def extract_fields(data: dict, fields: tuple | list):
    """
    Extract/remove specified fields from given data.
    Return extracted fields if needed.
    Return only remaining data after extraction by default.
    """
    excluded = {field: data.pop(field, None) for field in fields}
    return (data, excluded)


def convert_to_dictionary(ordered_dict: OrderedDict) -> dict:
    dictionary = {key: value for key, value in ordered_dict.items()}
    return dictionary


def create_nested_objects(
    data: dict, fields: tuple | list, serializer_classes: tuple | list
) -> dict:
    for field, serializer_class in zip(fields, serializer_classes):
        replacable = data.pop(field, None)
        if not replacable:
            data[field] = None
        elif isinstance(replacable, list):
            data[field] = _get_object(
                data=replacable, serializer_class=serializer_class, many=True
            )
        else:
            data[field] = _get_object(
                data=replacable, serializer_class=serializer_class
            )

    return data


def replace_uuids_with_objects(
    data: dict,
    uuid_fields: list | tuple,
    object_fields: list | tuple,
    model_classes: list | tuple,
) -> dict:
    """
    Retrieve objects using given uuids.
    Insert objects to corresponding object fields.
    Assume given data and uuids are valid.
    """
    for uuid_field, object_field, model_class in zip(
        uuid_fields, object_fields, model_classes
    ):
        uuid = data.pop(uuid_field)
        object_ = model_class.objects.get(uuid=uuid)
        data[object_field] = object_

    return data


def replace_ids_with_uuid_slug(
    instance: Any,
    uuid_fields: list | tuple = None,
    slug_fields: list | tuple = None,
):
    if uuid_fields:
        new_representation = {
            uuid_field: getattr(instance, uuid_field).uuid for uuid_field in uuid_fields
        }
    if slug_fields:
        new_representation.update(
            {
                slug_field: getattr(instance, slug_field).slug
                for slug_field in slug_fields
            }
        )
    return new_representation


def get_path_objects(
    request_kwargs: dict, path_variables: list | tuple, model_classes: list | tuple
) -> dict:
    kwarg_objects = {}
    for path_variable, model_class in zip(path_variables, model_classes):
        path_var_value = request_kwargs.get(path_variable)
        try:
            try:
                object_ = get_object_or_404(klass=model_class, uuid=path_var_value)
            except ValueError or TypeError:
                object_ = get_object_or_404(klass=model_class, slug=path_var_value)
        except Http404:
            raise NotFound(f"{model_class} does not exist.")
        kwarg_objects[path_variable] = object_

    return kwarg_objects


def _get_object(
    data: dict | list, serializer_class: ModelSerializer, many: bool = False
) -> list | Any:
    print(data)
    serializer: ModelSerializer = serializer_class(data=data, many=many)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    return instance
