#!/usr/bin/env python3
"""Validate ai_info as a maintainable Markdown knowledge base."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.yaml"
ARTICLE_DIRS = (
    ROOT / "anthropic" / "engineering",
    ROOT / "openai" / "research",
)
SUMMARY_FILES = (
    ROOT / "anthropic" / "engineering" / "summary.md",
    ROOT / "openai" / "research" / "summary.md",
)
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def article_files() -> list[Path]:
    files: list[Path] = []
    for directory in ARTICLE_DIRS:
        if directory.exists():
            files.extend(p for p in directory.glob("*.md") if p.name != "summary.md")
    return sorted(files)


def markdown_files() -> list[Path]:
    return sorted(ROOT.rglob("*.md"))


def has_line(text: str, marker: str) -> bool:
    return any(marker in line for line in text.splitlines()[:12])


def check_no_bom(errors: list[str]) -> None:
    for path in markdown_files():
        if path.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append(f"{rel(path)} starts with UTF-8 BOM")


def check_directory_names(errors: list[str]) -> None:
    bad = [p for p in ROOT.rglob("*") if "reserch" in p.parts]
    if bad:
        errors.extend(f"misspelled directory/path remains: {rel(p)}" for p in bad)
    if not (ROOT / "openai" / "research").is_dir():
        errors.append("missing expected directory: openai/research")


def check_article_metadata(errors: list[str]) -> None:
    for path in article_files():
        text = path.read_text(encoding="utf-8-sig")
        first = text.splitlines()[0] if text.splitlines() else ""
        if not first.startswith("# "):
            errors.append(f"{rel(path)} missing H1 title")
        for marker, name in (
            ("**原文链接**", "source link"),
            ("**发布日期**", "published date"),
            ("**标签**", "tags"),
        ):
            if not has_line(text, marker):
                errors.append(f"{rel(path)} missing {name} metadata")


def check_local_links(errors: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8-sig")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith("#"):
                continue
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            target_path = (path.parent / unquote(file_part)).resolve()
            try:
                target_path.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{rel(path)} links outside ai_info: {target}")
                continue
            if not target_path.exists():
                line_no = text[: match.start()].count("\n") + 1
                errors.append(f"{rel(path)}:{line_no} broken local link: {target}")


def check_catalog(errors: list[str]) -> None:
    if not CATALOG.exists():
        errors.append("catalog.yaml is missing")
        return
    text = CATALOG.read_text(encoding="utf-8")
    paths = re.findall(r"^  - path: '([^']+)'", text, flags=re.MULTILINE)
    urls = re.findall(r"^    source_url: '([^']+)'", text, flags=re.MULTILINE)
    article_paths = [rel(p) for p in article_files()]
    missing = sorted(set(article_paths) - set(paths))
    extra = sorted(set(paths) - set(article_paths))
    if missing:
        errors.append("catalog.yaml missing article paths: " + ", ".join(missing))
    if extra:
        errors.append("catalog.yaml has stale article paths: " + ", ".join(extra))
    seen: set[str] = set()
    dupes = sorted({url for url in urls if url in seen or seen.add(url)})
    if dupes:
        errors.append("catalog.yaml has duplicate source_url values: " + ", ".join(dupes))


def check_summary_numbering(errors: list[str]) -> None:
    for path in SUMMARY_FILES:
        if not path.exists():
            errors.append(f"missing summary file: {rel(path)}")
            continue
        text = path.read_text(encoding="utf-8-sig")
        nums = [int(m.group(1)) for m in re.finditer(r"^###\s+(\d+)\.", text, flags=re.MULTILINE)]
        if nums and nums != list(range(1, len(nums) + 1)):
            errors.append(f"{rel(path)} has non-sequential numbered H3 headings: {nums}")


def main() -> int:
    errors: list[str] = []
    check_no_bom(errors)
    check_directory_names(errors)
    check_article_metadata(errors)
    check_local_links(errors)
    check_catalog(errors)
    check_summary_numbering(errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: {len(article_files())} articles, {len(markdown_files())} markdown files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
