from django.urls import path

from . import views


urlpatterns = [
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:item_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:item_id>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:item_id>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_history, name="order_history"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/orders/<int:order_id>/advance/", views.advance_order, name="advance_order"),
    path("staff/menu/", views.staff_menu, name="staff_menu"),
    path("staff/menu/new/", views.staff_menu_create, name="staff_menu_create"),
    path("staff/menu/<int:item_id>/edit/", views.staff_menu_edit, name="staff_menu_edit"),
    path("staff/menu/<int:item_id>/delete/", views.staff_menu_delete, name="staff_menu_delete"),
    path("staff/menu/<int:item_id>/toggle/", views.staff_menu_toggle, name="staff_menu_toggle"),
]
