from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(SupplierCategory)
admin.site.register(Supplier)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Sale)
admin.site.register(SaleDetail)
