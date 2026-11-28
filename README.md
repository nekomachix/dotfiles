# komachix/dotfiles

A modular, wallpaper-themed, gaming-conscious Wayland desktop for CachyOS No Desktop.

**Status:** Desktop integration in progress. The checkout includes the Mango session payload, package planner, baseline probe, and user-file deployment and rollback commands. Follow the disposable rollout and track physical release gates in the validation plan.

## Purpose

Build a comfortable daily desktop with independently replaceable components, without an all-in-one shell or graphical greeter. Spend the resource budget on applications and games, not constant effects or unnecessary background work. Keep the distribution's own kernel, hardware detection, update policy and performance tuning intact.

Target: Ryzen 5 5600 (Zen 3), Radeon RX 9060 XT 8 GB, 16 GB DDR4-3200, 1 TB Gen4 NVMe. The target session uses one 1920×1080 monitor at 300 Hz and an Xbox One controller for Steam games. Development and local music share this session.

## Selected stack

| Layer | Selection |
|---|---|
| Platform | CachyOS No Desktop, systemd, AMDGPU/Mesa/RADV |
| Session | TTY/getty + PAM; MangoWM; UWSM trial integration |
| Desktop | Waybar, Rofi, SwayNC, Awww, Matugen, Swaylock, Swayidle, SwayOSD |
| Clipboard / capture | wl-clipboard, Cliphist + Rofi, optional wl-clip-persist; Grim + Slurp + Satty |
| Daily | Kitty, Fish, Starship, Yazi + Thunar, Neovim + Zed, Firefox, KeePassXC |
| Media | MPD + RMPC + mpd-mpris, MPV + UOSC, Swayimg, Zathura + MuPDF |
| Infrastructure | NetworkManager, PipeWire + WirePlumber, mate-polkit, GNOME Keyring, UDisks2 + Udiskie, BlueZ + Blueman |
| Gaming | Steam, Valve Proton default, Proton-CachyOS SLR per game, MangoHud, GPU Screen Recorder, amdgpu_top |
| Optional | Yapfast (experimental, explicit opt-in), Gamescope, night light, additional developer tools |

## Start here

Extract the archive, open a terminal in this directory and run:

```sh
./install.sh --profile daily
./install.sh --profile gaming
./scripts/dotctl validate
./scripts/dotctl baseline
./scripts/dotctl doctor --profile gaming
python3 -m unittest discover -s tests -v
```

`install.sh` is a **planner**, not an installer: it prints a candidate full-upgrade command and does not run it. `doctor` queries local package metadata and reports missing commands; it does not refresh package databases, install packages, or change services. It returns nonzero if required packages cannot be resolved. On non-CachyOS systems it reports that host checks are unavailable or inappropriate. Python 3 is required for tooling.

`dotctl baseline` prints M1 observations to standard output. Exit 0 means the report completed, including any individually blocked probes. Exit 2 identifies an unsupported host. Keep dated reports under the ignored `benchmarks/local/` directory. Confirm recovery by testing the TTY, recovery media and a backup restore.

On CachyOS, inspect package groups and doctor results before manually running a reviewed `sudo pacman -Syu --needed ...` transaction. Do not run an isolated `pacman -Sy`. Never run the scaffold itself as root. AUR and upstream artifacts are explicitly excluded from the planner. See [Deploy and recover](bootstrap/README.md) for disposable user deployment.

## Documentation map

| Document | Purpose |
|---|---|
| [Requirements](docs/REQUIREMENTS.md) | Scope, constraints, acceptance requirements and component decisions |
| [Infrastructure](docs/INFRASTRUCTURES.md) | Platform, services, session, portals, security and dependency ownership |
| [Implementation plan](docs/IMPLEMENTATION.md) | Milestones, configuration, theming, deployment and rollback |
| [Validation plan](docs/VALIDATION.md) | Test cases, evidence and performance methodology |
| [Decisions](docs/DECISIONS.md) | Accepted decisions and open gates |
| [Sources](docs/REFERENCES.md) | Upstream references and verification policy |
| [AGENT.md](AGENT.md) | Contributor/automation operating rules |

## Repository layout

```text
.
├── AGENT.md / AGENTS.md       # Human and agent operating contract
├── README.md
├── docs/                     # Architecture, requirements and plans
├── packages/                 # Repository manifests and native audit list
├── profiles/                 # Composable package selections
├── config/                   # Per-component design notes and examples
├── system/                   # Review-only system configuration notes
├── systemd/user/              # Review-only unit examples
├── scripts/                  # Read-only dotctl planner and diagnostics
├── bootstrap/                # Deployment and recovery procedure
├── desktop/                  # Explicitly mapped user configuration payload
├── themes/                   # Palette contract, fallback and templates
├── assets/wallpapers/         # User-provided assets only
├── benchmarks/               # Evidence schema and collection instructions
├── tests/                    # Portable structural/tooling tests
└── .github/workflows/        # CI for scaffold checks
```

The `config/` directory contains design notes and review examples. Deployment maps files from `desktop/` to explicit XDG paths and records ownership for rollback.

## Contribution workflow

Read AGENT.md, choose an implementation milestone, add or update the associated requirement/test IDs, implement in small reviewable changes, run portable checks, then collect host evidence. Never describe a host test as passed without its evidence. Keep credentials, generated themes, wallpapers without redistribution rights and local hardware state out of Git.

No external code or wallpaper is vendored. License selection is left to the repository owner; upstream components retain their own licenses.
