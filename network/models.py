from django.core.exceptions import ValidationError
from django.db import models


class NetworkNode(models.Model):
    MAX_LEVEL = 2

    name = models.CharField(max_length=255)

    # Контакты
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=20)

    supplier = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="clients"
    )

    debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name

    @property
    def level(self):
        level = 0
        supplier = self.supplier
        while supplier:
            level += 1
            supplier = supplier.supplier
        return level

    def clean(self):
        if self.pk and self.supplier_id == self.pk:
            raise ValidationError("Узел не может быть своим поставщиком.")

        level = 0
        supplier = self.supplier
        visited = set()

        while supplier:
            if supplier.pk in visited:
                raise ValidationError("Обнаружен цикл поставщиков.")
            visited.add(supplier.pk)

            level += 1
            if level > self.MAX_LEVEL:
                raise ValidationError("Максимальная глубина сети — 3 уровня.")

            supplier = supplier.supplier

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    network_node = models.ForeignKey(
        NetworkNode,
        related_name="products",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["release_date"]

    def __str__(self):
        return f"{self.name} ({self.model})"
