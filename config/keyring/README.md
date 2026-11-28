# keyring

**Status:** design / not deployed.

**Target:** `PAM and application-owned keyring state`

Review /etc/pam.d/login; no keyring files in repo; one Secret Service owner.

**Acceptance:** V-17 in [Validation](../../docs/VALIDATION.md). Check installed release and actual config paths before promoting any example. No credentials or generated runtime state in this directory.
