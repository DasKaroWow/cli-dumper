from pathlib import Path

from dumper.display import print_included


def matches_any_glob(path: Path, root: Path, patterns: list[str]) -> bool:
    path = path.resolve().relative_to(root.resolve())
    return any(path.match(pattern) for pattern in patterns)


def find_targets(globs: list[str], ignored_dirs: list[str], ignored_files: list[str], root: Path) -> set[Path]:
    paths_to_include = set()

    for current_root, current_dirs, current_files in root.walk(top_down=True):
        current_dirs[:] = [d for d in current_dirs if d not in ignored_dirs]
        current_files[:] = [f for f in current_files if f not in ignored_files]
        for filename in current_files:
            filepath = current_root / filename
            if matches_any_glob(filepath, root, globs):
                paths_to_include.add(filepath.resolve())

    return paths_to_include


def process_targets(filepaths: set[Path], root: Path, output: Path) -> None:
    with output.open("w", encoding="utf-8") as out:
        for filepath in filepaths:
            rel_path = filepath.relative_to(root)
            out.write(f"# {rel_path.as_posix()}\n")
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            out.write(content)
            out.write("\n\n")
            print_included(rel_path)
