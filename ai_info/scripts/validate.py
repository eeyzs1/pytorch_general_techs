#!/usr/bin/env python3
"""Validate ai_info as a maintainable Markdown knowledge base."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.yaml"
# 与 build_catalog.py 保持一致：动态扫描所有 provider 的文章
EXCLUDED_TOP_DIRS = {"scripts", "topics", ".trae", ".vscode", ".git"}
EXCLUDED_FILENAMES = {"summary.md", "README.md", "AGENTS.md"}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def article_dirs() -> list[Path]:
    """动态发现所有 provider/category 目录（与 build_catalog.py 一致）。"""
    dirs: list[Path] = []
    for provider_dir in ROOT.iterdir():
        if not provider_dir.is_dir():
            continue
        if provider_dir.name in EXCLUDED_TOP_DIRS or provider_dir.name.startswith("."):
            continue
        subdirs = [p for p in provider_dir.iterdir() if p.is_dir()]
        if subdirs:
            for category_dir in subdirs:
                dirs.append(category_dir)
        else:
            dirs.append(provider_dir)
    return sorted(dirs)


def summary_files() -> list[Path]:
    """动态发现所有 provider 的 summary.md 文件。"""
    files: list[Path] = []
    for provider_dir in ROOT.iterdir():
        if not provider_dir.is_dir():
            continue
        if provider_dir.name in EXCLUDED_TOP_DIRS or provider_dir.name.startswith("."):
            continue
        # provider/summary.md（扁平结构）
        flat_summary = provider_dir / "summary.md"
        if flat_summary.exists():
            files.append(flat_summary)
        # provider/{category}/summary.md（嵌套结构）
        for sub in provider_dir.iterdir():
            if sub.is_dir():
                nested_summary = sub / "summary.md"
                if nested_summary.exists():
                    files.append(nested_summary)
    return sorted(files)


def article_files() -> list[Path]:
    files: list[Path] = []
    for directory in article_dirs():
        if directory.exists():
            files.extend(
                p for p in directory.glob("*.md")
                if p.name not in EXCLUDED_FILENAMES
            )
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
    # 排除规则文件（AGENTS.md、.trae/rules/）——这些文件包含示例链接，不是真实链接
    excluded = {ROOT / "AGENTS.md"}
    for path in markdown_files():
        if path in excluded:
            continue
        # 跳过 .trae/ 目录下的规则文件
        try:
            path.relative_to(ROOT / ".trae")
            continue
        except ValueError:
            pass
        text = path.read_text(encoding="utf-8-sig")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith("#"):
                continue
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):
                continue
            # 跳过包含占位符的示例链接（如 {URL}、{相对路径}）
            if "{" in target and "}" in target:
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
    for path in summary_files():
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
