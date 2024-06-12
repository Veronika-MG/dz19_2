from django.urls import path

from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import home, contacts, index, categories, category_products, ProductDetailView, ProductListView, \
    ProductCreateView, ProductUpdateView, ProductDeleteView, VersionListView, VersionCreateView, VersionUpdateView, \
    VersionDetailView, VersionDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('categories/', categories, name='categories'),
    path('<int:pk>products/', category_products, name='category_products'),
    path('contacts/', contacts, name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    path('view/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='view'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('versions/<int:pk>', VersionListView.as_view(), name='versions'),
    path('versions/create/<int:pk>', VersionCreateView.as_view(), name='version_create'),
    path('versions/edit/<int:pk>/', VersionUpdateView.as_view(), name='version_edit'),
    path('versions/view/<int:pk>/', VersionDetailView.as_view(), name='version_view'),
    path('versions/delete/<int:pk>/', VersionDeleteView.as_view(), name='version_delete'),
]