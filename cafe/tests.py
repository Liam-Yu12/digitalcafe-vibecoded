from decimal import Decimal

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import MenuItem, Order, OrderItem


class CafeTestDataMixin:
    def setUp(self):
        self.customer = User.objects.create_user(username="student", password="correct-horse")
        self.other_customer = User.objects.create_user(username="other", password="correct-horse")
        self.staff = User.objects.create_user(username="barista", password="correct-horse", is_staff=True)
        self.coffee = MenuItem.objects.create(name="House Coffee", description="Dark and comforting.", price=Decimal("3.50"))
        self.scone = MenuItem.objects.create(name="Berry Scone", description="Buttery and bright.", price=Decimal("4.25"))


class AuthenticationTests(CafeTestDataMixin, TestCase):
    def test_registration_creates_customer_only(self):
        response = self.client.post(reverse("register"), {"username": "new", "email": "new@example.com", "password1": "a-long-password-123", "password2": "a-long-password-123"})
        self.assertRedirects(response, reverse("menu"))
        user = User.objects.get(username="new")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_staff_area_requires_staff(self):
        self.client.login(username="student", password="correct-horse")
        response = self.client.get(reverse("staff_dashboard"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('staff_dashboard')}")


class MenuAndCartTests(CafeTestDataMixin, TestCase):
    def test_unavailable_item_is_visible_but_cannot_be_added(self):
        self.coffee.is_available = False
        self.coffee.save()
        response = self.client.get(reverse("menu"))
        self.assertContains(response, "Unavailable")
        self.client.post(reverse("cart_add", args=[self.coffee.pk]), {"quantity": 1})
        self.assertNotIn(str(self.coffee.pk), self.client.session.get("digital_cafe_cart", {}))

    def test_cart_can_add_update_and_remove(self):
        self.client.post(reverse("cart_add", args=[self.coffee.pk]), {"quantity": 2})
        self.assertEqual(self.client.session["digital_cafe_cart"][str(self.coffee.pk)], 2)
        self.client.post(reverse("cart_update", args=[self.coffee.pk]), {"quantity": 3})
        self.assertEqual(self.client.session["digital_cafe_cart"][str(self.coffee.pk)], 3)
        self.client.post(reverse("cart_remove", args=[self.coffee.pk]))
        self.assertNotIn(str(self.coffee.pk), self.client.session["digital_cafe_cart"])


class OrderTests(CafeTestDataMixin, TestCase):
    def place_order(self, user=None):
        self.client.login(username=(user or self.customer).username, password="correct-horse")
        self.client.post(reverse("cart_add", args=[self.coffee.pk]), {"quantity": 2})
        return self.client.post(reverse("checkout"))

    def test_checkout_snapshots_lines_and_clears_cart(self):
        response = self.place_order()
        order = Order.objects.get()
        line = order.items.get()
        self.assertRedirects(response, reverse("order_detail", args=[order.pk]))
        self.assertEqual(line.item_name, "House Coffee")
        self.assertEqual(line.unit_price, Decimal("3.50"))
        self.assertEqual(order.total, Decimal("7.00"))
        self.assertEqual(self.client.session.get("digital_cafe_cart", {}), {})

    def test_customer_cannot_view_another_customers_order(self):
        self.place_order()
        order = Order.objects.get()
        self.client.login(username="other", password="correct-horse")
        response = self.client.get(reverse("order_detail", args=[order.pk]))
        self.assertEqual(response.status_code, 404)

    def test_checkout_revalidates_availability(self):
        self.client.login(username="student", password="correct-horse")
        self.client.post(reverse("cart_add", args=[self.coffee.pk]), {"quantity": 1})
        self.coffee.is_available = False
        self.coffee.save()
        response = self.client.post(reverse("checkout"))
        self.assertRedirects(response, reverse("cart"))
        self.assertFalse(Order.objects.exists())

    def test_staff_can_only_advance_orders_forward(self):
        self.place_order()
        order = Order.objects.get()
        self.client.login(username="barista", password="correct-horse")
        for expected in [Order.Status.PREPARING, Order.Status.READY, Order.Status.COMPLETED]:
            self.client.post(reverse("advance_order", args=[order.pk]))
            order.refresh_from_db()
            self.assertEqual(order.status, expected)
        self.client.post(reverse("advance_order", args=[order.pk]))
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.COMPLETED)


class StaffMenuTests(CafeTestDataMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username="barista", password="correct-horse")

    def test_staff_can_create_and_toggle_menu_item(self):
        response = self.client.post(reverse("staff_menu_create"), {"name": "Tea", "description": "Steaming.", "price": "2.50", "is_available": "on", "display_order": "2"})
        self.assertRedirects(response, reverse("staff_menu"))
        item = MenuItem.objects.get(name="Tea")
        self.client.post(reverse("staff_menu_toggle", args=[item.pk]))
        item.refresh_from_db()
        self.assertFalse(item.is_available)

    def test_deleting_menu_item_preserves_order_snapshot(self):
        order = Order.objects.create(customer=self.customer)
        OrderItem.objects.create(order=order, menu_item=self.coffee, item_name=self.coffee.name, unit_price=self.coffee.price, quantity=1)
        self.client.post(reverse("staff_menu_delete", args=[self.coffee.pk]))
        line = order.items.get()
        self.assertIsNone(line.menu_item)
        self.assertEqual(line.item_name, "House Coffee")
