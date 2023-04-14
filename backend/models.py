from django.db import models
from django.contrib.auth.models import AbstractUser


class GeneralUser(models.Model):
    city = models.CharField(max_length=50, verbose_name="Ciudad")
    phone_number = models.CharField(max_length=20, verbose_name="Numero de Telefono")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Inicio")
    address = models.CharField(
        max_length=100, verbose_name="Direccion", blank=True, null=True
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Costo",
        help_text="Costo de compra en córdobas",
    )


class CustomerTypes(models.TextChoices):
    RETAILER = "", "Cliente"
    WHOLESALE = "2", "Proveedor"


# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
#     type = models.CharField(
#         choices=CustomerTypes.choices,
#         max_length=50,
#         verbose_name="Tipo de Cliente",
#         blank=True,
#         null=True,
#     )

#     def __str__(self):
#         return self.user.username

#     class Meta:
#         verbose_name = "Cliente"
#         verbose_name_plural = "Clientes"
#         ordering = ["-user__date"]


class SupplierCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre de la Categoria")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria de Proveedor"
        verbose_name_plural = "Categorias de Proveedor"
        ordering = ["name"]


class Supplier(GeneralUser):
    name = models.CharField(max_length=50, verbose_name="Nombre del Proveedor")
    category = models.ManyToManyField(SupplierCategory, verbose_name="Categoria")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["name"]
