#!/usr/bin/env python3
"""Validate notebook structure, Python syntax, and declared dependencies."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
REQ_FILE = ROOT / "requirements.txt"

# Import names that are provided by packages whose PyPI requirement name differs.
PACKAGE_ALIASES = {
    "PIL": "pillow",
    "sklearn": "scikit-learn",
    "yaml": "pyyaml",
}

# Jupyter/runtime packages are environment dependencies, not imports expected in cells.
ENV_ONLY_REQUIREMENTS = {"jupyter", "ipykernel"}


@dataclass(frozen=True)
class Issue:
    path: Path
    message: str
    cell: int | None = None

    def format(self) -> str:
        rel = self.path.relative_to(ROOT)
        if self.cell is None:
            return f"{rel}: {self.message}"
        return f"{rel}:cell[{self.cell}]: {self.message}"


def iter_notebooks(paths: Iterable[str]) -> list[Path]:
    if paths:
        candidates = []
        for raw in paths:
            path = (ROOT / raw).resolve() if not Path(raw).is_absolute() else Path(raw)
            if path.is_dir():
                candidates.extend(path.rglob("*.ipynb"))
            else:
                candidates.append(path)
    else:
        candidates = list(ROOT.rglob("*.ipynb"))

    notebooks = []
    for path in candidates:
        if ".ipynb_checkpoints" in path.parts:
            continue
        notebooks.append(path)
    return sorted(set(notebooks))


def read_requirements() -> set[str]:
    if not REQ_FILE.exists():
        return set()
    packages: set[str] = set()
    for raw in REQ_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        name = line.split(";", 1)[0].strip()
        for sep in ("==", ">=", "<=", "~=", "!=", ">", "<"):
            if sep in name:
                name = name.split(sep, 1)[0].strip()
                break
        if name:
            packages.add(name.lower().replace("_", "-"))
    return packages


def normalize_package(import_name: str) -> str:
    return PACKAGE_ALIASES.get(import_name, import_name).lower().replace("_", "-")


def is_stdlib(name: str) -> bool:
    return name in getattr(sys, "stdlib_module_names", set()) or name.startswith("__future__")


def source_text(cell: dict) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(source)
    if isinstance(source, str):
        return source
    return ""


def source_line_issues(path: Path, cell: dict, idx: int) -> list[Issue]:
    source = cell.get("source", "")
    if not isinstance(source, list) or len(source) <= 1:
        return []
    missing = [line_no for line_no, line in enumerate(source[:-1], start=1) if not line.endswith("\n")]
    if not missing:
        return []
    preview = ", ".join(map(str, missing[:5]))
    suffix = "..." if len(missing) > 5 else ""
    return [Issue(path, f"source list lines missing trailing newline: {preview}{suffix}", idx)]


def validate_notebook(path: Path) -> tuple[list[Issue], set[str], int, int, int]:
    issues: list[Issue] = []
    imports: set[str] = set()
    code_cells = 0
    executed_cells = 0
    output_objects = 0

    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [Issue(path, f"invalid notebook JSON: {exc}")], imports, code_cells, executed_cells, output_objects

    if nb.get("nbformat") != 4:
        issues.append(Issue(path, f"expected nbformat=4, got {nb.get('nbformat')!r}"))
    metadata = nb.get("metadata", {})
    if "kernelspec" not in metadata:
        issues.append(Issue(path, "missing metadata.kernelspec"))
    if "language_info" not in metadata:
        issues.append(Issue(path, "missing metadata.language_info"))

    for idx, cell in enumerate(nb.get("cells", [])):
        issues.extend(source_line_issues(path, cell, idx))
        if cell.get("cell_type") != "code":
            continue
        code_cells += 1
        if cell.get("execution_count") is not None:
            executed_cells += 1
        output_objects += len(cell.get("outputs", []) or [])
        text = source_text(cell)
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            where = f"line {exc.lineno}, col {exc.offset}: {exc.msg}"
            issues.append(Issue(path, where, idx))
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".", 1)[0])
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imports.add(node.module.split(".", 1)[0])

    return issues, imports, code_cells, executed_cells, output_objects


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Notebook files or directories to validate")
    parser.add_argument(
        "--allow-dirty-outputs",
        action="store_true",
        help="Do not fail when notebooks contain executed cells or saved outputs.",
    )
    args = parser.parse_args()

    notebooks = iter_notebooks(args.paths)
    requirements = read_requirements()
    all_issues: list[Issue] = []
    imported: set[str] = set()
    total_code_cells = 0
    executed_code_cells = 0
    output_objects = 0

    for notebook in notebooks:
        issues, imports, code_cells, executed_cells, outputs = validate_notebook(notebook)
        all_issues.extend(issues)
        imported |= imports
        total_code_cells += code_cells
        executed_code_cells += executed_cells
        output_objects += outputs

    third_party = {
        normalize_package(name)
        for name in imported
        if not is_stdlib(name) and normalize_package(name) not in ENV_ONLY_REQUIREMENTS
    }
    missing_requirements = sorted(pkg for pkg in third_party if pkg not in requirements)
    if missing_requirements:
        all_issues.append(
            Issue(
                REQ_FILE,
                "missing requirements for imports: " + ", ".join(missing_requirements),
            )
        )

    if (executed_code_cells or output_objects) and not args.allow_dirty_outputs:
        all_issues.append(
            Issue(
                ROOT,
                f"dirty notebook state: {executed_code_cells} executed cells, {output_objects} output objects; clear outputs before committing",
            )
        )

    print(
        f"Validated {len(notebooks)} notebooks, {total_code_cells} code cells, "
        f"{len(third_party)} third-party imports."
    )
    if all_issues:
        print("\nIssues:")
        for issue in all_issues:
            print(f"- {issue.format()}")
        return 1

    print("All notebook checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
