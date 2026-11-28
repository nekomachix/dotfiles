# Agent and contributor contract

## Mission and authority

This repository configures a lightweight CachyOS desktop; it is not a replacement distribution. `docs/REQUIREMENTS.md` is the requirements baseline, `docs/DECISIONS.md` records architectural choices, and the implementation and validation plans define the work and proof. If a conflict exists, report it and resolve it explicitly rather than quietly changing the stack. User instructions supersede proposals in this scaffold.

## Non-negotiable rules

1. Preserve CachyOS-managed kernel/firmware, repositories, hardware profile, ZRAM, sysctl and scheduling defaults. Do not add performance hacks without measured evidence and an approved decision.
2. Use authenticated TTY login, never auto-login. Do not change PAM, polkit, bootloader, partitions, encryption, sudoers, login shells or system services without an explicit reviewed action and recovery path.
3. No all-in-one desktop shells. Each component has one owner and a defined lifecycle. No overlapping clipboard watchers, notification daemons, polkit agents, Secret Service providers, automounters or session managers.
4. Prefer current stable repository packages, using normal Pacman repository priority. No partial upgrades, forced overwrites, unsigned packages, blind AUR helpers, `curl | sh`, or development builds as silent fallback.
5. Do not embed tokens, keyrings, password vaults, credentials, private logs, user paths or machine-specific outputs. Yapfast is experimental and never default. Clipboard history remains off until the sensitive-data test passes or the user knowingly accepts a documented residual risk.
6. No production activation of `*.example` files. Verify versions and actual config grammar, executable paths, protocol support, service ownership and logout behavior first. Preserve an accessible recovery TTY.
7. Plan changes before applying; never use destructive defaults. Use absolute resolved paths, quote shell variables, treat filenames as data, and do not execute text selected from a launcher. Avoid `eval`. Use explicit allowlists for power actions.
8. Preserve active work: never kill arbitrary processes, flush caches, stop shared system services or restart a compositor during wallpaper/theme changes or gaming profile changes.

## Engineering workflow

- Identify requirement ID, milestone and validation cases before changing files.
- Consult installed `man` pages, package metadata, and release-tag documentation. The references list is not a version lock. Record source URL, version and check date for syntax-sensitive decisions.
- Add candidate package names to the correct manifest; optional/experimental artifacts remain outside the default profile. Run `dotctl validate` and `dotctl doctor` on the host.
- Keep static settings separate from generated theme files and local overrides. Never commit secrets or user state. Design for XDG directories, quoted paths and atomic writes. Do not generate directly into tracked/symlinked config sources.
- Keep scripts small, fail clearly, provide dry-run for mutating operations, and use bounded retries. New mutating operations need explicit apply, conflict detection, backup manifest and tested rollback. No blanket chmod/chown or deletion.
- Unit files must use correct user/system scope and stop with the session. Avoid blind enablement of all units, duplicated XDG autostart and `exec_once` processes. Verify with `systemd-analyze --user verify` where possible.
- Tests must distinguish portable static tests, host integration, and physical gaming/security tests. A skipped test is not a pass. Record actual command results, package versions, and known blockers.

## Definition of done

A change is done when the relevant acceptance criteria are met, documentation is updated, portable tests pass, configuration validation is recorded, recovery is possible, and affected host tests have evidence or an explicit pending status. Changes in authentication, clipboard privacy, lock/suspend, package updates and rollback are release blockers until validated.

## Commands

```sh
./scripts/dotctl validate
./scripts/dotctl plan --profile daily
./scripts/dotctl doctor --profile gaming
python3 -m unittest discover -s tests -v
bash -n install.sh
```

These commands do not install packages or enable services. Do not claim that passing them establishes a working desktop.
