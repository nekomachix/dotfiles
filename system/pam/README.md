# PAM review gate

Compare installed `/etc/pam.d/login` and included stacks against ArchWiki GNOME Keyring guidance. Typical hooks are `auth optional pam_gnome_keyring.so` and `session optional pam_gnome_keyring.so auto_start`, but placement depends on existing control flow. These are not a patch. Never append blindly. Backup with permissions, retain an authenticated recovery TTY, test new login and synthetic keyring entry; restore immediately on failure. V-17/V-30 required.
