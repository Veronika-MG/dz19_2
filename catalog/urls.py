from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home, contacts, index, categories, category_products

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('categories/', categories, name='categories'),
    path('<int:pk>products/', category_products, name='category_products'),
    path('contacts/', contacts, name='contacts')
]