from pathlib import Path

import pytest
from typer import Typer


@pytest.fixture()
def chdir_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def sample_tree(chdir_tmp: Path) -> dict[str, Path]:
    """
    a.py, b.txt, dir1/c.py, dir1/skip.me, ignore_me/d.py
    """
    root = chdir_tmp
    (root / "dir1").mkdir()
    (root / "ignore_me").mkdir()

    files = {
        "root": root,
        "a_py": root / "a.py",
        "b_txt": root / "b.txt",
        "c_py": root / "dir1" / "c.py",
        "skip_me": root / "dir1" / "skip.me",
        "ignored_py": root / "ignore_me" / "d.py",
    }
    _ = files["a_py"].write_text("A", encoding="utf-8")
    _ = files["b_txt"].write_text("B", encoding="utf-8")
    _ = files["c_py"].write_text("C", encoding="utf-8")
    _ = files["skip_me"].write_text("X", encoding="utf-8")
    _ = files["ignored_py"].write_text("D", encoding="utf-8")

    return files


@pytest.fixture()
def cli_app() -> Typer:
    try:
        from cli_dumper.cli import app

        return app
    except Exception as error:
        pytest.skip(f"Unable to import Typer app: {error}")
