from pathlib import Path

from pytest import CaptureFixture

from cli_dumper.core import find_targets, matches_any_glob, process_targets


def test_matches_any_glob(sample_tree: dict[str, Path]) -> None:
    root: Path = sample_tree["root"]
    file_py: Path = sample_tree["c_py"]
    assert matches_any_glob(file_py, root, [".py"])
    assert not matches_any_glob(file_py, root, [".txt"])
    assert matches_any_glob(file_py, root, [".md", ".py"])
    assert matches_any_glob(sample_tree["a_py"], root, [".py"])


def test_find_targets_respects_globs_and_ignores(sample_tree: dict[str, Path]) -> None:
    root: Path = sample_tree["root"]
    globs = [".py"]
    ignored_dirs = ["ignore_me"]
    ignored_files = ["skip.me"]

    targets = find_targets(globs, ignored_dirs, ignored_files, root)
    rel = {p.relative_to(root).as_posix() for p in targets}
    assert rel == {"a.py", "dir1/c.py"}  # d.py и skip.me исключены


def test_process_targets_writes_headers_and_prints(
    sample_tree: dict[str, Path], capsys: CaptureFixture[str]
) -> None:
    root: Path = sample_tree["root"]
    f1: Path = sample_tree["a_py"]
    f2: Path = sample_tree["c_py"]

    output = root / "project_dump.txt"
    process_targets({f1, f2}, root, output)

    assert output.exists()
    content = output.read_text(encoding="utf-8")
    assert "# a.py" in content
    assert "# dir1/c.py" in content

    out = capsys.readouterr().out
    assert "file included" in out
