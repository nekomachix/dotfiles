# Validation plan

Track observed outcomes in the local evidence record. Portable tests exercise the CLI, configuration payload and user-file transactions in disposable XDG directories. Use a spare account/VM for configuration tests where possible, but physical hardware is required for GPU, input, lock and gaming claims.

## 1. Test procedure and evidence

Record test ID, date, tester, commit, package versions, kernel, display modes, preconditions, steps, observed output, result (PASS / FAIL / BLOCKED / SKIP), artifacts and remediation. Redact usernames, private paths, tokens, clipboard contents and network identifiers. SKIP requires reason and applies only to optional/unavailable hardware; BLOCKED is not PASS. Use `benchmarks/run-template.md` and `benchmarks/results-schema.csv` locally. Repeat failures with one changed variable.

## 2. Acceptance cases

| ID | Test | Procedure / pass condition |
|---|---|---|
| V-01 | Native base and packages | Inspect os-release, repo priority, package metadata and full upgrade plan; v3 appropriate, no unauthorized repository changes or partial upgrade. |
| V-02 | AMD stack | `lspci -k`, `vulkaninfo --summary`, `vainfo`, 32-bit game smoke test; AMDGPU/RADV present, correct GPU selected, no unexpected ICD. |
| V-03 | Authenticated TTY startup | Password login on tty1; manual then optional guarded auto-start; no autologin, SSH or other TTY launch. Check that exit and startup failure return to a login prompt. Recovery tty accessible with fresh authentication. |
| V-04 | Session lifetime | Two login/logout cycles, abrupt compositor exit and config reload; one compositor/agent/bar instance; graphical units stop, no stale sockets or duplicate autostart; inspect user journal. |
| V-05 | Compositor and bar | Open/close/move/tile/float/fullscreen, tags, active window, launcher and tray; output hotplug if available; no crash or polling workaround needed. |
| V-06 | Notifications and OSD | Send test notification, act/dismiss, history/DND, volume/mute media keys, pavucontrol; no duplicate OSD or notification owner. |
| V-07 | Wallpaper/theme | Select dark/light/busy wallpapers, change quickly, reboot, simulate invalid input/failed generation; last valid fallback retained, no editor/compositor termination; record reload behavior. |
| V-08 | Lock and suspend | Manual lock, timeout, `loginctl lock-session` for current session, suspend/resume, multiple outputs; no desktop frame/input exposed after resume; test locker failure behavior in a safe environment. Confirm an existing default swayidle config is ignored. |
| V-09 | Inhibitors and physical access | Video playback and controller-only gameplay past idle timeout; check expected inhibition, then lock after activity stops. Switch back to the launch TTY while locked, and verify that recovery requires a fresh login. |
| V-10 | Basic clipboard | Text and image transfer between native Wayland and XWayland; close source app, verify expected persistence policy. With history explicitly enabled, test picker cancellation and paste after the picker exits. |
| V-11 | Sensitive clipboard | Use synthetic secret in KeePassXC; inspect active clipboard/history after timeout, pause, clear and restart; ensure no secret retained or disable history. Never test with real credentials. |
| V-12 | Screenshot | Region/fullscreen captures, multi-output, cancel, paths with spaces, Satty annotation and paste after Satty exits. Check output, temporary files, and clipboard owner cleanup on logout. |
| V-13 | Portal | Inspect backend selection and logs; Firefox file picker, WebRTC monitor sharing with chooser, cancel, repeat; document window-share limitations and no unexpected capture. |
| V-14 | Network | Ethernet/Wi-Fi as applicable, reconnect after suspend, settings UI, DNS; preserve existing native config. |
| V-15 | Audio | Playback, microphone, route/default sink, volume feedback; PipeWire/WirePlumber active and no competing PulseAudio server. |
| V-16 | Polkit | Trigger benign authorized operation, cancel and authenticate; exactly one agent and no broad privilege bypass. |
| V-17 | Keyring | Test password login and synthetic app credential retrieval; GNOME Keyring owns Secret Service, KeePassXC independent; lock/unlock semantics documented. |
| V-18 | Mounts and MIME | Plug/unplug removable drive, mount once, eject safely, GUI Show in folder and default apps; no overlapping automounts. |
| V-19 | XWayland | Launch a legacy client and Steam, copy/paste, resize, mouse input; no forced global Wayland flags. |
| V-20 | Bluetooth | Pair/reconnect headset/controller where available; test audio and input; no duplicate applets. |
| V-21 | Terminal/file workflow | Kitty with Yazi previews (image/PDF/video where installed), Fish prompt once, Thunar drag/drop and MIME; no unnecessary daemon. |
| V-22 | Development | Open test project in Neovim and Zed, LSP/completion, file dialogs, synthetic credentials; Vulkan renderer works; inspect language server lifetime. |
| V-23 | Browser/passwords | Firefox Wayland/acceleration, downloads, extension and KeePassXC browser integration if selected; no sandbox weakening. |
| V-24 | Media | MPD local playback, RMPC album art, one MPRIS bridge, media keys; MPV/UOSC seeks and hardware decode observed; software fallback works. |
| V-25 | Documents/notes | Swayimg image, Zathura PDF search/links, Neovim Markdown; correct associations and no automatic background indexing. |
| V-26 | Steam/Proton | Native title and representative Proton titles; exercise Steam’s default Proton and a per-title Proton-CachyOS SLR override; no unverified global overrides. Record compatibility failures. |
| V-27 | Fullscreen and input | Game fullscreen, alt-tab, mouse capture, Xbox One controller input and reconnect over the user’s connection, VRR if supported, monitor power. Verify the active 1920×1080 at nominal 300 Hz before gameplay and after returning to the desktop; no unexpected idle locking or rendering errors. |
| V-28 | Recording | Record locally with GPU Screen Recorder using AMD hardware encoding, sound/mic, playback of captured file, permissions; no replay or recording process when disabled. |
| V-29 | Deployment | Dry-run, conflict detection, explicit apply on disposable user, run twice, interrupt mid-apply, simulate a concurrent write before a later destination is attempted, and verify rollback preserves unrelated files and secrets. Reject direct and symlinked paths into the checkout. |
| V-30 | Recovery/update | M1 baseline recovery requires an authenticated recovery TTY, a successful recovery-media boot and an external backup restore to a scratch destination. Record each outcome separately. M7 repeats recovery after a full upgrade and verifies known-good boot, deployed configuration restore, manual PAM recovery and any selected fallback kernel/snapshot. |
| V-31 | Profiles | Daily→gaming→daily, nested launches and abnormal exit if automated; only owned workloads change, an open development project and ongoing MPD playback survive entry and exit; no system tuning conflict. |
| V-32 | Idle performance | Compare TTY, minimal session and complete desktop under controlled conditions; report memory/PSS/VRAM/CPU/wakeups/swap and variance. |
| V-33 | Gaming performance | Controlled repeat runs, frame times and memory pressure; report median FPS, p99 frame time, 1% lows definition, variance; investigate regression thresholds. |
| V-34 | Experimental Discord | User opt-in, review provenance/account risks, synthetic/non-sensitive test where appropriate, voice and monitor share; official web fallback. |
| V-35 | Accessibility/consistency | Text contrast, visible focus, readable auth prompts, keyboard and mouse actions, GTK/Qt fallback; inspect multiple palettes and high-DPI modes if applicable. |

## 3. Portable checks (available now)

```sh
./scripts/dotctl validate
python3 -m unittest discover -s tests -v
bash -n install.sh
```

These check required files, manifest syntax, profile resolution, optional isolation, example-only status, palette shape/contrast and CLI behavior. CI uses Python standard library. It does not invoke Pacman or start a compositor. Host `doctor` is read-only and should be run separately; local metadata may be stale.

## 4. Idle benchmark design

Compare A: CachyOS authenticated TTY; B: MangoWM with essential services; C: full modular desktop. Optional D: Sway or Niri only if a meaningful comparison is needed. Keep package/kernel/Mesa versions, monitor count, resolution, refresh, VRR, wallpaper image, network, power policy, fan policy and service selection constant except the tested component. Warm up after boot; wait a fixed five minutes after login, then sample for at least 60 seconds. Repeat three times, ideally alternating test order. No browser, editor, Steam or media unless explicitly part of workload. Do not drop kernel caches or disable swap to artificially improve results.

| Metric | Method |
|---|---|
| System memory | `/proc/meminfo`: MemTotal−MemAvailable; record both and `free -h` output |
| Process memory | `smem` PSS for owned services, same permissions; do not sum RSS or confuse PSS with system usage |
| CPU | `pidstat -u 1 60`, aggregate normalized to logical CPU count; report sample mean and peaks |
| Wakeups | powertop if available, same collection settings; no auto-tune |
| GPU/VRAM | amdgpu_top or driver sysfs counters, identify correct GPU, report accounting and display modes |
| Swap | zramctl, `vmstat 1 60`, `/proc/pressure/memory`; compare sustained swap-in/out not occupancy alone |
| Startup | systemd-analyze and user journal timestamps; distinguish boot and session start |

Record tools/versions and missing permissions. Measurement tools themselves consume resources; collect comparably or in separate runs. Targets in requirements are investigative thresholds, not proof of success.

## 5. Gaming benchmark design

Pick repeatable built-in benchmark or identical saved route, fixed graphics/resolution/upscaling/FPS cap/VRR/Proton version. Use shader-cache warmup; report cold-cache separately. Keep ambient/thermal conditions and background apps comparable. Run at least three repetitions per variant, alternate order where possible. Collect MangoHud logs with documented logging configuration and compare same scene interval.

Report per-run FPS, median across runs, 1% low definition (e.g. reciprocal of mean slowest 1% frame times; do not mix with p99 inverse), p95/p99 frame time in ms, system memory availability, swap activity, VRAM, GPU utilization and CPU saturation. Report variance/range; review >3% median FPS or >5% p99 degradation only after repeatability is established. Compare with and without recording/profile changes separately. Do not claim causation from one run or a Fastfetch screenshot.

## 6. Release gates

No release until security (V-08, V-09, V-11, V-16, V-17), session (V-03, V-04), recovery (V-29, V-30) and other MUST requirements have evidence. If clipboard history cannot be made safe, leave it disabled and document policy; test basic copy/paste independently. Optional features may be skipped with reason. Record known bugs, upstream issue links, workaround and rollback. A portable CI pass does not satisfy any physical runtime test.
