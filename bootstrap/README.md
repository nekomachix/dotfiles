# Deploy and recover

Use a disposable CachyOS guest first. Use the daily or gaming package set for the full payload. Review the package transaction with `./install.sh --profile gaming`. Install the reviewed system transaction with Pacman separately.

1. Run `./scripts/dotctl deploy install` as the guest's login user and review its file destinations. Use `--replace` in the preview to see an installation that backs up existing regular files.
2. Add `--apply` to the reviewed command. The files listed in `desktop/files.json` are the installation payload. The private history under `${XDG_STATE_HOME:-~/.local/state}/dotfiles/deploy` records the original and installed contents and modes.
3. Log in with a password on tty1 and run `exec "${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/session"` from a Bourne-compatible login shell. The invoker uses `exec` so logout or a failed compositor cannot leave the authenticated launch shell available. Use a separately authenticated recovery TTY.
4. To roll back, log out of Mango. Preview with `./scripts/dotctl deploy rollback`, then add `--apply`. Rollback checks files the transaction attempted to write and preserves later edits. Keep the configured XDG destinations and journal outside the checkout. Complete rollback before retrying an interrupted apply. A fresh user login picks up restored systemd unit files.
5. Repeat the deployment and rollback in the guest. Record the physical release checks separately according to the validation plan.

In Mango, Super+Enter opens Kitty, Super+Space opens Rofi, Super+M starts MPD and its MPRIS bridge and opens RMPC, and Super+Shift+Q exits. MPD reads `~/Music` and binds to loopback. Update its library from RMPC. The configured media keys target MPD. Super+Shift+C toggles notification DND for gaming. Steam and GPU Screen Recorder launch on demand. Use `mangohud %command%` in Steam for per-title overlay and logging.

Run `./scripts/dotctl theme apply "/path/to/wallpaper" --dry-run` to generate and check a palette without activating it. From Mango, omit the flag to apply it. Use `./scripts/dotctl theme rollback` to switch back to the preceding successful revision. Kitty and Rofi read the new palette on their next launch.

Text clipboard history requires an explicit start of `dotfiles-history.service` during the Mango session. Use synthetic data for V-11 and stop the service before clearing with `cliphist wipe`. Leave it off for ordinary use until the privacy gate passes. Clipboard history and Satty use the Mango session to keep copied data available after the picker or editor exits. Daily applications use their packaged defaults wherever the payload has no override.
