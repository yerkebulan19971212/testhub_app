from rest_framework import serializers


class NameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    @staticmethod
    def get_name(obj):
        return obj.name_ru
