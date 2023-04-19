from django.db import models
from django.contrib.auth.models import AbstractUser
from .validator import validate_phone


class GeneralUser(models.Model):
    city = models.CharField(max_length=50, verbose_name="Ciudad")
    phone_number = models.CharField(
        max_length=8, verbose_name="Numero de Telefono", validators=[validate_phone]
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Inicio")
    address = models.TextField(verbose_name="Dirección", blank=True, null=True)

    class Meta:
        abstract = True


class User(AbstractUser, GeneralUser):
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Saldo",
        help_text="Saldo de cliente",
    )


class CustomerType(models.TextChoices):
    RETAILER = "", "Minorista"
    WHOLESALE = "2", "Mayorista"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    type = models.CharField(
        choices=CustomerType.choices,
        default=CustomerType.RETAILER,
        max_length=50,
        verbose_name="Tipo de Cliente",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["-user__date"]


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


class ProductCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre de la Categoria")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria de Producto"
        verbose_name_plural = "Categorias de Producto"
        ordering = ["name"]


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, verbose_name="Categoria"
    )
    name = models.CharField(max_length=50, verbose_name="Nombre del Producto")
    image = models.ImageField(upload_to="products", verbose_name="Imagen")
    stock = models.IntegerField(verbose_name="Stock", blank=True, null=True)
    base_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio base"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio mayorista"
    )
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Descuento", blank=True, null=True
    )
    description = models.TextField(verbose_name="Descripción", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["name"]


class Payment(models.Model):
    name = models.CharField(max_length=50, verbose_name="Tipo de Pago")
    credit_days = models.IntegerField(
        verbose_name="Días de Crédito", blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de Pago"
        verbose_name_plural = "Tipos de Pago"
        ordering = ["name"]


COIN = (
    ("C$", "Córdobas"),
    ("$", "Dolares"),
)


class Sale(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name="Cliente"
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, verbose_name="Tipo de Pago"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    coin = models.CharField(max_length=10, choices=COIN, default="C$")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Venta")

    def __str__(self):
        return self.customer.user.username

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-date"]


class SaleDetail(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Producto"
    )
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="Venta")
    amount = models.IntegerField(verbose_name="Cantidad")
    UnitPrice = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio Unitario"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"
        ordering = ["product"]
