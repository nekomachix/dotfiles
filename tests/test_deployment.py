import argparse
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from desktop import deploy


class DeploymentTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="desktop test ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.env = dict(os.environ, XDG_CONFIG_HOME=str(self.root / "config"),
                        XDG_DATA_HOME=str(self.root / "data"), XDG_STATE_HOME=str(self.root / "state"))
        self.config = self.root / "config"
        self.journal = self.root / "state/dotfiles/deploy/history.json"

    def cli(self, *args, success=True):
        result = subprocess.run([sys.executable, ROOT / "scripts/dotctl", *args], text=True,
                                capture_output=True, env=self.env, timeout=20)
        self.assertEqual(result.returncode == 0, success, result.stderr)
        return result

    @unittest.skipIf(os.getuid() == 0, "user deployment requires an unprivileged account")
    def test_backup_conflict_idempotence_and_rollback(self):
        target = self.config / "kitty/kitty.conf"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"original")
        target.chmod(0o640)
        self.cli("deploy", "install", success=False)
        self.cli("deploy", "install", "--replace")
        self.assertFalse(self.journal.exists())
        self.cli("deploy", "install", "--replace", "--apply")
        deployed = target.read_bytes()
        self.cli("deploy", "install", "--apply")
        self.assertEqual(len(json.loads(self.journal.read_text())), 1)
        target.write_bytes(b"my edit")
        self.cli("deploy", "rollback", "--apply", success=False)
        self.assertEqual(target.read_bytes(), b"my edit")
        target.write_bytes(deployed)
        self.cli("deploy", "rollback", "--apply")
        self.assertEqual(target.read_bytes(), b"original")
        self.assertEqual(target.stat().st_mode & 0o777, 0o640)
        self.assertFalse((self.config / "mango/config.conf").exists())

    def test_parent_symlink_conflict(self):
        self.config.mkdir()
        (self.config / "kitty").symlink_to(self.root)
        self.cli("deploy", "install", "--replace", success=False)
        self.assertFalse(self.journal.exists())

    @unittest.skipIf(os.getuid() == 0, "user deployment requires an unprivileged account")
    def test_interrupted_apply(self):
        args = argparse.Namespace(action="install", apply=True, replace=False)
        real_restore = deploy.restore
        def interrupt(path, contents):
            if path.name == "config.jsonc":
                raise OSError("interrupted")
            real_restore(path, contents)
        with patch.dict(os.environ, self.env), patch.object(deploy, "restore", side_effect=interrupt):
            with self.assertRaises(OSError):
                deploy.run(args)
        self.cli("deploy", "install", "--apply", success=False)
        self.cli("deploy", "rollback", "--apply")
        self.cli("deploy", "install", "--apply")
        self.assertTrue((self.config / "mango/config.conf").exists())

    @unittest.skipIf(os.getuid() == 0, "user deployment requires an unprivileged account")
    def test_concurrent_edit_to_unattempted_file_does_not_block_rollback(self):
        first = self.config / "mango/config.conf"
        later = self.config / "waybar/config.jsonc"
        original_restore = deploy.restore
        independent = b"independent file"

        def edit_later(path, value):
            original_restore(path, value)
            if path == first:
                later.parent.mkdir()
                later.write_bytes(independent)

        args = argparse.Namespace(action="install", apply=True, replace=False)
        with patch.dict(os.environ, self.env), patch.object(deploy, "restore", side_effect=edit_later):
            with self.assertRaisesRegex(ValueError, "Concurrent edit"):
                deploy.run(args)
        self.assertEqual(len(json.loads(self.journal.read_text())[-1]["files"]), 1)
        self.cli("deploy", "rollback", "--apply")
        self.assertFalse(first.exists())
        self.assertEqual(later.read_bytes(), independent)
        self.cli("deploy", "install", "--apply", "--replace")
        self.cli("deploy", "rollback", "--apply")
        self.assertEqual(later.read_bytes(), independent)

    @unittest.skipIf(os.getuid() == 0, "user deployment requires an unprivileged account")
    def test_checkout_rejected_before_install_creates_state(self):
        alias = self.root / "checkout"
        alias.symlink_to(ROOT, target_is_directory=True)
        for variable in ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME"):
            for path in (ROOT / "desktop", alias / "desktop"):
                with self.subTest(variable=variable, path=path), patch.dict(self.env, {variable: str(path)}):
                    result = self.cli("deploy", "install", "--apply", success=False)
                    self.assertIn("inside the repository", result.stderr)
                    self.assertFalse(self.journal.parent.exists())

    @unittest.skipIf(os.getuid() == 0, "user deployment requires an unprivileged account")
    def test_legacy_rollback_rejects_checkout_targets(self):
        alias = self.root / "checkout"
        alias.symlink_to(ROOT, target_is_directory=True)
        self.journal.parent.mkdir(parents=True, mode=0o700)
        for path in (ROOT / "desktop/files.json", alias / "desktop/files.json"):
            with self.subTest(path=path):
                journal = [{"status": "complete", "files": [[str(path), None, deploy.snapshot(path.resolve())]]}]
                self.journal.write_text(json.dumps(journal))
                result = self.cli("deploy", "rollback", "--apply", success=False)
                self.assertIn("inside the repository", result.stderr)
                self.assertEqual(json.loads(self.journal.read_text()), journal)
                self.assertFalse((self.journal.parent / "lock").exists())
        for state in (ROOT / "desktop", alias / "desktop"):
            with patch.dict(self.env, XDG_STATE_HOME=str(state)):
                result = self.cli("deploy", "rollback", "--apply", success=False)
                self.assertIn("inside the repository", result.stderr)

    @unittest.skipIf(os.getuid() == 0, "user deployment requires an unprivileged account")
    def test_legacy_rollback_restores_owned_file(self):
        path = self.root / "legacy.conf"
        path.write_bytes(b"before")
        old = deploy.snapshot(path)
        path.write_bytes(b"installed")
        self.journal.parent.mkdir(parents=True, mode=0o700)
        self.journal.write_text(json.dumps([{"status": "complete", "files": [[str(path), old, deploy.snapshot(path)]]}]))
        self.cli("deploy", "rollback", "--apply")
        self.assertEqual(path.read_bytes(), b"before")

    def test_fallback_theme(self):
        self.cli("theme", "init", "--dry-run")
        self.assertFalse(self.config.exists())
        self.cli("theme", "init")
        current = self.config / "dotfiles/theme/current"
        first = current.resolve()
        self.cli("theme", "init")
        self.assertEqual(current.resolve(), first)
        self.assertIn("@define-color", (current / "palette.css").read_text())
        self.cli("theme", "apply", str(self.root / "missing"), success=False)
        self.assertEqual(current.resolve(), first)

    def test_theme_reload_failure_restores_previous_revision(self):
        import runpy

        self.cli("theme", "init")
        current = self.config / "dotfiles/theme/current"
        old = current.resolve()
        image = self.root / "wallpaper.png"
        image.touch()
        main = runpy.run_path(str(ROOT / "desktop/theme/tool"))["main"]
        render = main.__globals__["render"]
        failure = subprocess.CalledProcessError(1, "systemctl")
        wallpaper = unittest.mock.Mock()
        reload_clients = unittest.mock.Mock(side_effect=[failure, None])
        env = dict(self.env, WAYLAND_DISPLAY="wayland-test", XDG_CURRENT_DESKTOP="mango:wlroots")
        with patch.dict(os.environ, env), patch.object(sys, "argv", ["theme", "apply", str(image)]), \
                patch.dict(main.__globals__, render=lambda stage, _: render(stage, None),
                           wallpaper=wallpaper, reload_clients=reload_clients):
            with self.assertRaises(subprocess.CalledProcessError):
                main()
        self.assertEqual(current.resolve(), old)
        self.assertEqual(wallpaper.call_count, 2)
        wallpaper.assert_called_with(old)
