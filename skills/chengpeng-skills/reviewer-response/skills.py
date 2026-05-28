#!/usr/bin/env python3
"""skills.py for reviewer-response — Organize reviewer comments into a structured evidence-response matrix, mapping each comment to paper sections and planned revisions."""
import re, json, os, sys

def main():
    print("[i] reviewer-response: Organize reviewer comments into a structured evidence-response matrix, mapping each comment to paper sections and planned revisions.")
    print("[i] Input types: 审稿意见文本 (.txt/.md), 论文 PDF 或 .tex 文件, 编辑决策信件（可选）")
    print("[i] Output: structured report")
    print("[i] Run with: python skills.py --input path/to/input/")
    print("[i] (Full implementation pending — see SKILL.md for workflow)")

if __name__ == "__main__":
    main()
