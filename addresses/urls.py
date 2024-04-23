from django.urls import path

from addresses.apps import AddressesConfig
from addresses.views import AddressCreateView, AddressListView, AddressDetailView, AddressUpdateView, AddressDeleteView, \
    toggle_activity

app_name = AddressesConfig.name

urlpatterns = [
    path('create/', AddressCreateView.as_view(), name='create'),
    path('', AddressListView.as_view(), name='list'),
    path('view/<int:pk>/', AddressDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', AddressUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', AddressDeleteView.as_view(), name='delete'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]