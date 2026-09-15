# Forwarded URL `ALLOWED_HOSTS` Fix Plan

- [ ] Create a fix branch from the current `main` branch.
- [ ] Update `cafe_site/settings.py` to allow local development hosts and the
  exact CodeRange forwarded hostname `itent-45-1t-2526-p27.coderange.net`.
- [ ] Run Django system checks and the existing test suite.
- [ ] Start the development server on `0.0.0.0:8000` and request the app with
  the forwarded hostname to verify Django no longer returns `DisallowedHost`.
- [ ] Review the diff and commit the settings change with a Conventional Commit
  message beginning with `fix:`.
- [ ] Merge the fix branch back into `main` after verification and confirm the
  working tree is clean.
- [ ] Update `doc/wiki/` if the development host configuration documentation
  needs to reflect the exact current behavior.
