# Implementation plan

## 1. Delivery model

Implement in vertical slices, one verified desktop capability at a time. The milestone gates below define completion. Track test evidence independently of the presence of a deployable payload. Every milestone requires an evidence entry in `benchmarks/` or a local ignored validation record. Do not deploy all templates in one operation.

| Milestone | Deliverable | Gate |
|---|---|---|
| M0 | Scaffold, manifests, planning and portable tests | Static checks pass |
| M1 | Native CachyOS baseline and recovery | V-01, V-02, V-30 baseline recovery |
| M2 | MangoWM manual TTY session and service ownership | V-03–V-06, V-14–V-19 |
| M3 | Lock, idle, clipboard, screenshot and portal integration | V-08–V-13 |
| M4 | Dynamic theme pipeline and consistent UI | V-07, V-35 |
| M5 | Daily applications and media | V-20–V-25; V-34 if opted in |
| M6 | Gaming and performance | V-26–V-28, V-31–V-33 |
| M7 | Reviewed deployment, rollback and release | V-29, V-30 post-deployment recovery and all MUST gates |

## 2. M1: inspect and establish baseline

1. Install CachyOS No Desktop using the supported installer. Choose filesystem, bootloader and encryption independently; this repository will not repartition or alter boot entries.
2. Run `./scripts/dotctl baseline` before and after desktop installation and retain dated output under ignored `benchmarks/local/`. Confirm CPU repository tier (Zen 3 / v3), AMD driver, firmware, microcode, Vulkan and video decode. Record current kernel and Mesa, firmware, package versions and monitor modes. Preserve native settings and enabled services.
3. Establish a recovery path: authenticated TTY, bootable recovery media, external backup and, if applicable, a tested Btrfs snapshot/bootloader workflow. Test fallback kernel if selected.
4. Run `./scripts/dotctl doctor --profile gaming` and inspect the native audit list. Missing packages are resolved against current local metadata. Do not turn missing official packages into automatic AUR builds.
5. Perform an approved full update and repository package installation as one transaction. Check transaction contents, package conflicts and keyring status. Capture baseline before and after desktop installation.

## 3. M2: create the graphical session

- Start MangoWM manually as the normal user from an authenticated TTY. Copy the installed `/etc/mango/config.conf` to a working user file only after inspecting it; do not treat development-branch examples as installed grammar. Start with a terminal and exit binding. Verify `mango -c <path> -p` if the installed version supports validation.
- Implement a single session owner. Evaluate UWSM using the shipped Wayland desktop entry and actual desktop identifier. Verify environment and start/stop behavior. If unsuccessful, use a custom target with explicit wrapper cleanup. Never start both paths. Document decision D-02.
- Add session services in this order: Waybar, SwayNC, wallpaper, SwayOSD, polkit, Udiskie. Check packaged autostart entries before creating custom units; do not duplicate services. Verify two complete login/logout cycles and configuration reloads.
- Configure Waybar with installed Mango modules; use an event subscription for SwayNC indicator, native audio/tray/network modules, and a low-frequency clock. Start with no live CPU/GPU graphs. Rofi uses native Wayland if supported, `drun` for applications, dmenu modes for explicit script data.
- Install portals with distro defaults. Compare upstream-provided Mango configuration and only override if necessary. Validate file chooser and screen capture. Do not globally bypass output selection.
- Only after manual launch is stable, consider a login-shell hook restricted to tty1, no existing display, no SSH and an explicit user opt-out. Validate logout behavior and recovery tty. Keep Bash/system scripts separate from Fish.

## 4. M3: safety and desktop utility integration

**Authentication:** inspect installed PAM stack and agent executable. Review a minimal diff, backup and test on a separate authenticated TTY before accepting any PAM changes. Ensure GNOME Keyring has one Secret Service owner. No passwordless power actions.

**Lock/idle:** configure `swayidle -w` with `swaylock -f` on lock and before-sleep, using installed manuals. Start with a 10-minute lock timeout. Add output blanking only after checking Mango protocols/commands; no Sway IPC commands. Test multi-output, suspend, failed locker, controller-only games and video idle inhibition. A secure lock is release-blocking.

**Clipboard:** test text and image copy without history first. Implement an explicit opt-in watcher lifecycle and private history. Test synthetic KeePassXC secrets before enabling history; filtering based on MIME hints is not a universal security guarantee. If unsafe, keep watchers disabled. Add persistence only after the same test. Never log contents.

**Capture:** region/fullscreen capture with Grim/Slurp; handle cancelled selection without empty files, quote paths, use private temporary storage and clean it. Launch Satty on demand. Set capture outputs explicitly; no automatic upload.

**Menus:** use Rofi for clipboard, wallpaper, power and app menus. Route choices through fixed actions or validated file IDs; do not interpret selected text as shell commands. Confirm power actions; rely on logind/polkit. Do not terminate an unrelated user session.

## 5. M4: dynamic theming pipeline

Use static wallpaper images rendered by Awww; transitions only on selection, not continuous animation. Matugen runs once per wallpaper change; use its installed version's template grammar. Design system: Material-inspired dark mode, Inter UI, JetBrains Mono Nerd Font terminal, Papirus icons, Bibata cursor (all candidates); 4/8/12/16 px spacing, approximately 8–12 px corners, modest animations, opaque default surfaces, no blur. Keep text contrast and stable semantic colors.

### Theme transaction (future `dotctl theme apply`)

1. Resolve selected wallpaper as a readable regular file in the user-approved library; reject symlink escapes if library restriction applies. Serialize concurrent requests with a private runtime lock.
2. Generate palette and templates into a unique staging directory, never tracked files. Verify required roles, contrast, file syntax, and application version compatibility. Abort with current wallpaper and theme unchanged if preparation fails.
3. Commit a revision by atomic rename or pointer switch within the same filesystem; retain previous revision. Set wallpaper via verified Awww client command. If this fails, revert the theme pointer and report the error. Treat wallpaper plus multiple app reloads as a best-effort transaction, not truly atomic across processes.
4. Reload each supported application individually using its documented interface. Never restart compositor or editors automatically. For unsupported reloads, mark next-launch pending. If a critical reload fails, preserve/restore the previous revision and report partial status.
5. Record wallpaper reference, palette revision, template version and outcome (no private path in public logs). Restore last valid theme on login; use static fallback if missing. Do not start a continuous watcher or generator.

| Adapter | Destination concept | Reload strategy (verify installed release) |
|---|---|---|
| MangoWM | included colors file | validated config reload only |
| Waybar | imported CSS | documented reload signal or controlled service restart |
| Rofi | imported Rasi | next launch |
| SwayNC | CSS | documented client style reload |
| Swaylock | color/image config | next lock; never restart active locker |
| SwayOSD | GTK CSS | next service restart if no supported reload |
| Kitty | palette include | documented reload, no unrestricted remote control |
| Neovim / Zed | palette / custom theme | next launch or explicit user command |
| Yazi / RMPC / Btop | theme files | next launch unless documented reload |
| Zathura / Swayimg / MPV | colors/options | next launch |
| GTK / Qt | supported toolkit settings | conservative fallback; do not force unsupported libadwaita CSS |

The canonical role list and static fallback are in `themes/`. No actual Matugen templates are claimed complete until app/version syntax is validated.

## 6. M5: daily application integration

- Kitty: test image previews with Yazi and album art with RMPC. Use a single instance only when beneficial and verify window lifecycle. Fish: inspect `cachyos-fish-config` and avoid duplicate prompt/greeting. Starship only interactive. Bash stays available for automation.
- Yazi: enable only needed preview dependencies. Thunar owns GUI directory MIME and drag-and-drop. Configure GVfs/Tumbler as needed; no duplicate automounter. Set MIME defaults explicitly, not by overwriting all existing associations.
- Neovim: small plugin set, version/lockfile policy, lazy/filetype loading, native LSP; Zed stable repository build, verify Vulkan and Secret Service. Avoid two LSP/indexing sessions for the same project. Notes remain Markdown; do not impose a vault format.
- Firefox: supported browser, native Wayland where available, hardware decode verified in about:support. No sandbox disabling or aggressive global flags. KeePassXC browser integration optional; keyring stays separate.
- MPD: user service, local socket or loopback, PipeWire-compatible output, library path selected by user. RMPC uses same endpoint. Start exactly one MPRIS bridge, verify playerctl and Waybar/SwayNC. UOSC: reviewed tagged release/packaged source and checksum or provenance record, no script pipe; mpv built-in OSC remains fallback until plugin installed.
- Zathura: install one PDF backend; test PDFs, links and search. Swayimg: use supported native protocol and MIME defaults. Btop and amdgpu_top remain on demand.
- Bluetooth: enable only if hardware exists; test headphones, mic and controller. Yapfast: explicit opt-in and trust review; never automate token extraction; use official web fallback.

## 7. M6: gaming and measurement

Inspect `cachyos-gaming-meta` dependencies, retain installed Mesa/RADV 32-bit drivers, install Steam with normal Pacman priority. Keep Valve's Proton default; test SLR only per game. If metadata names change, update manifests with evidence. Exercise Steam, the development editor and MPD in the same session. Verify that entering and leaving a game preserves the open project and music playback. Use GPU Screen Recorder for local recordings and leave OBS Studio optional for streaming. Validate native and Proton titles; no promise of anti-cheat compatibility.

Test fullscreen, mouse confinement, VRR if supported, input and screen capture. MangoHud only per game; Gamescope only for demonstrated compatibility need. GPU Screen Recorder on demand, replay off by default. Verify actual encoder and permissions. Do not stack GameMode on Ananicy-CPP; optional game-performance wrapper only after verifying current policy.

Daily/gaming profiles are optional workload policies, not kernel tuning. The initial runtime mode is a manual SwayNC DND toggle on Super+Shift+C. Never automatically stop databases/containers with active clients, close browsers, terminate music without consent or modify system services. If future profile manager changes owned optional services, record prior state, serialize transitions, restore only changes it made, and handle nested launches/abnormal exits. Test the DND toggle with an editor and MPD active.

## 8. M7: deployment and rollback contract

The planner is deliberately non-mutating. User-file deployment is handled by `dotctl deploy`. Its implementation and release checks follow this contract:

1. **Preflight:** non-root user, CachyOS, local package resolution, explicit profile, XDG paths, free space, backup location, existing config conflicts, current session and recovery access. Use normal repository priority. Never alter repository lists or refresh without full update.
2. **Plan:** show package transaction, exact file mappings, service changes and manual root steps. Exclude `.example`, local state and unreviewed configs. Require explicit apply; no implicit sudo. Record chosen profile and versions.
3. **Backup:** copy only affected user files with permissions/symlinks preserved into a private timestamped directory. Record prior existence/type/hash or symlink target and service enablement. Do not back up secrets to public Git. Treat PAM/system changes as a separate manual operation with recovery plan.
4. **Deploy:** explicit allowlisted mappings or GNU Stow packages organized by target XDG tree. Stow requires conflict checks; never use `--adopt` without review. Validate staged configuration, commit individual files atomically where practical, do not replace unmanaged files by default. Generated theme files stay outside tracked symlink sources.
5. **Activate:** reload user systemd manager only if needed; start only selected session owner; verify no duplicate autostart. Root actions separate, reviewed and documented. No automatic logout/reboot.
6. **Rollback:** stop only newly introduced units; restore affected paths only if current hashes still match deployed content (otherwise report conflict). Restore prior enablement and configuration; leave packages installed by default. Package rollback requires coherent system snapshot or supported recovery, not partial downgrades. Never recursively delete home configuration. Test twice including interrupted deployment.

## 9. Proposed interaction map

| Binding | Action |
|---|---|
| Super+Return / Super+Space | Kitty / Rofi drun |
| Super+E / Super+Shift+E | Yazi / Thunar |
| Super+B / Super+N | Firefox / Neovim |
| Super+M / Super+V | RMPC / history picker (after opt-in) |
| Super+C / Super+Escape | notification drawer / lock |
| Super+Shift+Escape | power menu with confirmation |
| Print / Shift+Print | region / fullscreen capture |
| Super+1…9 | Mango tags; Shift moves window |
| Media keys | SwayOSD / playerctl |

These are proposed; confirm compositor syntax, conflicts, keyboard layout and accessible alternatives before finalizing.
