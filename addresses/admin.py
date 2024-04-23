from django.contrib import admin

from addresses.models import Address


@admin.register(Address)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'image', 'date_of_creation', 'is_published', "views_count", "slug",)


