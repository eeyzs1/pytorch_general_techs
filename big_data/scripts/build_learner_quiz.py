#!/usr/bin/env python3
"""Create a learner-facing quiz file by removing answer/explanation lines."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "交互式学习_随堂测验题库.md"
TARGET = ROOT / "learner" / "随堂测验题库_学员版.md"
ANSWER_PREFIXES = ("**正确答案：", "**参考答案：", "**解析：")


def main() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    output: list[str] = [
        "# 大数据随堂测验题库（学员版）",
        "",
        "> 本文件由 `scripts/build_learner_quiz.py` 从原题库生成，已移除正确答案和解析。",
        "",
    ]
    skip_continuation = False
    for line in lines:
        if line.startswith("# 大数据随堂测验题库"):
            continue
        if line.startswith(ANSWER_PREFIXES):
            skip_continuation = True
            continue
        if skip_continuation:
            if not line.strip() or line.startswith("---") or line.startswith("**第") or line.startswith("### ") or line.startswith("## "):
                skip_continuation = False
            else:
                continue
        output.append(line)
    TARGET.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote learner quiz to {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
