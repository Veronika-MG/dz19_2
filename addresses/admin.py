from django.contrib import admin

from addresses.models import Address


@admin.register(Address)
class ProductAdmin(admin.ModelAdmin):
    """Класс для регистрации адреса в административной панели."""
    list_display = ('title', 'location', 'image', 'date_of_creation', 'is_published', "views_count", "slug",)


