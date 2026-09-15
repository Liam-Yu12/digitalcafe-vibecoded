# Wildcard CodeRange CSRF Trust Fix Study

## Problem

Django now accepts the forwarded CodeRange hostname through `ALLOWED_HOSTS`,
but unsafe requests from the HTTPS forwarded URL are rejected by CSRF origin
validation. The error identifies
`https://itent-45-1t-2526-p27-8000.coderange.net` as an untrusted origin.

## Feasibility

Django's `CSRF_TRUSTED_ORIGINS` setting accepts scheme-inclusive origins. A
leading wildcard subdomain entry, `https://*.coderange.net`, matches HTTPS
CodeRange subdomains, including hostnames that encode forwarded ports. This
should be added alongside local HTTPS development support only if needed; the
reported forwarded URL specifically requires the wildcard HTTPS entry.

## Tradeoffs

- The setting must include `https://`; unlike `ALLOWED_HOSTS`, a bare domain is
  not valid for CSRF trusted origins.
- `https://*.coderange.net` trusts cross-origin unsafe requests from any
  CodeRange HTTPS subdomain. This is appropriate for the development workspace
  forwarding model but should not be copied into production without reviewing
  the deployment trust boundary.
- The change complements, rather than replaces, the existing `.coderange.net`
  host allowlist.

## Planned Verification

After approval and implementation:

- Run `manage.py check` and the existing tests.
- Inspect Django's parsed CSRF trusted origins to confirm the wildcard is
  recognized.
- Exercise a CSRF-protected POST with an HTTPS CodeRange `Origin` header and
  confirm it is not rejected for origin mismatch.
- Update the wiki's development security settings documentation.
- Commit with a `fix:` Conventional Commit message and merge to `main` after
  verification.
