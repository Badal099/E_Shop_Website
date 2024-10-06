from django.contrib import admin
from Store.models import Product, Categories, Carousal, Customer, Order

# Register your models here.
@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']

@admin.register(Categories)
class CategoriesModel(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Carousal)
class CarousalModel(admin.ModelAdmin):
    list_display = ['id', 'image']

@admin.register(Customer)
class CustomerModel(admin.ModelAdmin):
    list_display = ['name', 'phone']

@admin.register(Order)
class OrderModel(admin.ModelAdmin):
    list_display = ['product', 'customer', 'phone']