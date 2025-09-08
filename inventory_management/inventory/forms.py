from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import InventoryItem, InventoryProveedor, Tag

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InventoryItemForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(  
        queryset=Tag.objects.all(),
        required=False,
        label="Etiquetas",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})  
    )

    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'tags', 'expiration_date', 'serial_number', 'description']
        labels = {
            'name': 'Nombre',
            'quantity': 'Stock',
            'expiration_date': 'Fecha de vencimiento',
            'serial_number': 'Número de serie',
            'description': 'Descripción',
        }
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = InventoryProveedor
        fields = ['name_p', 'email_p', 'number_p', 'description_p']
        labels = {
            'name_p': 'Nombre',
            'email_p': 'Correo',
            'number_p': 'Número telefónico',
            'description_p': 'Descripción',
        }
