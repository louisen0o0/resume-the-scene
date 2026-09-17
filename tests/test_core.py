from pathlib import Path
import unittest

from resume_scene.core import RSMError, checkpoint, parse_frame, resume, validate_tree


class CoreTest(unittest.TestCase):
    def test_parse_task(self):
        kind, fields = parse_frame("@task{id:#t1|goal:#g1|state:active|requires:[#a,#b]|done:[#e1]|next:#x1}")
        self.assertEqual(kind, "task")
        self.assertEqual(fields["requires"], ["#a", "#b"])

    def test_duplicate_rejected(self):
        with self.assertRaises(RSMError) as exc:
            parse_frame("@goal{id:#g1|id:#g2|state:active|accept:#a1}")
        self.assertEqual(exc.exception.code, "E_DUP")

    def test_required_rejected(self):
        with self.assertRaises(RSMError) as exc:
            parse_frame("@goal{id:#g1|state:active}")
        self.assertEqual(exc.exception.code, "E_REQUIRED")

    def test_example_tree(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "native"
        self.assertGreaterEqual(validate_tree(root), 6)
        cp1 = checkpoint(root)
        cp2 = checkpoint(root)
        self.assertEqual(cp1, cp2)
        msg = resume(root)
        self.assertTrue(msg.startswith("@msg{op:resume|task:#t1"))
        self.assertIn("skip:[#e1]", msg)
        self.assertIn("next:#a1", msg)


if __name__ == "__main__":
    unittest.main()
