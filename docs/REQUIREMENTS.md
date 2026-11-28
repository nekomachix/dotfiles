# Requirements specification

**Baseline:** v0.1.0 design; all host acceptance criteria pending. IDs are stable. MUST = release requirement, SHOULD = preferred unless a decision records an exception, MAY = optional.

## 1. Context and scope

The desktop is a personal daily driver for software development, media and gaming on the specified Zen 3 / RDNA 4 system. Resource efficiency includes working-set memory, GPU memory, CPU wakeups, responsiveness and frame-time consistency. Package count is not a runtime metric. The objective is not to guarantee higher FPS or to imitate another desktop environment.

In scope: package selection, XDG configuration, login/session integration, themes, keyboard/mouse workflows, application defaults, user service orchestration, recovery, diagnostics and gaming profiles. Out of scope: building a distribution, replacing CachyOS package management, bootloader/partition automation, automatic driver changes, overclocking, automatic account login, unofficial client credential handling, and mandatory cloud services.

## 2. Functional requirements

| ID | Level | Requirement | Acceptance |
|---|---|---|---|
| R-01 | MUST | Preserve CachyOS No Desktop base, stable repository packages, full upgrades and native tuning | V-01, V-02 |
| R-02 | MUST | Authenticate via getty/PAM; launch MangoWM only from an intended TTY; clean shutdown | V-03, V-04 |
| R-03 | MUST | Provide workspace navigation, floating/fullscreen, bar, app launcher, tray and power menu | V-05 |
| R-04 | MUST | Notifications, history, DND, audio OSD and accessible settings | V-06 |
| R-05 | MUST | Static wallpaper with optional transitions; wallpaper-derived palette, fallback and safe reload | V-07 |
| R-06 | MUST | Lock reliably, including before suspend; respect supported inhibitors | V-08, V-09 |
| R-07 | MUST | Copy/paste text/images; history only with privacy controls and explicit activation | V-10, V-11 |
| R-08 | MUST | Region/fullscreen screenshot and annotation; correct portal routing | V-12, V-13 |
| R-09 | MUST | Reliable networking, audio, authentication, credentials, mounts and XWayland | V-14 through V-19 |
| R-10 | SHOULD | Bluetooth pairing and routing when hardware is present | V-20 |
| R-11 | MUST | Daily apps support image preview, development, browser, documents and media without duplication | V-21 through V-25 |
| R-12 | MUST | Use Steam as the sole default game platform, with native titles, Steam’s default Proton and per-title Proton-CachyOS SLR; VRR where supported, input and fullscreen stability | V-26, V-27 |
| R-13 | SHOULD | Hardware decoding and on-demand native recording with GPU Screen Recorder. OBS Studio is optional for streaming | V-24, V-28 |
| R-14 | MUST | Reproducible staged deployment, backups and rollback, no destructive defaults | V-29, V-30 |
| R-15 | SHOULD | Daily/gaming profiles reduce only explicitly owned optional workloads | V-31 |
| R-16 | MUST | Collect comparable performance data before claiming improvements | V-32, V-33 |
| R-17 | MAY | Yapfast, explicitly opted in after trust/account risk review | V-34 |
| R-18 | MUST | Consistent readable colors, typography, spacing and icons, without unsupported global overrides | V-07, V-35 |

## 3. Component baseline and rationale

| Domain | Component | Status / rationale |
|---|---|---|
| Compositor | MangoWM | Selected; stable packaged version, protocol and gaming gates required |
| Bar | Waybar | Selected; native Mango modules where installed version supports them |
| Launcher and menus | Rofi | Selected; native Wayland backend; Steam is game launcher only |
| Notifications | SwayNC | Selected; history and quick actions justify a session daemon |
| Wallpaper / theme | Awww + Matugen | Selected; daemon plus one-shot generator, no animated video wallpaper |
| Lock / idle | Swaylock + Swayidle | Selected; security over cosmetic forks |
| Session | TTY; UWSM candidate | TTY login required; session manager decision gated |
| OSD | SwayOSD | Selected; no optional input backend unless required |
| Clipboard | wl-clipboard + Cliphist + Rofi | Selected; history default off until gate; wl-clip-persist optional after test |
| Capture | Grim + Slurp + Satty | Selected; output and cancellation checks |
| Terminal | Kitty + Fish + Starship | Selected; image protocol, separate Bash scripting; avoid duplicate prompt |
| Files | Yazi + Thunar | Selected; CLI-first and GUI directory/MIME fallback |
| Editors / notes | Neovim + Zed; Markdown | Selected; avoid duplicate LSPs and indexers |
| Browser | Firefox | Selected; supported browser and hardware decode |
| Discord | Yapfast / official web fallback | Experimental; account and supply-chain risks |
| Music | MPD + RMPC + mpd-mpris | Selected; one media bridge, playerctl integration |
| Video / image | MPV + UOSC; Swayimg | Selected; UOSC external release managed separately |
| PDF | Zathura + MuPDF plugin | Selected; Poppler alternative, one backend |
| Monitoring | Btop + amdgpu_top | Selected; on-demand |
| Passwords | KeePassXC | Selected; Secret Service disabled in KeePassXC when GNOME Keyring owns it |
| Network / audio | NetworkManager, PipeWire/WirePlumber | Preserve existing system services; pavucontrol on demand |
| Auth / secrets | mate-polkit, GNOME Keyring | Revised from xfce-polkit for repository/GTK consistency; PAM gate |
| Removable / Bluetooth | UDisks2 + Udiskie, BlueZ + Blueman | Single automounter; Bluetooth opt-in |
| Gaming | Steam, Valve Proton, Proton-CachyOS SLR | Valve default; per-game overrides; optional Gamescope |
| Recording | GPU Screen Recorder + MangoHud | On demand; verify AMD encode and overlay |

## 4. Nonfunctional requirements

| ID | Target / constraint |
|---|---|
| N-01 | Whole-system idle memory target ≤ 800 MiB; investigate above 1 GiB, not automatic failure. Record MemAvailable and PSS separately. |
| N-02 | Sustained idle aggregate CPU target ≤ 1%; report normalized sampling method and wakeups. |
| N-03 | Idle VRAM target ≤ 300 MiB, conditional on display configuration; document actual monitor count/mode and driver accounting. |
| N-04 | No sustained swap churn at idle; do not equate nonzero ZRAM occupancy with active swapping. |
| N-05 | Gaming: no material regression relative to controlled baseline; suggested review threshold >3% median FPS or >5% p99 frame time degradation; account for run variance. |
| N-06 | No persistent polling below 1 s without measured need; prefer event subscriptions and longer intervals for optional metrics. |
| N-07 | Repeated installation produces no duplicate services or data loss; config changes reversible and validated. |
| N-08 | Core desktop usable offline after packages installed; no mandatory network theme generation. |
| N-09 | Text contrast target ≥4.5:1 for normal text; retain distinct error/warning colors, keyboard focus and readable auth prompts. |
| N-10 | No default application autostart for browser, editors, games, recording, Docker, database or sync tools. |

Targets are proposals, not measured guarantees. If a target is missed, inspect root cause and gaming impact before removing a useful feature.

## 5. Constraints and assumptions

- CachyOS installed with administrator access, supported current kernel and working AMD firmware. The target is one 1920×1080 monitor at 300 Hz and an Xbox One controller. Discover the connector, supported modes, VRR capability and controller transport on the host. Disk layout, bootloader, encryption and network topology remain installation-specific.
- Package names and repository locations are candidates until `pacman -Si` on the host. Stable releases may differ from upstream development documentation.
- One local graphical session initially. Multiple simultaneous sessions, remote desktops and multi-seat are not supported by v1.
- User chooses wallpaper library, fonts, Bluetooth hardware, editor plugins and optional apps. No assets bundled without redistribution permission.
- Application-wide palette reload support varies. Next-launch refresh is acceptable when live reload is unsupported.

## 6. Release exit criteria

All MUST requirements have passing evidence; security and recovery gates cannot be waived implicitly. Document any SHOULD exceptions and optional feature skips. Package update/rollback tests completed on the target; no untracked secrets. See [Validation](VALIDATION.md) for cases and evidence requirements.
