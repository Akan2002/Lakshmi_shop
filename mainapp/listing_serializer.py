from rest_framework import serializers


class ColorListingField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'color_id': value.id,
            'color': value.name, 
        }


class SizeListingField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'size_id': value.id,
            'size': value.name,
        }