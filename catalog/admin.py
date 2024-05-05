from django.contrib import admin

from catalog.models import Product, Category, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс для регистрации категории в административной панели."""
    list_display = ('pk', 'name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Класс для регистрации продукта в административной панели."""
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    """Класс для регистрации версии в административной панели."""
    list_display = ('number', 'name', 'product',)
    list_filter = ('product',)