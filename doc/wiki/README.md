# Digital Cafe

Digital Cafe is a server-rendered Django application for browsing a cafe menu,
building a session-based cart, and submitting payment-free pickup requests. It
uses SQLite by default and provides a customer-facing ordering flow, a custom
staff desk, and Django admin.

## Setup

The project does not declare a minimum Python version. It requires the
dependencies listed in `requirements.txt`: Django 5.x (`Django>=5.0,<6.0`)
and Pillow (`Pillow>=10.0,<12.0`). From the project root:

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py runserver
```

Open `http://127.0.0.1:8000/`. The root URL redirects to `/menu/`.

Useful development commands are:

```bash
./.venv/bin/python manage.py check
./.venv/bin/python manage.py test cafe
```

The default database is SQLite at `db.sqlite3`. The project settings use
`DEBUG = True`, an in-code development secret key, and an explicit development
`ALLOWED_HOSTS` list containing `localhost`, `127.0.0.1`, and the current
CodeRange forwarded hostname `itent-45-1t-2526-p27.coderange.net`; these
settings are for local development, not production.

## Accounts and Roles

Public registration is available at `/accounts/register/`. It asks for a
username, email address, and password, logs the new user in, and explicitly
sets `is_staff` and `is_superuser` to false. Customers can log in at
`/accounts/login/` and log out with the POST form at `/accounts/logout/`.

Create an initial administrator and staff account with:

```bash
./.venv/bin/python manage.py createsuperuser
```

The superuser can access `/admin/` and also satisfies the custom staff check
because Django superusers have staff status. To grant staff-desk access to an
existing user, use Django admin and enable that user's `Staff status`
(`is_staff`). The custom staff desk does not require `is_superuser`; it
requires an authenticated user with `is_staff=True`.

## Models

### `MenuItem`

Fields:

- `name`: required text, maximum 120 characters.
- `description`: required text.
- `price`: decimal with up to 8 digits and 2 decimal places, minimum `0.01`.
- `photo`: optional image uploaded under `menu/`.
- `is_available`: boolean, defaulting to true.
- `display_order`: non-negative integer, defaulting to zero.
- `created_at` and `updated_at`: automatic timestamps.

Querysets order menu items by `display_order` and then `name`. An unavailable
item remains visible on the customer menu but cannot be added to the cart.

### `Order`

An order belongs to Django's configured user model through `customer` and has
`status`, `created_at`, and `updated_at` fields. The status choices and labels
are:

1. `placed` (Placed)
2. `preparing` (Preparing)
3. `ready` (Ready)
4. `completed` (Completed)

Orders are ordered newest first. `total` sums the related order-item line
totals. `next_status` returns only the next forward transition, or no value
when the order is completed.

### `OrderItem`

An order item stores its `order`, an optional `menu_item` reference,
`item_name`, `unit_price`, and positive `quantity`. The source menu-item
foreign key uses `SET_NULL`, so deleting a menu item does not delete existing
order lines. Checkout copies the menu item's name and price into the order
item; receipts and totals therefore use those snapshots even if the menu item
is later edited or deleted. `line_total` is `unit_price * quantity`.

## Routes

The following routes are registered by `cafe_site/urls.py` and `cafe/urls.py`.
Methods listed as POST-only are enforced by `@require_POST`.

### General and authentication

| Method | Path | Access and behavior |
| --- | --- | --- |
| GET | `/` | Redirects to `/menu/`. |
| GET | `/admin/` | Django admin; requires Django admin authorization. |
| GET, POST | `/accounts/login/` | Django login form. |
| POST | `/accounts/logout/` | Logs out; redirects to `/menu/`. |
| GET, POST | `/accounts/register/` | Creates and logs in a customer account. Authenticated users are redirected to the menu. |

### Customer menu, cart, and orders

| Method | Path | Access and behavior |
| --- | --- | --- |
| GET | `/menu/` | Displays all menu items, including unavailable items. |
| GET | `/cart/` | Displays the current session cart, quantities, and total. |
| POST | `/cart/add/<item_id>/` | Adds a quantity from 1 through 99; unavailable items are rejected. |
| POST | `/cart/update/<item_id>/` | Sets a quantity from 1 through 99. |
| POST | `/cart/remove/<item_id>/` | Removes an item from the session cart. |
| GET, POST | `/checkout/` | Requires login. GET reviews the cart; POST creates an order if all items are available. |
| GET | `/orders/` | Requires login; lists only the current user's orders. |
| GET | `/orders/<order_id>/` | Requires login; shows the order only if it belongs to the current user, otherwise returns 404. |

### Staff desk

Every staff route requires an authenticated user with `is_staff=True`.

| Method | Path | Behavior |
| --- | --- | --- |
| GET | `/staff/` | Displays the order queue with customer, items, totals, and status. |
| POST | `/staff/orders/<order_id>/advance/` | Moves an order from placed to preparing, preparing to ready, or ready to completed. Completed orders remain completed. |
| GET | `/staff/menu/` | Lists all menu items for staff. |
| GET, POST | `/staff/menu/new/` | Shows or submits the menu-item form, including an optional image upload. |
| GET, POST | `/staff/menu/<item_id>/edit/` | Shows or submits edits to a menu item, including an optional image upload. |
| POST | `/staff/menu/<item_id>/delete/` | Deletes a menu item; existing order-item snapshots remain. |
| POST | `/staff/menu/<item_id>/toggle/` | Flips `is_available`. |

The custom staff desk permits only forward order transitions. It has no route
for skipping, reversing, or resetting a status.

## Customer Workflow

1. Browse `/menu/`. Available items can be added to the tray. Unavailable
   items remain visible but cannot be added.
2. Review `/cart/`. Quantities can be updated from 1 through 99, or lines can
   be removed. The cart can be built before login.
3. Open `/checkout/`. An unauthenticated customer is redirected to login. An
   empty cart redirects back to the menu.
4. Submit the pickup request. Checkout rechecks availability, creates the
   order and its lines in an atomic transaction, clears the session cart, and
   redirects to the order detail page.
5. Use `/orders/` and `/orders/<order_id>/` to view the authenticated user's
   own order history and status. A customer cannot view another customer's
   order.

The cart is stored in the session under `digital_cafe_cart`. Cart item lookup
uses current `MenuItem` rows; items that no longer exist are not returned by
the cart listing. Checkout does not charge a payment method or collect pickup
time, name, contact information, or other customer-provided fulfillment
details.

## Staff Workflow

1. Create a superuser with `createsuperuser`, or mark an existing user as
   staff in Django admin by enabling `Staff status`.
2. Open `/staff/` to review the incoming order queue.
3. Advance each order manually from Placed to Preparing, Ready, and Completed.
4. Open `/staff/menu/` to create, edit, toggle, or delete menu items.
5. Use the menu form's file field to upload an optional local menu photo.

Staff can use Django admin at `/admin/` when they have the required admin
permissions. The custom staff desk itself checks only authentication and
`is_staff`.

## Media and Static Files

Menu photos submitted through the staff create or edit forms are stored below
`MEDIA_ROOT`, which is the project-level `media/` directory, using the
`menu/` upload path. In the current development configuration they are
available at URLs beginning with `/media/` because `cafe_site/urls.py` appends
the media URL pattern when `DEBUG` is true. The `media/` directory is ignored
by git. This debug URL serving is not a production media-serving setup.

Static assets use `STATIC_URL = "static/"`, are sourced from the project
`static/` directory, and have `STATIC_ROOT = staticfiles/` for collection.

## Testing

Run Django's checks and the app test suite with:

```bash
./.venv/bin/python manage.py check
./.venv/bin/python manage.py test cafe
```

`cafe/tests.py` currently covers:

- customer registration and the guarantee that public registration does not
  create staff or superuser accounts;
- rejection of non-staff access to the staff dashboard;
- visibility and add rejection for unavailable menu items;
- session-cart add, update, and remove behavior;
- checkout order creation, copied item name and price, totals, and cart
  clearing;
- isolation of customer order detail pages;
- checkout revalidation when an item becomes unavailable;
- the three forward staff order transitions and completed-order behavior;
- staff menu-item creation and availability toggling; and
- preservation of copied order-line data after deleting its menu item.

The tests use Django's test database and do not require a pre-existing local
`db.sqlite3`.

## Known Limitations

- Checkout is a pickup request only; there is no payment processing, pickup
  scheduling, receipt email, or customer notification system.
- Orders have no customer-entered pickup name, contact information, notes, or
  location field.
- Staff status is advanced manually through the custom desk; there is no
  automated kitchen or inventory integration.
- The application uses Django's built-in `User` model and does not provide a
  separate profile or role model.
- The project configuration is development-oriented (`DEBUG = True`, a hard-
  coded secret key, workspace-specific `ALLOWED_HOSTS`, SQLite, and debug media
  serving).
- No production deployment, object storage, media access control, or static
  asset deployment configuration is included.
