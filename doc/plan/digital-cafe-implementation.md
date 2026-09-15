# Digital Cafe Implementation Plan

This checklist implements the approved Digital Cafe requirements from
`doc/study/overall-project-structure.md`.

## 1. Repository and Django Foundation

- [x] Rename the current `master` branch to `main` and ensure `main` points at the initial scaffold.
- [x] Create a separate implementation branch from `main`.
- [x] Add Django and required development dependencies in `requirements.txt`.
- [x] Create `manage.py` and the Django project package with settings, root URLs, ASGI, and WSGI modules.
- [x] Configure SQLite, templates, static files, local media uploads, timezone, and development-safe defaults.
- [x] Add `.gitignore` entries for the SQLite database, media uploads, Python caches, virtual environments, and local environment files.
- [x] Create the main cafe app and register it in Django settings.
- [x] Add a minimal health/home route so the project can be run and smoke-tested early.

## 2. Data Model and Admin

- [x] Add a `MenuItem` model with name, description, decimal price, optional local photo, availability flag, display ordering, and timestamps.
- [x] Add an `Order` model tied to Django’s built-in user, with a generated order identifier, constrained status choices (`placed`, `preparing`, `ready`, `completed`), and timestamps.
- [x] Add an order-line model tied to `Order` and optionally the source `MenuItem`, storing copied item name, unit price, and quantity snapshots.
- [x] Add model validation and database constraints for positive prices/quantities and valid order statuses.
- [x] Add calculated order totals from persisted order-line snapshots.
- [x] Generate and apply initial migrations.
- [x] Register menu items and orders in Django admin with useful list displays, filters, search, and staff-manageable availability/status fields.
- [x] Add a management command or document the admin workflow for creating staff users; keep public registration customer-only.

## 3. Authentication and Roles

- [x] Add public customer registration using a Django form that creates ordinary non-staff users only.
- [x] Add login and logout routes using Django authentication.
- [x] Add navigation and redirects appropriate for anonymous customers, authenticated customers, and staff.
- [x] Add server-side staff authorization for every staff view using login and `is_staff` checks.
- [x] Ensure customers can only access their own orders and cannot access staff operations.

## 4. Customer Menu and Cart

- [x] Add a customer menu view showing all menu items, including unavailable items with a clear `Unavailable` label.
- [x] Prevent unavailable items from being added to the cart even if a request is manually crafted.
- [x] Build a session-backed cart with add, quantity update, and remove operations.
- [x] Validate cart quantities as positive integers and remove or reject invalid entries safely.
- [x] Display item prices, line subtotals, cart subtotal, availability state, and empty-cart guidance.
- [x] Add responsive templates and vintage cafe styling for the menu and cart.

## 5. Checkout and Customer Orders

- [x] Add an authenticated, payment-free checkout confirmation page for pickup requests.
- [x] Revalidate every cart item’s existence and availability at checkout.
- [x] Create orders transactionally with line-item name/price snapshots and quantities.
- [x] Clear the session cart only after a successful order is created.
- [x] Reject checkout for an empty or invalid cart with a useful message.
- [x] Add customer order history scoped to the current user.
- [x] Add customer order detail/status views showing order identifier, lines, total, and current pipeline status.
- [x] Add clear status badges for `Placed`, `Preparing`, `Ready`, and `Completed`.

## 6. Staff Menu Management

- [x] Add staff menu listing with availability and edit/delete controls.
- [x] Add staff create and edit forms for menu name, description, price, photo upload, display ordering, and availability.
- [x] Add a staff availability toggle that changes customer ordering behavior without deleting the menu item.
- [x] Add delete confirmation and preserve historical order-line snapshots when a menu item is removed.
- [x] Ensure local media URLs and upload handling work in development.

## 7. Staff Order Operations

- [x] Add a staff incoming-orders dashboard ordered by newest or operational priority.
- [x] Show customer, order identifier, line items, total, created time, and current status.
- [x] Add a forward-only status action for each order.
- [x] Enforce transitions strictly as `placed` → `preparing` → `ready` → `completed` on the server.
- [x] Reject skipped, backward, or repeated transitions with an explanatory message.
- [x] Restrict all order operations to staff users.

## 8. Visual System and Templates

- [x] Create a shared base template with navigation, authentication state, cart count, flash messages, and responsive layout.
- [x] Implement a warm cream, coffee-brown, muted red/cranberry, and ink color palette.
- [x] Use serif or typewriter-inspired display typography and readable body typography.
- [x] Add subtle vintage cafe details such as borders, signage-style headings, paper textures, or menu-card treatments without harming accessibility.
- [x] Provide graceful image fallbacks for menu items without uploaded photos.
- [x] Add responsive layouts for phone, tablet, and desktop widths.
- [x] Add visible keyboard focus states, form labels, semantic headings, and sufficient color contrast.

## 9. Automated Verification

- [x] Add tests for registration, login, logout, and customer-only public registration.
- [x] Add tests for customer/staff authorization boundaries.
- [x] Add tests for menu listing, unavailable labels, and unavailable-item add-to-cart rejection.
- [x] Add tests for cart add/update/remove behavior and invalid quantities.
- [x] Add tests for transactional checkout, empty-cart rejection, availability revalidation, snapshots, and totals.
- [x] Add tests proving customers cannot view other customers’ orders.
- [x] Add tests for the valid status pipeline and invalid transition rejection.
- [x] Add tests for staff menu CRUD and availability toggles.
- [x] Run Django system checks, migrations, and the full test suite.
- [ ] Perform a manual responsive smoke test of customer and staff flows.

## 10. Rendezvous and Documentation

- [ ] Review the implementation branch status and diff for unintended files or secrets.
- [ ] Confirm the app runs from a clean checkout with documented setup commands.
- [ ] Merge the implementation branch into `main` only after verification succeeds.
- [ ] Add living documentation under `doc/wiki/` covering setup, models, routes, authentication roles, staff account creation, media configuration, and customer/staff workflows.
- [ ] Confirm the final `main` branch is clean and the documented commands remain accurate.

## Approved Product Decisions

- The repository branch is renamed from `master` to `main` before implementation, and the implementation branch is created from `main`.
- Unavailable menu items remain visible to customers, are labeled `Unavailable`, and cannot be ordered.
- Public registration creates customer accounts only.
- Staff accounts are created through Django admin or a management command.
- Menu photos use local image uploads in the first version.
- Staff may only move orders forward through the four statuses; no backward transitions or resets are supported.
- Checkout is a payment-free cafe pickup request.
