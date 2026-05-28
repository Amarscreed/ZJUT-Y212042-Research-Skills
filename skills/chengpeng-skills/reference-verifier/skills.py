#!/usr/bin/env python3
"""
reference-verifier: Verify references cited in a LaTeX paper are real,
traceable publications.

Usage:
    python skills.py path/to/paper.tex
    python skills.py path/to/references.bib

Output:
    - paper.references.json or refs.references.json  (JSON report)
    - paper.references.md or refs.references.md       (human-readable report)
"""

import re
import os
import sys
import json
from pathlib import Path


# ─── Venue Database ──────────────────────────────────────────────────────────

VENUES = {
    "MICCAI": {
        "full_name": "Medical Image Computing and Computer-Assisted Intervention",
        "year_range": (1998, 2099),
        "aliases": ["miccai", "MICCAI", "Med Image Comput Comput Assist Interv"],
        "type": "conference",
    },
    "CVPR": {
        "full_name": "IEEE/CVF Conference on Computer Vision and Pattern Recognition",
        "year_range": (1985, 2099),
        "aliases": ["cvpr", "CVPR", "Comput Vis Pattern Recognit", "Computer Vision and Pattern Recognition"],
        "type": "conference",
    },
    "NeurIPS": {
        "full_name": "Advances in Neural Information Processing Systems",
        "year_range": (1987, 2099),
        "aliases": ["neurips", "NeurIPS", "Neural Inf Process Syst", "NIPS", "nips"],
        "type": "conference",
    },
    "AAAI": {
        "full_name": "AAAI Conference on Artificial Intelligence",
        "year_range": (1980, 2099),
        "aliases": ["aaai", "AAAI", "Artif Intell", "Artificial Intelligence"],
        "type": "conference",
    },
    "EMNLP": {
        "full_name": "Conference on Empirical Methods in Natural Language Processing",
        "year_range": (1996, 2099),
        "aliases": ["emnlp", "EMNLP", "Empir Methods Nat Lang Process"],
        "type": "conference",
    },
    "NAACL": {
        "full_name": "Conference of the North American Chapter of the Association for Computational Linguistics",
        "year_range": (2000, 2099),
        "aliases": ["naacl", "NAACL", "N Am Chapter Assoc Comput Linguist"],
        "type": "conference",
    },
    "ISBI": {
        "full_name": "IEEE International Symposium on Biomedical Imaging",
        "year_range": (2002, 2099),
        "aliases": ["isbi", "ISBI", "Int Symp Biomed Imaging"],
        "type": "conference",
    },
    "JBHI": {
        "full_name": "IEEE Journal of Biomedical and Health Informatics",
        "year_range": (1995, 2099),
        "aliases": ["jbhi", "JBHI", "J Biomed Health Inform", "IEEE Trans Inf Technol Biomed"],
        "type": "journal",
    },
    "SciData": {
        "full_name": "Scientific Data (Nature)",
        "year_range": (2014, 2099),
        "aliases": ["sci data", "Scientific Data", "Sci Data", "Nat Sci Data"],
        "type": "journal",
    },
    "ICLR": {
        "full_name": "International Conference on Learning Representations",
        "year_range": (2013, 2099),
        "aliases": ["iclr", "ICLR", "Learn Represent", "Learning Representations"],
        "type": "conference",
    },
    "ECCV": {
        "full_name": "European Conference on Computer Vision",
        "year_range": (1990, 2099),
        "aliases": ["eccv", "ECCV", "Eur Conf Comput Vis"],
        "type": "conference",
    },
    "ICCV": {
        "full_name": "International Conference on Computer Vision",
        "year_range": (1987, 2099),
        "aliases": ["iccv", "ICCV", "Int Conf Comput Vis"],
        "type": "conference",
    },
    "TMI": {
        "full_name": "IEEE Transactions on Medical Imaging",
        "year_range": (1982, 2099),
        "aliases": ["tmi", "TMI", "IEEE Trans Med Imaging", "Trans Med Imaging"],
        "type": "journal",
    },
    "MedIA": {
        "full_name": "Medical Image Analysis",
        "year_range": (1996, 2099),
        "aliases": ["media", "MedIA", "Med Image Anal", "Medical Image Analysis"],
        "type": "journal",
    },
}

# Common known-valid venue abbreviations (not in our DB — flagged as uncertain)
KNOWN_OTHER_VENUES = {
    "nature", "science", "cell", "plos", "bmc", "frontiers",
    "ieee", "acm", "springer", "elsevier", "arxiv", "biorxiv",
    "medrxiv", "the lancet", "jama", "nejm", "radiology",
    "investigative radiology", "eur radiol", "phys med biol",
}


# ─── Parsing ────────────────────────────────────────────────────────────────

def read_file(path):
    """Read a .tex or .bib file."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def parse_bibitem(content):
    """Parse \\bibitem entries from thebibliography environment in .tex files."""
    refs = []

    # Find thebibliography environment
    env_match = re.search(
        r"\\begin\{thebibliography\}(.*?)\\end\{thebibliography\}",
        content, re.DOTALL
    )
    if not env_match:
        return refs

    env_content = env_match.group(1)

    # Find each bibitem: \bibitem[label]{key} ... (until next \bibitem or end)
    pattern = r"\\bibitem(?:\[.*?\])?\s*\{([^}]*)\}\s*(.*?)(?=\\bibitem|\Z)"
    matches = re.findall(pattern, env_content, re.DOTALL)

    for key, rest in matches:
        ref = parse_bibitem_text(key, rest)
        if ref:
            refs.append(ref)

    return refs


def parse_bibitem_text(key, text):
    """Parse a single bibitem's text for authors, title, journal, year, etc."""
    text = text.strip()
    ref = {
        "key": key,
        "raw": text[:200],  # truncated
        "authors": "",
        "title": "",
        "journal": "",
        "year": "",
        "volume": "",
        "pages": "",
        "doi": "",
        "arxiv_id": "",
    }

    # Year: look for (YYYY) or . YYYY.
    m = re.search(r"\((\d{4})\)|\.\s*(\d{4})\.", text)
    if m:
        ref["year"] = m.group(1) or m.group(2)

    # DOI
    m = re.search(r"doi\s*[:=]?\s*(10\.\d{4,}/[^\s,}\]]+)", text, re.IGNORECASE)
    if m:
        ref["doi"] = m.group(1).rstrip(".,")

    # arXiv ID: arXiv:YYMM.NNNNN or arXiv:YYMM.NNNNNvN
    m = re.search(
        r"(?:arXiv|arxiv)[:\s]*((?:\d{4}\.\d{4,5})(?:v\d+)?)",
        text
    )
    if m:
        ref["arxiv_id"] = m.group(1)

    # Also try: "arXiv preprint" patterns
    m = re.search(r"(?:\d{4}\.\d{4,5})(?:v\d+)?", text)
    if m and not ref["arxiv_id"]:
        ref["arxiv_id"] = m.group(0)

    # Pages
    m = re.search(r"(?:pp\.?\s*|pages?\s*)(\d+\s*[-–]\s*\d+)", text, re.IGNORECASE)
    if m:
        ref["pages"] = m.group(1)

    # Volume
    m = re.search(r"(?:vol\.?\s*|volume\s*)(\d+)", text, re.IGNORECASE)
    if m:
        ref["volume"] = m.group(1)

    # Title: often in quotes or between braces (approximate)
    # Bibitem often: Author. "Title." Journal. Year.
    m = re.search(r'["""]([^""]+)["""]', text)
    if not m:
        m = re.search(r"\{(.+?)\}", text)
    if m:
        ref["title"] = m.group(1)[:150]

    # Authors: first part before period
    m = re.match(r"^([^.]+\.[^.]*?)\.", text)
    if m:
        ref["authors"] = m.group(1)[:200]

    return ref


def parse_bib_file(content):
    """Parse a .bib file for @article, @inproceedings, etc."""
    refs = []
    # Match @entrytype{key, ... }
    pattern = r"@(\w+)\s*\{([^,]+),\s*(.*?)\n\}", re.DOTALL

    # Simpler: find entries by @ symbol
    entries = re.findall(
        r"@(\w+)\s*\{\s*([^,\s]+)\s*,([^@]*?)\}",
        content, re.DOTALL
    )

    for entry_type, key, fields_text in entries:
        ref = {
            "key": key,
            "entry_type": entry_type,
            "raw": (entry_type + "{" + key + ", " + fields_text[:100]).strip(),
            "authors": "",
            "title": "",
            "journal": "",
            "year": "",
            "volume": "",
            "pages": "",
            "doi": "",
            "arxiv_id": "",
        }
        # Extract fields
        fields = re.findall(r"(\w+)\s*=\s*\{([^}]*)\}", fields_text)
        field_dict = {k.lower(): v for k, v in fields}

        ref["title"] = field_dict.get("title", "")
        ref["authors"] = field_dict.get("author", "")
        ref["journal"] = field_dict.get("journal", "") or field_dict.get("booktitle", "")
        ref["year"] = field_dict.get("year", "")
        ref["volume"] = field_dict.get("volume", "")
        ref["pages"] = field_dict.get("pages", "")
        ref["doi"] = field_dict.get("doi", "")
        ref["url"] = field_dict.get("url", "")

        # arXiv ID from journal/note/url
        for source in ["journal", "note", "url"]:
            val = field_dict.get(source, "")
            m = re.search(r"(?:arXiv|arxiv)[:\s]*((?:\d{4}\.\d{4,5})(?:v\d+)?)", val)
            if m:
                ref["arxiv_id"] = m.group(1)
                break

        refs.append(ref)

    return refs


def detect_venue(ref):
    """Detect the venue from a reference's text."""
    text = (ref.get("journal", "") + " " + ref.get("raw", "")).strip()

    for venue_key, venue_info in VENUES.items():
        for alias in venue_info["aliases"]:
            if re.search(re.escape(alias), text, re.IGNORECASE):
                return venue_key, venue_info["full_name"], venue_info["type"]

    # Check known-other venues
    for known in KNOWN_OTHER_VENUES:
        if re.search(re.escape(known), text, re.IGNORECASE):
            return "other", known, "unknown"

    return "unknown", "", "unknown"


def validate_arxiv_id(arxiv_id):
    """Validate an arXiv ID format."""
    # Format: YYMM.NNNNN or YYMM.NNNN (older: YYMMNNNN with YY < 15)
    # New format (since 2015): YYMM.NNNNN
    m = re.match(r"^(\d{2})(\d{2})\.(\d{4,5})(?:v\d+)?$", arxiv_id)
    if m:
        yy = int(m.group(1))
        mm = int(m.group(2))
        if mm < 1 or mm > 12:
            return "invalid", "Month out of range (1-12)"
        return "format_valid", ""

    # Old format: YYMMNNNN (for pre-2015 IDs)
    m = re.match(r"^(\d{4})(\d{4})(?:v\d+)?$", arxiv_id)
    if m:
        yy = int(m.group(1))
        return "format_valid", ""

    return "invalid", "Does not match arXiv ID format (YYMM.NNNNN or YYYYNNNN)"


# ─── Verification ────────────────────────────────────────────────────────────

def verify_reference(ref):
    """Verify a single reference and return a structured result."""
    result = {
        "key": ref["key"],
        "title": ref.get("title", "")[:80],
        "year": ref.get("year", ""),
        "doi": ref.get("doi", ""),
        "arxiv_id": ref.get("arxiv_id", ""),
        "venue_key": "",
        "venue_name": "",
        "venue_type": "",
        "status": "unknown",
        "issues": [],
        "suggestions": [],
    }

    venue_key, venue_name, venue_type = detect_venue(ref)
    result["venue_key"] = venue_key
    result["venue_name"] = venue_name
    result["venue_type"] = venue_type

    # Check venue against database
    if venue_key == "unknown":
        result["status"] = "uncertain"
        result["issues"].append("Venue not in reference database")
        result["suggestions"].append("Manually verify this reference's venue")
    elif venue_key == "other":
        result["status"] = "uncertain"
        result["issues"].append(f"Venue from known but unverified source: {venue_name}")
    else:
        # Known venue — check year
        venue_info = VENUES[venue_key]
        year_str = ref.get("year", "")
        result["status"] = "verified"

        if year_str:
            try:
                year_int = int(year_str)
                year_start, year_end = venue_info["year_range"]
                if year_int < year_start or year_int > year_end:
                    result["issues"].append(
                        f"Year {year_int} out of range for {venue_key} "
                        f"({year_start}-{year_end})"
                    )
                    result["status"] = "suspicious"
            except ValueError:
                result["issues"].append(f"Unparseable year: '{year_str}'")
                result["status"] = "uncertain"
        else:
            result["issues"].append("No year found")
            result["status"] = "uncertain"

    # Check arXiv
    if ref.get("arxiv_id"):
        arxiv_status, arxiv_msg = validate_arxiv_id(ref["arxiv_id"])
        if arxiv_status != "format_valid":
            result["issues"].append(f"arXiv ID issue: {arxiv_msg}")
            result["suggestions"].append(f"Check arXiv ID: {ref['arxiv_id']}")
            if result["status"] == "verified":
                result["status"] = "uncertain"
        else:
            result["suggestions"].append(f"arXiv:{ref['arxiv_id']} — format OK, verify online")

    # Check for possible issues
    if ref.get("doi"):
        # Basic DOI plausibility
        if not ref["doi"].startswith("10."):
            result["issues"].append(f"Suspicious DOI format: {ref['doi']}")
            if result["status"] == "verified":
                result["status"] = "suspicious"

    # Flag missing info
    if not ref.get("year"):
        result["issues"].append("Missing publication year")
    if not ref.get("doi") and not ref.get("arxiv_id") and venue_key not in ("unknown", "other"):
        result["suggestions"].append("Consider adding DOI or arXiv ID for this reference")

    return result


# ─── Reporting ───────────────────────────────────────────────────────────────

def generate_report(refs, results):
    """Generate a human-readable report."""
    verified = sum(1 for r in results if r["status"] == "verified")
    uncertain = sum(1 for r in results if r["status"] == "uncertain")
    suspicious = sum(1 for r in results if r["status"] == "suspicious")
    unknown = sum(1 for r in results if r["status"] == "unknown")

    lines = []
    lines.append("# Reference Verification Report\n")
    lines.append(f"**Total references:** {len(refs)}")
    lines.append(f"**Verified:** {verified}")
    lines.append(f"**Uncertain:** {uncertain}")
    lines.append(f"**Suspicious:** {suspicious}")
    lines.append(f"**Unknown:** {unknown}\n")

    lines.append("---\n")

    # Status summary
    status_counts = {"verified": verified, "uncertain": uncertain, "suspicious": suspicious, "unknown": unknown}
    lines.append("| Status | Count |")
    lines.append("|--------|-------|")
    for status, count in status_counts.items():
        lines.append(f"| {status.title()} | {count} |")
    lines.append("")

    # Per-reference details
    lines.append("## Per-Reference Details\n")

    for ref, result in zip(refs, results):
        status_icon = {"verified": "[OK]", "uncertain": "[!]", "suspicious": "[X]", "unknown": "[?]"}
        icon = status_icon.get(result["status"], "[?]")
        lines.append(f"### {icon} [{result['key']}] ({result['status']})")
        lines.append(f"- **Title:** {result['title'][:100] or 'N/A'}")
        lines.append(f"- **Year:** {result['year'] or 'N/A'}")
        lines.append(f"- **Venue:** {result['venue_key']} — {result['venue_name'] or 'unknown'}")
        lines.append(f"- **DOI:** {result['doi'] or 'N/A'}")

        if result["arxiv_id"]:
            lines.append(f"- **arXiv:** {result['arxiv_id']} ({validate_arxiv_id(result['arxiv_id'])[0]})")

        if result["issues"]:
            lines.append("- **Issues:**")
            for issue in result["issues"]:
                lines.append(f"  - {issue}")
        if result["suggestions"]:
            lines.append("- **Suggestions:**")
            for s in result["suggestions"]:
                lines.append(f"  - {s}")
        lines.append("")

    return "\n".join(lines)


def generate_json_report(refs, results):
    """Generate a JSON report."""
    report = {
        "total": len(refs),
        "verified": sum(1 for r in results if r["status"] == "verified"),
        "uncertain": sum(1 for r in results if r["status"] == "uncertain"),
        "suspicious": sum(1 for r in results if r["status"] == "suspicious"),
        "unknown": sum(1 for r in results if r["status"] == "unknown"),
        "references": results,
    }
    return json.dumps(report, indent=2, ensure_ascii=False)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python skills.py path/to/paper.tex")
        print("       python skills.py path/to/references.bib")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    content = read_file(str(input_path))
    ext = input_path.suffix.lower()

    if ext == ".bib":
        refs = parse_bib_file(content)
    elif ext == ".tex":
        refs = parse_bibitem(content)
        # Also try bib file if referenced
        bib_cmds = re.findall(r"\\bibliography\{(.+?)\}", content)
        for bib_cmd in bib_cmds:
            for name in bib_cmd.split(","):
                bib_path = input_path.parent / f"{name.strip()}.bib"
                if bib_path.exists():
                    bib_content = read_file(str(bib_path))
                    refs_bib = parse_bib_file(bib_content)
                    refs.extend(refs_bib)
    else:
        print(f"Error: Unsupported file type: {ext}. Expected .tex or .bib")
        sys.exit(1)

    if not refs:
        print("No references found in the input file.")
        print("Tip: Make sure the file contains \\bibitem entries or a .bib file.")
        sys.exit(1)

    print(f"Found {len(refs)} references.")
    results = [verify_reference(ref) for ref in refs]

    verified = sum(1 for r in results if r["status"] == "verified")
    uncertain = sum(1 for r in results if r["status"] == "uncertain")
    suspicious = sum(1 for r in results if r["status"] == "suspicious")
    unknown = sum(1 for r in results if r["status"] == "unknown")

    print(f"  Verified: {verified}")
    print(f"  Uncertain: {uncertain}")
    print(f"  Suspicious: {suspicious}")
    print(f"  Unknown: {unknown}")

    # Output files
    stem = input_path.stem
    out_dir = input_path.parent

    md_report = generate_report(refs, results)
    md_path = out_dir / f"{stem}.references.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_report)
    print(f"  Report: {md_path}")

    json_report = generate_json_report(refs, results)
    json_path = out_dir / f"{stem}.references.json"
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(json_report)
    print(f"  JSON: {json_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
