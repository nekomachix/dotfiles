# Theme contract

`fallback.json` defines the portable role names (background, surface, surface_raised, foreground, muted, accent, on_accent, border, error, warning, success). Matugen adapters map version-specific Material roles to these names; semantic warning/error/success colors must remain distinguishable. Validate text contrast and selection pairs. Static fallback is original and can be used offline. Store generated revisions under a private XDG directory outside the repository. See Implementation M4 for staging, reload, partial failure and rollback policy.
