from django.contrib import admin
from .models import *

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'agent_firstname', 'agent_name', 'agent_telephone')
    search_fields = ('name',)
    list_editable = ('name','agent_firstname', 'agent_name')

@admin.register(Supply)
class SupplyApdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_supply', 'supplier')
    list_editable = ('date_supply', 'supplier')

@admin.register(Pos_supply)
class Pos_supplyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'supply')
    list_editable = ('product', 'supply')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_editable = ('title',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_editable = ('title',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'delivery_address', 'date_create', 'delivery_type', 'FIO_customer')
    search_fields = ('FIO_customer',)
    list_filter = ('delivery_type',)

@admin.register(Pos_order)
class Pos_orderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'order', 'count', 'discount')
    list_editable = ('product', 'order', 'count', 'discount')


@admin.register(Parametr)
class ParametrAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_editable = ('name', )

@admin.register(Pos_parametr)
class Pos_parametrAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'parametr')
    list_editable = ('product', 'parametr')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'create_date', 'exists', 'category')
    list_editable = ('name', 'price', 'exists', 'category')
    search_fields = ('name',)
    list_filter = ('category', 'exists')


