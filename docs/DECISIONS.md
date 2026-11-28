# Architecture decision log

Status: accepted design decisions are not runtime certification. Update with date, rationale, evidence, alternatives and affected test IDs when revising.

| ID | Status | Decision and rationale | Review trigger |
|---|---|---|---|
| D-01 | Accepted | MangoWM stable repository release; Waybar/Rofi/SwayNC modular stack; no all-in-one shell. | Regression, protocol limitation or package removal |
| D-02 | Open | TTY retained. The trial payload uses the packaged UWSM Mango desktop entry. No auto-start until V-03/04. | Host integration evidence |
| D-03 | Accepted | Rofi desktop launcher; Steam gaming only. Corrects duplicate launcher choice. | Changed workflow |
| D-04 | Accepted | Awww + Matugen on-demand generation; static fallback; no live wallpaper. | Measured overhead or unsupported reload |
| D-05 | Accepted | Swaylock/Swayidle stable; no effects fork. | Lock/inhibitor failure |
| D-06 | Accepted | mate-polkit instead of xfce-polkit; GTK and repository packaging. | Agent incompatibility or source availability |
| D-07 | Gated | GNOME Keyring via existing/reviewed PAM; KeePassXC independent. | V-17 or PAM review |
| D-08 | Gated | Cliphist installed, history off by default until privacy validation; persistence optional. | V-11 |
| D-09 | Accepted | WLR + GTK portal; prefer shipped config; verify Secret/Inhibit interface. | Portal incompatibility |
| D-10 | Accepted | Valve Proton default; SLR per game; no global Gamescope. | Game-specific results or CachyOS policy change |
| D-11 | Accepted | Preserve native tuning; no GameMode with active Ananicy. | Measured approved change |
| D-12 | Accepted | Yapfast opt-in only; no automated token handling. | User consent and provenance review |
| D-13 | Open | Btrfs/Snapper and fallback kernel only if suitable for actual install. | Filesystem/boot decision |
| D-14 | Accepted | Keep the package planner read-only. Use explicit apply and rollback for user configuration. | M7 completion |
| D-15 | Open | Final font/icon/cursor choices, display capabilities, palette reload coverage. | User selection and V-35 |
| D-16 | Accepted | One MPRIS bridge; Thunar GUI MIME fallback and Udiskie automounter. | Integration failure |

## Unresolved information

Actual installed package versions, available refresh modes and VRR support, bootloader/filesystem, PAM layout, Xbox One controller connection type, chosen game test set, actual memory footprint, session integration and application config grammar. Do not infer these from project name or sample configuration.
