# Forwarded URL `ALLOWED_HOSTS` Fix Study

## Problem

The development server is reachable through the CodeRange forwarded hostname
`itent-45-1t-2526-p27.coderange.net`, but Django currently has an empty
`ALLOWED_HOSTS` setting. Django therefore rejects requests using the forwarded
host with `DisallowedHost` before the application can serve a response.

## Feasibility

This is a small, low-risk settings change. Adding the exact forwarded hostname
to `ALLOWED_HOSTS` will allow Django's host validation to accept requests from
the CodeRange URL while leaving unrelated hosts rejected. The existing local
development hosts should remain usable as well, including `localhost` and
`127.0.0.1`.

## Tradeoffs

- An exact hostname is safer than allowing every host with `*`.
- The CodeRange hostname is environment-specific and may need to be updated if
  the workspace or forwarded URL changes.
- This remains development configuration; production should supply hosts via an
  environment variable or deployment-specific settings rather than hard-code
  a workspace hostname.

## Planned Verification

After approval and implementation:

- Run `manage.py check`.
- Start the server on `0.0.0.0:8000`.
- Request the app with the forwarded hostname in the `Host` header and confirm
  it no longer returns `400 DisallowedHost`.
- Run the Django test suite.
- Confirm the fix is committed with a `fix:` Conventional Commit message.
