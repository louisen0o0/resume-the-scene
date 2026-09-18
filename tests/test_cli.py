from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class CliTest(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "resume_scene.cli", *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_help_lists_v03_working_commands(self):
        result = self._run("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("init|validate|docs|checkpoint|resume|handoff", result.stdout)

    def test_cli_init_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            init = self._run("init", str(root))
            self.assertEqual(init.returncode, 0)
            self.assertEqual(init.stdout.strip(), "@result{op:init|state:pass|count:4}")

            validate = self._run("validate", str(root))
            self.assertEqual(validate.returncode, 0)
            self.assertEqual(validate.stdout.strip(), "@result{op:validate|state:pass|count:4}")

            handoff = self._run("handoff", str(root))
            self.assertEqual(handoff.returncode, 0)
            lines = handoff.stdout.strip().splitlines()
            self.assertEqual(len(lines), 5)
            self.assertTrue(lines[0].startswith("@doc{id:#project|"))
            self.assertTrue(lines[3].startswith("@checkpoint{"))
            self.assertTrue(lines[4].startswith("@msg{op:resume|"))

    def test_cli_init_collision_is_machine_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "PROJECT.rsm").write_text("occupied\n", encoding="utf-8")
            result = self._run("init", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout.strip(), "@result{op:cli|state:error|code:E_INIT_EXISTS}")

    def test_cli_handoff_matches_fixture(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "handoff"
        expected = (root / "expected" / "handoff.rsm").read_text(encoding="utf-8").strip()
        result = self._run("handoff", str(root))
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), expected)


if __name__ == "__main__":
    unittest.main()
