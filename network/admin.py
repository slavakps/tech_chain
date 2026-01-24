from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import NetworkNode, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "supplier_link", "debt", "created_at")
    list_filter = ("city",)
    actions = [clear_debt]

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse("admin:network_networknode_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "network_node", "release_date")
