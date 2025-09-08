from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm, ProveedorForm
from .models import InventoryItem, InventoryProveedor
from inventory_management.settings import LOW_QUANTITY, VERY_LOW_QUANTITY
from django.contrib import messages
from datetime import date, timedelta

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views import View
from .models import InventoryItem

class Index(TemplateView):
	template_name = 'inventory/index.html'


CRITICAL_QUANTITY = 5 
LOW_QUANTITY = 15
EXPIRATION_THRESHOLD_DAYS = 28

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("q", "")
        
        items = InventoryItem.objects.filter(user=request.user).order_by('id')

        if query:
            items = items.filter(name__icontains=query)  # busca insensible a mayúsculas/minúsculas

        # INVENTARIO CRÍTICO (cantidad <= 0)
        critical_inventory = InventoryItem.objects.filter(
            user=request.user,
            quantity__lte=CRITICAL_QUANTITY
        )

        if critical_inventory.exists():
            count = critical_inventory.count()
            messages.error(request, f'{count} producto{"s" if count > 1 else ""} bajo umbral critico de stock')

        # INVENTARIO BAJO (cantidad <= LOW_QUANTITY pero > CRITICAL)
        low_inventory = InventoryItem.objects.filter(
            user=request.user,
            quantity__gt=CRITICAL_QUANTITY,
            quantity__lte=LOW_QUANTITY
        )

        if low_inventory.exists():
            count = low_inventory.count()
            messages.warning(request, f'{count} producto{"s" if count > 1 else ""} bajo umbral minimo de stock')

        # PRODUCTOS PRÓXIMOS A VENCER
        today = date.today()
        expiration_limit = today + timedelta(days=EXPIRATION_THRESHOLD_DAYS)

        expiring_soon = InventoryItem.objects.filter(
            user=request.user,
            expiration_date__isnull=False,
            expiration_date__range=[today, expiration_limit]
        )

        if expiring_soon.exists():
            count = expiring_soon.count()
            messages.warning(request, f'{count} producto{"s" if count > 1 else ""} cerca de la fecha de vencimiento')

        # IDs para pintar cantidades bajas o críticas en tabla
        critical_inventory_ids = critical_inventory.values_list('id', flat=True)
        low_inventory_ids = low_inventory.values_list('id', flat=True)

        return render(request, 'inventory/dashboard.html', {
            'items': items,
            'low_inventory_ids': list(low_inventory_ids),
            'critical_inventory_ids': list(critical_inventory_ids),
        })

class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')

		return render(request, 'inventory/signup.html', {'form': form})

class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'


#Informe
class InformeProductoView(DetailView):
    model = InventoryItem
    template_name = 'inventory/informe.html'
    context_object_name = 'producto'





#Proveedor
class ProveedorListView(LoginRequiredMixin,ListView):
    model = InventoryProveedor
    template_name = 'inventory/proveedores.html'  
    context_object_name = 'proveedores'

class ProveedorCreateView(LoginRequiredMixin,CreateView):
    model = InventoryProveedor
    form_class = ProveedorForm
    template_name = 'inventory/proveedor_form.html'
    success_url = reverse_lazy('proveedores')

class ProveedorUpdateView(LoginRequiredMixin,UpdateView):
    model = InventoryProveedor
    form_class = ProveedorForm
    template_name = 'inventory/proveedor_form.html'
    success_url = reverse_lazy('proveedores')

class ProveedorDeleteView(LoginRequiredMixin,DeleteView):
    model = InventoryProveedor
    template_name = 'inventory/proveedor_confirm_delete.html'
    success_url = reverse_lazy('proveedores')



#compra
class PurchaseView(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=request.user).order_by('name')
        return render(request, 'inventory/purchase.html', {'items': items})

    def post(self, request):
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 0))

        item = get_object_or_404(InventoryItem, id=product_id, user=request.user)

        if quantity <= 0:
            messages.error(request, "La cantidad debe ser mayor a 0.")
            return redirect("purchase")

        if item.quantity < quantity:
            messages.error(request, f"No hay suficiente stock disponible de {item.name}. Stock actual: {item.quantity}")
            return redirect("purchase")

        # Descontar stock
        item.quantity -= quantity
        item.save()

        messages.success(request, f"Compra realizada. Se descontaron {quantity} unidades de {item.name}.")
        return redirect("dashboard")