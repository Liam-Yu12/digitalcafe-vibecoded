# Digital Cafe: Overall Project Structure Study

## Request Summary

Build a server-rendered Django + SQLite campus cafe application with two roles:

- Customers can register, authenticate, browse available menu items, manage a cart, place orders, and review order history and statuses.
- Staff can authenticate, manage menu items and stock visibility, inspect incoming orders, and advance order statuses from `placed` through `completed`.
- The interface should use a warm, vintage cafe visual language rather than a generic modern dashboard.

The repository currently contains only `AGENTS.md` and empty `doc/study/`,
`doc/plan/`, and `doc/wiki/` directories. The Django application, tests,
static assets, templates, and dependency files all need to be created.

## Feasibility

The project is well suited to a conventional Django monolith:

- Django's built-in authentication can handle registration, login, logout, password hashing, sessions, and staff permissions.
- SQLite is sufficient for a campus cafe prototype and keeps local setup simple.
- Django models and migrations provide durable menu, cart, order, and order-line data.
- Django templates, forms, static files, and standard views satisfy the requirement to keep the UI server-rendered.
- A custom staff area can use `is_staff` plus login protection; Django admin may remain available for operational fallback, but the primary staff workflow should be purpose-built and styled consistently.
- CSS and local/static image handling can deliver the retro aesthetic without introducing a frontend framework.

No external payment gateway is required by the request. Checkout can therefore
create an order from the current cart without collecting payment details. This
keeps the first implementation focused on ordering and fulfillment status.

## Proposed Application Shape

```text
project root/
├── manage.py
├── requirements.txt
├── .gitignore
├── cafe_site/              # Django project configuration and URL root
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── cafe/                   # Main domain application
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── tests/
├── templates/
│   ├── base.html
│   ├── registration/
│   ├── cafe/
│   └── staff/
├── static/
│   ├── css/
│   └── images/
├── media/                  # Local development uploads, ignored by git
├── db.sqlite3              # Local database, ignored by git
└── doc/
    ├── study/
    ├── plan/
    └── wiki/
```

The exact app names can be adjusted during planning, but the implementation
should keep the domain model and customer/staff workflows in one focused app
unless the plan identifies a concrete reason to split them.

## Domain Model Direction

### Menu item

`MenuItem` should include a name, description, price, photo, availability flag,
timestamps, and an optional category or display ordering field. Customer menu
queries should filter or clearly annotate unavailable items. Staff should be
able to edit all operational fields and toggle availability without deleting
historical references.

### Cart

A cart can be session-backed for a low-friction first version. This avoids
creating abandoned cart records and supports anonymous browsing while requiring
authentication only when the customer checks out. Cart quantities should be
validated against positive integers and unavailable items should not be added
or checked out.

### Order and order line

`Order` should belong to a customer and store a status constrained to the
four-step pipeline: `placed`, `preparing`, `ready`, and `completed`. It should
also store creation and update timestamps and a stable order identifier for the
customer and staff views.

`OrderItem`/`OrderLine` should reference the menu item when possible, copy the
item name and unit price at checkout, and store quantity. Copying these values
preserves the historical receipt if a staff member later edits or removes a
menu item. Order totals should be calculated from persisted line snapshots,
preferably with a database decimal field for money.

## URL and Permission Direction

The public/customer surface will likely need routes for:

- Menu listing and item details, if an item detail page is useful.
- Registration, login, and logout.
- Cart display, quantity updates, item removal, and checkout.
- Customer order history and an individual order detail/status view.

The staff surface will likely need routes for:

- Staff dashboard/incoming orders.
- Order status updates restricted to valid forward transitions.
- Menu item listing, creation, editing, deletion, and availability toggle.

Authentication and authorization should be enforced server-side, not only by
navigation. Staff routes should reject authenticated non-staff users, while
customer order queries must always be scoped to the logged-in customer.

## Visual and UX Direction

Use a shared base template with a warm paper/cream background, dark coffee-brown
text, muted brick or cranberry accents, and restrained decorative borders or
signage motifs. Serif or typewriter-inspired display typography should be used
for headings, with a highly readable body face. The design should feel like a
campus coffeehouse menu: tactile and nostalgic, but still responsive and clear
on small screens.

Important usability details include:

- Clear availability labels and disabled add-to-cart controls for unavailable items.
- Visible cart quantity and subtotal changes.
- A checkout confirmation that shows the order total and resulting order status.
- Status badges that distinguish each pipeline stage.
- Staff controls that make the next valid status action obvious.
- Accessible labels, focus states, sufficient contrast, and responsive layouts.

Photos should be optional at the model/form level so the app remains usable
without a configured upload service. The UI can provide an intentional
illustrated or patterned fallback rather than a broken image.

## Feasibility Risks and Tradeoffs

### Authentication and roles

Using Django's user model with `is_staff` is the smallest viable role model and
avoids a custom user migration. A dedicated profile or role field would be
more explicit but adds complexity and migration decisions without a stated
need for multiple staff role types.

### Cart persistence

A session cart is simple and supports guest browsing, but it is not shared
between devices and disappears when the session is cleared. A database cart
would support persistence but introduces cart cleanup and ownership behavior.
The session approach is appropriate unless cross-device cart persistence is a
requirement.

### Stock changes during checkout

Availability can change between adding an item and checkout. Checkout must
revalidate every line inside a transaction and fail safely if an item became
unavailable. Because this is a small SQLite application without inventory
counts, a boolean availability flag is enough for the requested behavior; exact
quantity inventory is out of scope.

### Order status integrity

Staff should not be able to skip or reverse stages accidentally. The server
should validate allowed transitions even if the UI only exposes a next-status
button. Whether staff need a correction mechanism for mistakes is an open
product question.

### Image storage

Local `MEDIA_ROOT` uploads are straightforward for development but are not a
production asset strategy. The initial project can configure local media and
document that production storage needs a deployment-specific backend.

### Payment and notifications

The requested feature set does not define payment processing, pickup timing,
email, or push notifications. Adding those now would expand security and
operational scope. The first version should stop at order placement and show
status in the authenticated order history.

## Testing Strategy Direction

The implementation should include Django tests covering at least:

- Registration and authentication flow.
- Customer/staff authorization boundaries.
- Menu visibility and availability behavior.
- Cart quantity, removal, and checkout validation.
- Order line price/name snapshots and total calculation.
- Customer ownership restrictions on order history/details.
- Valid and invalid order status transitions.
- Staff menu CRUD and availability changes.

Template smoke checks and a small set of view-level assertions should verify
that the main pages render. Static asset and responsive behavior should be
checked manually in a browser-sized viewport because they are not fully
captured by Django unit tests.

## Open Questions for Planning

1. The repository's current branch is `master`, but the required workflow says
   to create the implementation branch off `main`. Should `master` be renamed
   to `main` before execution, or should a new local `main` branch be created
   at the current scaffold commit?
2. Should unavailable menu items be hidden from customers or shown with a clear
   unavailable label? Showing them preserves menu context and better supports
   the stated "hidden or shown as unavailable" requirement.
3. Should registration create ordinary customers only, with staff accounts
   created through Django admin or a management command?
4. Is a local image upload field sufficient for this first version, or should
   menu photos be represented by externally hosted URLs?
5. Should staff be allowed to move an order backward or reset it, or only make
   forward transitions through the four stated statuses?
6. Is checkout intentionally payment-free, with the order treated as a cafe
   pickup request rather than a paid transaction?

## Recommendation

Proceed with a single Django project and one domain app, Django's built-in user
model plus `is_staff`, a session-backed cart, SQLite, local media uploads, and
strict forward-only status transitions. Show unavailable items on the customer
menu with an explicit label unless product direction says otherwise. Resolve
the branch naming question before the plan execution stage, then define the
implementation checklist in `doc/plan/`.
