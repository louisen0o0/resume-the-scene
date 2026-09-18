from pathlib import Path
import tempfile
import unittest

from resume_scene.core import RSMError, checkpoint, parse_frame, resume, validate_tree


class CoreTest(unittest.TestCase):
    def _write_project(self, root: Path, memory_docs: list[str], doc_lines: list[str]) -> None:
        (root / ".resume").mkdir(parents=True, exist_ok=True)
        (root / "PROJECT.rsm").write_text(
            "@project{id:#p0|v:0.1|state:active|memory:#m0}\n",
            encoding="utf-8",
        )
        (root / "CURRENT.rsm").write_text(
            "@task{id:#t0|goal:#g0|state:active|requires:[]|done:[]|next:#a0}\n",
            encoding="utf-8",
        )
        memory = "@memory{id:#m0|mode:selected|docs:[" + ",".join(memory_docs) + "]}\n"
        (root / ".resume" / "memory.rsm").write_text(
            memory + "\n".join(doc_lines) + "\n",
            encoding="utf-8",
        )

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

    def test_handoff_expected_outputs(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "handoff"
        expected_checkpoint = (root / "expected" / "checkpoint.rsm").read_text(encoding="utf-8").strip()
        expected_resume = (root / "expected" / "resume.rsm").read_text(encoding="utf-8").strip()
        self.assertEqual(checkpoint(root), expected_checkpoint)
        self.assertEqual(resume(root), expected_resume)

    def test_mapped_layout_without_root_reorganization(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "mapped"
        self.assertFalse((root / "PROJECT.rsm").exists())
        self.assertFalse((root / "CURRENT.rsm").exists())
        self.assertGreaterEqual(validate_tree(root), 6)
        cp1 = checkpoint(root)
        cp2 = checkpoint(root)
        self.assertEqual(cp1, cp2)
        msg = resume(root)
        self.assertIn("task:#t3", msg)
        self.assertIn("load:[#p3,#s3,#t3,#e3,#d3]", msg)
        self.assertIn("skip:[#e3]", msg)
        self.assertIn("next:#a3", msg)

    def test_duplicate_primary_authority_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_project(
                root,
                ["#project", "#project2", "#current"],
                [
                    "@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:primary}",
                    "@doc{id:#project2|type:project|path:PROJECT.rsm|state:active|authority:primary}",
                    "@doc{id:#current|type:state|path:CURRENT.rsm|state:active|authority:primary}",
                ],
            )
            with self.assertRaises(RSMError) as exc:
                validate_tree(root)
            self.assertEqual(exc.exception.code, "E_AUTHORITY")

    def test_missing_primary_authority_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_project(
                root,
                ["#project", "#current"],
                [
                    "@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:primary}",
                    "@doc{id:#current|type:artifact|path:CURRENT.rsm|state:active|authority:primary}",
                ],
            )
            with self.assertRaises(RSMError) as exc:
                validate_tree(root)
            self.assertEqual(exc.exception.code, "E_AUTHORITY")

    def test_parent_escape_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "project"
            root.mkdir()
            (base / "outside.rsm").write_text(
                "@evidence{id:#e0|task:#t0|subject:#x|state:valid|ref:none|hash:none}\n",
                encoding="utf-8",
            )
            self._write_project(
                root,
                ["#project", "#current", "#escape"],
                [
                    "@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:primary}",
                    "@doc{id:#current|type:state|path:CURRENT.rsm|state:active|authority:primary}",
                    "@doc{id:#escape|type:evidence|path:../outside.rsm|state:active|authority:primary}",
                ],
            )
            with self.assertRaises(RSMError) as exc:
                validate_tree(root)
            self.assertEqual(exc.exception.code, "E_DOC_PATH")

    def test_absolute_path_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "project"
            root.mkdir()
            outside = base / "outside.rsm"
            outside.write_text(
                "@evidence{id:#e0|task:#t0|subject:#x|state:valid|ref:none|hash:none}\n",
                encoding="utf-8",
            )
            self._write_project(
                root,
                ["#project", "#current", "#escape"],
                [
                    "@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:primary}",
                    "@doc{id:#current|type:state|path:CURRENT.rsm|state:active|authority:primary}",
                    f"@doc{{id:#escape|type:evidence|path:{outside.resolve()}|state:active|authority:primary}}",
                ],
            )
            with self.assertRaises(RSMError) as exc:
                validate_tree(root)
            self.assertEqual(exc.exception.code, "E_DOC_PATH")

    def test_symlink_escape_rejected_before_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "project"
            root.mkdir()
            outside = base / "outside.rsm"
            outside.write_text(
                "@evidence{id:#e0|task:#t0|subject:#x|state:valid|ref:none|hash:none}\n",
                encoding="utf-8",
            )
            (root / "linked.rsm").symlink_to(outside)
            self._write_project(
                root,
                ["#project", "#current", "#escape"],
                [
                    "@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:primary}",
                    "@doc{id:#current|type:state|path:CURRENT.rsm|state:active|authority:primary}",
                    "@doc{id:#escape|type:evidence|path:linked.rsm|state:active|authority:primary}",
                ],
            )
            with self.assertRaises(RSMError) as exc:
                validate_tree(root)
            self.assertEqual(exc.exception.code, "E_DOC_PATH")

    def test_duplicate_doc_ids_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_project(
                root,
                ["#project", "#current"],
                [
                    "@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:primary}",
                    "@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:example}",
                    "@doc{id:#current|type:state|path:CURRENT.rsm|state:active|authority:primary}",
                ],
            )
            with self.assertRaises(RSMError) as exc:
                validate_tree(root)
            self.assertEqual(exc.exception.code, "E_DOC_DUP")

    def test_duplicate_memory_entries_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_project(
                root,
                ["#project", "#current", "#current"],
                [
                    "@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:primary}",
                    "@doc{id:#current|type:state|path:CURRENT.rsm|state:active|authority:primary}",
                ],
            )
            with self.assertRaises(RSMError) as exc:
                validate_tree(root)
            self.assertEqual(exc.exception.code, "E_MEMORY_DUP")

    def test_missing_selected_doc_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_project(
                root,
                ["#project", "#current", "#missing"],
                [
                    "@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:primary}",
                    "@doc{id:#current|type:state|path:CURRENT.rsm|state:active|authority:primary}",
                    "@doc{id:#missing|type:evidence|path:missing.rsm|state:active|authority:primary}",
                ],
            )
            with self.assertRaises(RSMError) as exc:
                validate_tree(root)
            self.assertEqual(exc.exception.code, "E_DOC_MISSING")


if __name__ == "__main__":
    unittest.main()
