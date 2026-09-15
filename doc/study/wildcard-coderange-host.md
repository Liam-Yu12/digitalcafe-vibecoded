# Wildcard CodeRange Host Fix Study

## Problem

CodeRange may expose the development server through different hostnames for
different forwarded ports. The current settings allow one exact hostname,
`itent-45-1t-2526-p27.coderange.net`, but a forwarded request using
`itent-45-1t-2526-p27-8000.coderange.net` is rejected by Django with
`DisallowedHost`.

## Feasibility

Django supports a leading-dot entry in `ALLOWED_HOSTS` to match the domain and
its subdomains. Replacing the single workspace hostname with `.coderange.net`
will allow CodeRange workspace and forwarded-port subdomains without adding a
new settings entry for every port. Local hosts should remain explicitly listed
for direct development access.

## Security Tradeoff

`.coderange.net` is narrower than `*`, but it trusts any subdomain under the
CodeRange parent domain. That is appropriate for this workspace's forwarded
development URLs and is not a production deployment setting. Production should
use an environment-specific allowlist and avoid accepting a broad workspace
domain unless its trust boundary is understood.

## Planned Verification

After approval and implementation:

- Run Django system checks and the existing tests.
- Request `/menu/` using both the existing hostname and the `-8000` hostname in
  the `Host` header while the server listens on `0.0.0.0:8000`.
- Confirm both requests return successfully instead of `DisallowedHost`.
- Update the wiki's host configuration description.
- Commit the change with a `fix:` Conventional Commit message and merge it to
  `main` after verification.
