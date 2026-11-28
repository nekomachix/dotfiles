import contextlib
import io
import os
import runpy
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

CLI = Path(__file__).resolve().parents[1] / "scripts/dotctl"
baseline = runpy.run_path(str(CLI))["baseline"]


class BaselineTests(unittest.TestCase):
    def collect(self, supported, replies):
        def run(argv, **kwargs):
            self.assertLessEqual(kwargs["timeout"], 10)
            if argv[0] == "pacman":
                return subprocess.CompletedProcess(argv, 0, f"{argv[-1]} 1.0", "")
            reply = replies[argv[0]]
            if isinstance(reply, Exception):
                raise reply
            return subprocess.CompletedProcess(argv, 0, reply, "private diagnostic")

        output = io.StringIO()
        with patch.dict(baseline.__globals__, supported_host=lambda: supported,
                        drm_inventory=lambda root: None), patch.dict(os.environ, {}, clear=True), \
                patch("subprocess.run", side_effect=run), contextlib.redirect_stdout(output):
            status = baseline()
        return status, output.getvalue()

    def test_supported(self):
        replies = {"pacman-conf": "core\nextra\n", "vulkaninfo": "deviceName = Test GPU\n",
                   "vainfo": "VAProfileH264Main : VAEntrypointVLD\n",
                   "zramctl": "/dev/zram0 4G\n", "systemctl": "active\n"}
        status, report = self.collect(True, replies)
        self.assertEqual(status, 0)
        for field in ("core, extra", "mesa 1.0", "Test GPU", "VAProfileH264Main",
                      "/dev/zram0 4G", "ananicy-cpp service: active", "manual checks"):
            self.assertIn(field, report)
        self.assertNotIn("private diagnostic", report)

    def test_unsupported(self):
        self.assertEqual(self.collect(False, {})[0], 2)

    def test_partial(self):
        replies = {"pacman-conf": "core", "vulkaninfo": subprocess.TimeoutExpired("probe", 10),
                   "vainfo": FileNotFoundError(), "zramctl": "", "systemctl": "inactive"}
        status, report = self.collect(True, replies)
        self.assertEqual(status, 0)
        self.assertIn("Vulkan devices: BLOCKED", report)
        self.assertIn("missing vainfo", report)
        self.assertIn("ananicy-cpp service: inactive", report)
