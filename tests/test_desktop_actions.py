import runpy
import subprocess
import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch

ACTIONS = Path(__file__).resolve().parents[1] / "desktop/tools/actions"
power = runpy.run_path(str(ACTIONS))["power"]


class SuspendTest(unittest.TestCase):
    def test_suspend_requires_an_active_locker(self):
        commands = Mock()
        with patch.dict(power.__globals__, choose=Mock(return_value=b"Suspend"), run=commands):
            power()
        self.assertEqual(commands.call_args_list, [
            call("systemctl", "--user", "start", "dotfiles-lock.service"),
            call("systemctl", "--user", "is-active", "--quiet", "dotfiles-lock.service"),
            call("systemctl", "suspend"),
        ])

    def test_locker_failure_stops_suspend(self):
        commands = Mock(side_effect=[None, subprocess.CalledProcessError(3, "systemctl")])
        with patch.dict(power.__globals__, choose=Mock(return_value=b"Suspend"), run=commands):
            with self.assertRaises(subprocess.CalledProcessError):
                power()
        self.assertNotIn(call("systemctl", "suspend"), commands.call_args_list)
