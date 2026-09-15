# Wildcard CodeRange CSRF Fix Plan

- [ ] Create a dedicated fix branch from the current `main` branch.
- [ ] Add the scheme-inclusive `https://*.coderange.net` entry to
  `CSRF_TRUSTED_ORIGINS` in `cafe_site/settings.py`.
- [ ] Update `doc/wiki/README.md` to document the development CSRF trusted
  origin configuration and its workspace-only security boundary.
- [ ] Run `manage.py check` and the complete `cafe` test suite.
- [ ] Verify Django recognizes the wildcard trusted origin and exercise a
  CSRF-protected POST with a matching HTTPS CodeRange origin.
- [ ] Commit the implementation with a `fix:` Conventional Commit message.
- [ ] Merge the fix branch into `main` with `--no-ff` and confirm a clean tree.
