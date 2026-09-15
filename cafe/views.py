from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CustomerRegistrationForm, MenuItemForm, QuantityForm
from .models import MenuItem, Order, OrderItem


def home(request):
    return redirect("menu")


def register(request):
    if request.user.is_authenticated:
        return redirect("menu")
    form = CustomerRegistrationForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        messages.success(request, "Welcome to Digital Cafe!")
        return redirect("menu")
    return render(request, "registration/register.html", {"form": form})


def menu(request):
    return render(request, "cafe/menu.html", {"items": MenuItem.objects.all()})


@require_POST
def cart_add(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    if not item.is_available:
        messages.error(request, f"{item.name} is currently unavailable.")
        return redirect("menu")
    form = QuantityForm(request.POST)
    if form.is_valid():
        Cart(request).add(item, form.cleaned_data["quantity"])
        messages.success(request, f"{item.name} added to your tray.")
    return redirect(request.POST.get("next") or "menu")


@require_POST
def cart_update(request, item_id):
    form = QuantityForm(request.POST)
    if form.is_valid():
        Cart(request).set_quantity(item_id, form.cleaned_data["quantity"])
    return redirect("cart")


@require_POST
def cart_remove(request, item_id):
    Cart(request).remove(item_id)
    messages.info(request, "Item removed from your tray.")
    return redirect("cart")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cafe/cart.html", {"cart": cart, "items": cart.items()})


@login_required
def checkout(request):
    cart = Cart(request)
    items = cart.items()
    if not items:
        messages.info(request, "Your tray is empty. Add something delicious first.")
        return redirect("menu")
    unavailable = [line["product"].name for line in items if not line["product"].is_available]
    if request.method == "POST":
        if unavailable:
            messages.error(request, f"Unavailable items cannot be ordered: {', '.join(unavailable)}.")
            return redirect("cart")
        with transaction.atomic():
            order = Order.objects.create(customer=request.user)
            OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        menu_item=line["product"],
                        item_name=line["product"].name,
                        unit_price=line["product"].price,
                        quantity=line["quantity"],
                    )
                    for line in items
                ]
            )
        cart.clear()
        messages.success(request, f"Order #{order.pk} is in the kitchen queue.")
        return redirect("order_detail", order_id=order.pk)
    return render(request, "cafe/checkout.html", {"cart": cart, "items": items, "unavailable": unavailable})


@login_required
def order_history(request):
    return render(request, "cafe/order_history.html", {"orders": request.user.orders.all()})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(request.user.orders.prefetch_related("items"), pk=order_id)
    return render(request, "cafe/order_detail.html", {"order": order})


def staff_required(view):
    return user_passes_test(lambda user: user.is_authenticated and user.is_staff, login_url="login")(view)


@staff_required
def staff_dashboard(request):
    orders = Order.objects.select_related("customer").prefetch_related("items")
    return render(request, "staff/dashboard.html", {"orders": orders})


@require_POST
@staff_required
def advance_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if not order.next_status:
        messages.info(request, "That order is already completed.")
    else:
        order.status = order.next_status
        order.save(update_fields=["status", "updated_at"])
        messages.success(request, f"Order #{order.pk} moved to {order.get_status_display()}.")
    return redirect("staff_dashboard")


@staff_required
def staff_menu(request):
    return render(request, "staff/menu.html", {"items": MenuItem.objects.all()})


@staff_required
def staff_menu_create(request):
    form = MenuItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Menu item added.")
        return redirect("staff_menu")
    return render(request, "staff/menu_form.html", {"form": form, "title": "Add menu item"})


@staff_required
def staff_menu_edit(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    form = MenuItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, "Menu item updated.")
        return redirect("staff_menu")
    return render(request, "staff/menu_form.html", {"form": form, "title": f"Edit {item.name}"})


@require_POST
@staff_required
def staff_menu_delete(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    item.delete()
    messages.success(request, "Menu item removed.")
    return redirect("staff_menu")


@require_POST
@staff_required
def staff_menu_toggle(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    item.is_available = not item.is_available
    item.save(update_fields=["is_available", "updated_at"])
    messages.success(request, f"{item.name} is now {'available' if item.is_available else 'unavailable'}.")
    return redirect("staff_menu")
