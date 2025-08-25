from pathlib import Path
from typer.testing import CliRunner
from dumper.cli import app
from typer import Typer
from click.testing import Result
from pytest import MonkeyPatch


def run_cli(app: Typer, *args: str) -> Result:
    return CliRunner().invoke(app, list(args))

def test_cli_dumper_creates_dump_and_summary(cli_app: Typer,sample_tree: dict[str, Path], monkeypatch: MonkeyPatch) -> None:
    root: Path = sample_tree["root"]
    monkeypatch.chdir(root)

    result = run_cli(
        cli_app,
            "--globs", "*.py",
            "--ignored-dirs", "ignore_me",
            "--ignored-files", "skip.me",
    )

    assert result.exit_code == 0, result.stdout
    dump = root / "project_dump.txt"
    assert dump.exists()

    txt = dump.read_text(encoding="utf-8")
    assert "# a.py" in txt
    assert "# dir1/c.py" in txt
    assert "# dir1/skip.me" not in txt
    assert "# ignore_me/d.py" not in txt

    stdout = result.stdout
    assert "Summary" in stdout
    assert "Included:" in stdout
    assert "file included" in stdout

def test_cli_requires_globs_arg(cli_app: Typer, sample_tree: dict[str, Path], monkeypatch: MonkeyPatch) -> None:
    root: Path = sample_tree["root"]
    monkeypatch.chdir(root)

    result = run_cli(cli_app)
    assert result.exit_code != 0
    assert "Missing option '--globs'" in result.stderr
