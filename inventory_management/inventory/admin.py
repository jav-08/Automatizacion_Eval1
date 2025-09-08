from django.contrib import admin
from .models import InventoryItem, Tag, InventoryProveedor

admin.site.register(InventoryItem)
admin.site.register(Tag)
admin.site.register(InventoryProveedor)