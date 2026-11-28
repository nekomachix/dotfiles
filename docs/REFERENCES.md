# References and verification policy

Reference review: 2026-11-28. These links document intended integration, not a locked package set. Prefer installed manuals and version-tagged upstream docs over latest development pages. Record exact versions and commands during host validation. No upstream configs are vendored; examples are original minimal scaffolds or interface sketches.

| Topic | Upstream reference | Use |
|---|---|---|
| CachyOS gaming | [Gaming guide](https://wiki.cachyos.org/configuration/gaming/) | Meta-package, Proton variants, GameMode/Ananicy warning |
| CachyOS | [Wiki](https://wiki.cachyos.org/) | Installation, hardware and native settings |
| MangoWM | [Project](https://github.com/mangowm/mango), [configuration basics](https://mangowm.github.io/docs/configuration/basics/) | Config paths, includes, autostart, validation; match installed version |
| MangoWM portals | [XDG portal guide](https://mangowm.github.io/docs/configuration/xdg-portals/) | Desktop identifier, chooser, clipboard, keyring, limitations |
| UWSM | [Arch manual](https://man.archlinux.org/man/uwsm.1.en), [ArchWiki](https://wiki.archlinux.org/title/Universal_Wayland_Session_Manager) | Session lifecycle and finalization |
| Keyring | [ArchWiki](https://wiki.archlinux.org/title/GNOME/Keyring), [PAM documentation](https://wiki.gnome.org/Projects/GnomeKeyring/Pam) | TTY password-based unlocking; inspect stack |
| Packages | [Arch package search](https://archlinux.org/packages/), [MangoWM](https://archlinux.org/packages/extra/x86_64/mangowm/), [mate-polkit](https://archlinux.org/packages/extra/x86_64/mate-polkit/) | Candidate names; actual CachyOS Pacman metadata authoritative |
| Portals | [XDG portal docs](https://flatpak.github.io/xdg-desktop-portal/), [WLR backend](https://github.com/emersion/xdg-desktop-portal-wlr) | Interface routing and supported methods |
| Bar / launcher | [Waybar](https://github.com/Alexays/Waybar), [Rofi](https://github.com/davatorium/rofi) | Native modules and Wayland support |
| Notifications / OSD | [SwayNC](https://github.com/ErikReider/SwayNotificationCenter), [SwayOSD](https://github.com/ErikReider/SwayOSD) | Widget and service options |
| Wallpaper / color | [Awww](https://codeberg.org/LGFae/awww), [Matugen](https://github.com/InioX/matugen) | Daemon/client and template syntax |
| Lock / idle | [swaylock](https://github.com/swaywm/swaylock), [swayidle](https://github.com/swaywm/swayidle) | Installed manual for readiness and inhibition |
| Clipboard | [Cliphist](https://github.com/sentriz/cliphist), [wl-clipboard](https://github.com/bugaevc/wl-clipboard), [KeePassXC](https://keepassxc.org/docs/) | History/privacy and password integration |
| Terminal / files | [Kitty](https://sw.kovidgoyal.net/kitty/), [Yazi](https://yazi-rs.github.io/), [Thunar](https://docs.xfce.org/xfce/thunar/start) | Image protocols, GUI integration |
| Editors | [Neovim](https://neovim.io/doc/), [Zed Linux](https://zed.dev/docs/linux) | LSP and graphics/desktop requirements |
| Media | [MPD](https://www.musicpd.org/doc/html/), [RMPC](https://rmpc.mierak.dev/), [MPV](https://mpv.io/manual/stable/), [UOSC](https://github.com/tomasklaen/uosc) | User daemon and media interface |
| Discord | [Discord terms](https://discord.com/terms), [Yapfast](https://github.com/yapfast/yapfast) | Account risks and experimental upstream review |
| Gaming | [Proton-CachyOS](https://github.com/CachyOS/proton-cachyos), [MangoHud](https://github.com/flightlessmango/MangoHud), [GPU Screen Recorder](https://git.dec05eba.com/gpu-screen-recorder/about/) | Compatibility and measurement |

Some secondary links are reference pointers for future implementation rather than independently reverified on the review date. Check availability, package versions and licensing before incorporating code or binaries. Never infer compatibility solely from the presence of an Arch package.

The first deployment trial used the CachyOS MangoWM 0.18.6-1.1 package and the Arch UWSM 0.27.2-1 package on 2026-11-28. The packaged desktop entry, Mango parser, and UWSM manual establish the launch syntax. The Waybar 0.16.0-3.1 package supplies the Mango workspace and window modules. Confirm syntax again after updating those packages.

The idle and clipboard regression checks use swayidle 1.9.1-1.1, systemd 262.2-1, wl-clipboard 1:2.3.0-1.1, and Satty 0.23.0-1.1. The packaged swayidle manual documents explicit config selection. The systemd-run and wl-copy manuals document scope inheritance and the clipboard owner process. Satty exposes its copy command through its CLI. [Satty CLI](https://satty-org.github.io/Satty/usage/cli/)
