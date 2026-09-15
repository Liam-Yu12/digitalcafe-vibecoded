from decimal import Decimal

from .models import MenuItem


class Cart:
    SESSION_KEY = "digital_cafe_cart"

    def __init__(self, request):
        self.session = request.session
        self.data = self.session.setdefault(self.SESSION_KEY, {})

    def add(self, item, quantity=1):
        key = str(item.pk)
        self.data[key] = int(self.data.get(key, 0)) + quantity
        self.save()

    def set_quantity(self, item_id, quantity):
        if quantity > 0:
            self.data[str(item_id)] = quantity
        else:
            self.data.pop(str(item_id), None)
        self.save()

    def remove(self, item_id):
        self.data.pop(str(item_id), None)
        self.save()

    def clear(self):
        self.session.pop(self.SESSION_KEY, None)
        self.session.modified = True
        self.data = {}

    def save(self):
        self.session[self.SESSION_KEY] = self.data
        self.session.modified = True

    def items(self):
        products = MenuItem.objects.filter(pk__in=self.data).order_by("display_order", "name")
        result = []
        for product in products:
            quantity = int(self.data.get(str(product.pk), 0))
            if quantity:
                result.append({"product": product, "quantity": quantity, "line_total": product.price * quantity})
        return result

    @property
    def count(self):
        return sum(int(quantity) for quantity in self.data.values())

    @property
    def total(self):
        return sum((line["line_total"] for line in self.items()), Decimal("0.00"))
