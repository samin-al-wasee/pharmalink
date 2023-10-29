from rest_framework.serializers import ModelSerializer

from .models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "unit_no",
            "street_no",
            "line_1",
            "line_2",
            "city",
            "region",
            "postal_code",
            "country",
        )
        extra_kwargs = {
            "unit_no": {"required": False},
            "street_no": {"required": False},
            "line_1": {"required": False},
            "line_2": {"required": False},
            "region": {"required": False},
        }

    def create(self, validated_data):
        try:
            address = Address.objects.get(**validated_data)
            return self.update(instance=address, validated_data=validated_data)
        except Address.DoesNotExist:
            return super().create(validated_data)

    def save(self, **kwargs):
        try:
            search_parameters = {
                field: self.validated_data.get(field, "") for field in self.Meta.fields
            }
            address = Address.objects.get(**search_parameters)
            self.instance = address
        except Address.DoesNotExist:
            pass
        return super().save(**kwargs)
