from django.db import models
from django.core.exceptions import ValidationError

class NodeType(models.IntegerChoices):
    FACTORY = 0, "Завод"
    RETAIL = 1, "Розничная сеть"
    ENTREPRENEUR = 2, "ИП"


class NetworkNode(models.Model):
    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ["created_at"]

    name = models.CharField(max_length=255)

    node_type = models.IntegerField(choices=NodeType.choices)

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

    @property
    def level(self):
        if not self.supplier:
            return 0
        if not self.supplier.supplier:
            return 1
        return 2

    def clean(self):
        # 1. Завод не может иметь поставщика
        if self.node_type == NodeType.FACTORY and self.supplier:
            raise ValidationError("Завод не может иметь поставщика.")

        # 2. Проверка глубины (не больше 2 переходов вверх)
        level = 0
        current_supplier = self.supplier

        while current_supplier:
            level += 1
            if level > 2:
                raise ValidationError("Превышена допустимая глубина иерархии (максимум 3 уровня).")
            current_supplier = current_supplier.supplier

        # 3. Проверка циклов
        current_supplier = self.supplier
        while current_supplier:
            if current_supplier == self:
                raise ValidationError("Обнаружен цикл в иерархии поставщиков.")
            current_supplier = current_supplier.supplier

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["release_date"]

    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    network_node = models.ForeignKey(
        NetworkNode,
        related_name="products",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} ({self.model})"
