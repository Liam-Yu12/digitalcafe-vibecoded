# Wildcard CodeRange Host Fix Plan

- [ ] Create a dedicated fix branch from the current `main` branch.
- [ ] Replace the exact CodeRange hostname in `cafe_site/settings.py` with
  Django's `.coderange.net` suffix entry while retaining local hosts.
- [ ] Update `doc/wiki/README.md` to describe the wildcard CodeRange host
  behavior and its development-only security boundary.
- [ ] Run `manage.py check` and the complete `cafe` test suite.
- [ ] Start the development server on `0.0.0.0:8000` and verify requests with
  both CodeRange host variants, including the `-8000` hostname.
- [ ] Commit the implementation with a `fix:` Conventional Commit message.
- [ ] Merge the fix branch into `main` with `--no-ff` and confirm a clean tree.
