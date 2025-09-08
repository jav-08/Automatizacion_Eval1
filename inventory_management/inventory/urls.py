from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard, AddItem, EditItem, DeleteItem, InformeProductoView, ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView, PurchaseView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('informe/<int:pk>/', InformeProductoView.as_view(), name='informe-producto'),

    path('proveedores/', ProveedorListView.as_view(), name='proveedores'),
    path('proveedores/agregar/', ProveedorCreateView.as_view(), name='agregar-proveedor'),
    path('proveedores/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='editar-proveedor'),
    path('proveedores/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='eliminar-proveedor'),

    path('purchase/', PurchaseView.as_view(), name='purchase'),
]