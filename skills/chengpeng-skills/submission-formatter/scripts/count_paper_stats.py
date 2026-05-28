#!/usr/bin/env python3
"""
Count paper statistics: words, pages, figures, tables, references.
Usage: python count_paper_stats.py <paper.tex> [--venue MICCAI]
"""

import re
import sys
import argparse


def count_tex_stats(tex_path: str, venue: str = ""):
    with open(tex_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Remove comments
    text_no_comments = re.sub(r"(?<!\\)%.*", "", text)

    # Remove LaTeX commands (rough estimate)
    # Keep figure/table/content text
    body_match = re.search(
        r"\\begin\{document\}(.*?)\\end\{document\}",
        text_no_comments,
        re.DOTALL,
    )
    if body_match:
        body = body_match.group(1)
    else:
        body = text_no_comments

    # Remove command names
    clean = re.sub(r"\\[a-zA-Z]+(\[.*?\])?(\{.*?\})?", " ", body)
    # Remove math
    clean = re.sub(r"\$.*?\$", "", clean)
    clean = re.sub(r"\\\[.*?\\\]", "", clean, flags=re.DOTALL)
    clean = re.sub(r"\\begin\{equation\}.*?\\end\{equation\}", "", clean, flags=re.DOTALL)
    # Remove environments
    clean = re.sub(r"\\begin\{figure\}.*?\\end\{figure\}", "", clean, flags=re.DOTALL)
    clean = re.sub(r"\\begin\{table\}.*?\\end\{table\}", "", clean, flags=re.DOTALL)

    # Word count in body text
    words = clean.split()
    word_count = len([w for w in words if re.search(r"[a-zA-Z]", w)])

    # Figure count
    figures = len(re.findall(r"\\includegraphics", text))
    tables = len(re.findall(r"\\begin\{tabular\}", text))
    equations = len(re.findall(r"\\begin\{equation\}", text))
    refs = len(re.findall(r"\\bibitem", text))

    # Section count
    sections = len(re.findall(r"\\section\{", text))
    subsections = len(re.findall(r"\\subsection\{", text))

    print(f"{'='*50}")
    print(f"Paper: {tex_path}")
    if venue:
        print(f"Target Venue: {venue}")
    print(f"{'='*50}")
    print(f"Word count (body):    {word_count}")
    print(f"Figures:             {figures}")
    print(f"Tables:              {tables}")
    print(f"Equations:           {equations}")
    print(f"References:          {refs}")
    print(f"Sections:            {sections} (+ {subsections} subsections)")
    print(f"{'='*50}")

    # Venue-specific warnings
    venue_limits = {
        "MICCAI": {"max_words": 4500, "max_pages": 8, "max_refs": 20},
        "AAAI": {"max_words": 5000, "max_pages": 8, "max_refs": 30},
        "CVPR": {"max_words": 5000, "max_pages": 8, "max_refs": 40},
        "ISBI": {"max_words": 2500, "max_pages": 6, "max_refs": 15},
        "NATURE": {"max_words": 3000, "max_pages": None, "max_refs": 50},
        "MEDIA": None,  # no strict limits
    }

    if venue and venue.upper() in venue_limits:
        limits = venue_limits[venue.upper()]
        if limits:
            if limits["max_words"] and word_count > limits["max_words"]:
                print(f"⚠️  WARNING: Word count exceeds {venue} limit ({limits['max_words']}) by {word_count - limits['max_words']}")
            if limits["max_refs"] and refs > limits["max_refs"]:
                print(f"⚠️  WARNING: References exceed {venue} limit ({limits['max_refs']}) by {refs - limits['max_refs']}")

    return {
        "words": word_count,
        "figures": figures,
        "tables": tables,
        "equations": equations,
        "refs": refs,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count paper statistics from LaTeX source")
    parser.add_argument("tex_path", help="Path to .tex file")
    parser.add_argument("--venue", "-v", default="", help="Target venue for limit checks")
    args = parser.parse_args()
    count_tex_stats(args.tex_path, args.venue)
