import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/dotctl"


class ScaffoldTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), *args], cwd=ROOT,
                              capture_output=True, text=True, timeout=10)

    def test_validate(self):
        result = self.run_cli("validate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Host checks NOT run", result.stdout)

    def test_all_profiles_plan(self):
        profiles = json.loads((ROOT / "profiles/profiles.json").read_text())["profiles"]
        for profile in profiles:
            with self.subTest(profile=profile):
                result = self.run_cli("plan", "--profile", profile)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("sudo pacman -Syu --needed", result.stdout)
                self.assertIn("No packages, configurations or services were changed", result.stdout)
                self.assertNotIn(" yapfast", result.stdout)
                self.assertNotIn(" wl-clip-persist", result.stdout)
                self.assertIn(" uwsm", result.stdout)

    def test_optional_group(self):
        result = self.run_cli("plan", "--profile", "gaming", "--with", "bluetooth", "--with", "bluetooth")
        self.assertEqual(result.returncode, 0)
        command = next(line for line in result.stdout.splitlines() if line.startswith("sudo "))
        self.assertEqual(command.split().count("bluez"), 1)
        self.assertIn("proton-cachyos-slr", command)

    def test_audit_cannot_install(self):
        self.assertNotEqual(self.run_cli("plan", "--with", "native-audit").returncode, 0)

    def test_no_apply_mode(self):
        self.assertNotEqual(self.run_cli("plan", "--apply").returncode, 0)

    def test_wrapper(self):
        result = subprocess.run(["bash", str(ROOT / "install.sh"), "--profile", "minimal"],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PLAN ONLY", result.stdout)

    def test_requirement_traceability(self):
        import re
        req = (ROOT / "docs/REQUIREMENTS.md").read_text()
        val = (ROOT / "docs/VALIDATION.md").read_text()
        ids = re.findall(r"^\| (V-\d+) \|", val, re.M)
        self.assertEqual(len(ids), 35)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(set(re.findall(r"V-\d+", req)).issubset(ids))


if __name__ == "__main__":
    unittest.main()
