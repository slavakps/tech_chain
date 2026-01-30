from rest_framework import serializers

from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "model", "release_date")


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    level = serializers.SerializerMethodField()

    class Meta:
        model = NetworkNode
        fields = (
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "debt",
            "created_at",
            "products",
            "level",
        )
        read_only_fields = ("debt", "created_at")

    def get_level(self, obj):
        return obj.level

    def validate_supplier(self, value):
        if self.instance and value == self.instance:
            raise serializers.ValidationError("Нельзя указать самого себя поставщиком.")
        return value
