from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
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
    search_fields = ("name", "city", "country")
    readonly_fields = ("created_at",)
    list_select_related = ("supplier",)
    actions = [clear_debt]

    def supplier_link(self, obj):
        if not obj.supplier:
            return "-"
        ct = ContentType.objects.get_for_model(obj.supplier)
        url = reverse(f"admin:{ct.app_label}_{ct.model}_change", args=[obj.supplier.pk])
        return format_html('<a href="{}">{}</a>', url, obj.supplier.name)

    supplier_link.short_description = "Поставщик"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "network_node", "release_date")
    list_select_related = ("network_node",)
    search_fields = ("name", "model")
    list_filter = ("release_date",)
