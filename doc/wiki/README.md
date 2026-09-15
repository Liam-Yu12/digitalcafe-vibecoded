# Digital Cafe

Digital Cafe is a server-rendered Django + SQLite ordering app for a campus
cafe. Customers can browse the menu, create pickup requests, and follow their
orders. Staff can maintain the menu and move orders through the fulfillment
queue.

## Setup

The project targets Python 3.12+ and Django 5.

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py runserver
```

Open `http://127.0.0.1:8000/` after starting the development server.

Run checks and tests with:

```bash
./.venv/bin/python manage.py check
./.venv/bin/python manage.py test cafe
```

The local SQLite database is `db.sqlite3`. It is intentionally ignored by git.
Uploaded menu photos are stored below `media/menu/` during development and are
also ignored by git.

## Accounts and Roles

Public registration at `/accounts/register/` creates customer accounts only.
Customers can log in, log out, place pickup requests, and see only their own
orders.

Create staff accounts with Django's admin user creation flow:

```bash
./.venv/bin/python manage.py createsuperuser
```

The created account can use `/admin/` and the custom staff desk at `/staff/`.
An existing user can also be marked as staff in Django admin by enabling
`Staff status`. Public registration never grants staff or superuser access.

## Models

### `MenuItem`

Stores a menu item's name, description, decimal price, optional local photo,
availability toggle, display order, and timestamps. An unavailable item stays
visible on the customer menu but is labeled `Unavailable` and cannot be added
to the cart.

### `Order`

Belongs to a Django user and stores timestamps and one of four statuses:

1. `placed`
2. `preparing`
3. `ready`
4. `completed`

The custom staff desk only exposes the next forward transition. The server
does not support skipping, reversing, or resetting a status.

### `OrderItem`

Stores the order, optional source menu item, copied item name, unit price, and
quantity. The copied name and price preserve the order receipt if the menu item
is edited or removed later. Totals are calculated from these snapshots.

## Routes

Customer routes include `/menu/`, `/cart/`, `/checkout/`, `/orders/`, and
`/orders/<id>/`. Cart writes use POST requests and checkout requires login.

Authentication routes are `/accounts/login/`, `/accounts/logout/`, and
`/accounts/register/`.

Staff routes are under `/staff/`:

- `/staff/` shows the incoming order queue.
- `/staff/orders/<id>/advance/` moves an order one step forward.
- `/staff/menu/` manages menu items.
- `/staff/menu/new/` creates a menu item.
- `/staff/menu/<id>/edit/` edits a menu item.
- `/staff/menu/<id>/toggle/` changes availability.
- `/staff/menu/<id>/delete/` removes a menu item without deleting historical order-line snapshots.

All staff routes require an authenticated user with Django `is_staff=True`.

## Product Behavior

The cart is stored in the user's session, allowing visitors to browse and
build a tray before signing in. Checkout is a payment-free pickup request.
Checkout rechecks menu availability inside an atomic transaction, creates the
order and snapshot lines, then clears the session cart.

The interface uses cream paper tones, coffee brown, muted red, serif display
headings, menu-card borders, and small cafe-sign details. Menu images are local
uploads with an illustrated fallback when no photo is provided.
