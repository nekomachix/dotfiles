# User service sketches

Examples only. Do not enable or copy them blindly. Select one session owner first, verify `graphical-session.target` lifecycle and packaged XDG autostart ownership. Attach units to session target only after confirming dependencies and environment. No `WantedBy=default.target` for graphical utilities. `systemctl --user daemon-reload` and verify only after reviewed deployment. The clipboard watcher is intentionally not supplied; privacy gate must be implemented first.
