#!/usr/bin/env python3
"""
reviewer-simulator: Simulate MICCAI reviewer feedback on a LaTeX paper.

Usage:
    python skills.py path/to/paper.tex

Outputs:
    - paper.reviewer.fixed.tex   (auto-applied simple fixes)
    - paper.reviewer.report.md   (structured review report)
    - paper.reviewer.diff.md     (diff of changes made)
"""

import re
import os
import sys
import json
import difflib
from pathlib import Path


# ─── Constants ───────────────────────────────────────────────────────────────

MICCAI_CRITERIA = [
    "novelty",
    "technical_soundness",
    "experimental_rigor",
    "clarity",
    "reproducibility",
]

CRITERION_LABELS = {
    "novelty": "Novelty (1-5)",
    "technical_soundness": "Technical Soundness (1-5)",
    "experimental_rigor": "Experimental Rigor (1-5)",
    "clarity": "Clarity (1-5)",
    "reproducibility": "Reproducibility (1-5)",
}

# Common patterns for auto-fixes
TYPO_MAP = {
    r"(?<!\w)teh(?!\w)": "the",
    r"(?<!\w)alot(?!\w)": "a lot",
    r"(?<!\w)occured(?!\w)": "occurred",
    r"(?<!\w)recieve(?!\w)": "receive",
    r"(?<!\w)acheive(?!\w)": "achieve",
    r"(?<!\w)becuase(?!\w)": "because",
    r"(?<!\w)begining(?!\w)": "beginning",
    r"(?<!\w)beleive(?!\w)": "believe",
    r"(?<!\w)calender(?!\w)": "calendar",
    r"(?<!\w)comming(?!\w)": "coming",
    r"(?<!\w)definately(?!\w)": "definitely",
    r"(?<!\w)desparate(?!\w)": "desperate",
    r"(?<!\w)embarass(?!\w)": "embarrass",
    r"(?<!\w)enviroment(?!\w)": "environment",
    r"(?<!\w)existance(?!\w)": "existence",
    r"(?<!\w)extremly(?!\w)": "extremely",
    r"(?<!\w)goverment(?!\w)": "government",
    r"(?<!\w)happend(?!\w)": "happened",
    r"(?<!\w)independant(?!\w)": "independent",
    r"(?<!\w)immediatly(?!\w)": "immediately",
    r"(?<!\w)neccessary(?!\w)": "necessary",
    r"(?<!\w)occassion(?!\w)": "occasion",
    r"(?<!\w)priviledge(?!\w)": "privilege",
    r"(?<!\w)seperate(?!\w)": "separate",
    r"(?<!\w)sergent(?!\w)": "sergeant",
    r"(?<!\w)succesful(?!\w)": "successful",
    r"(?<!\w)surprize(?!\w)": "surprise",
    r"(?<!\w)thier(?!\w)": "their",
    r"(?<!\w)wierd(?!\w)": "weird",
    r"(?<!\w)writen(?!\w)": "written",
    r"(?<!\w)usefull(?!\w)": "useful",
    r"(?<!\w)carefull(?!\w)": "careful",
    r"(?<!\w)beautifull(?!\w)": "beautiful",
    r"(?<!\w)sucess(?!\w)": "success",
    r"(?<!\w)propogate(?!\w)": "propagate",
    r"(?<!\w)preceed(?!\w)": "precede",
    r"(?<!\w)proceedure(?!\w)": "procedure",
}

GRAMMAR_PATTERNS = [
    # "a" -> "an" before vowels
    (r"\ba (\b[aeiouAEIOU][a-z]*)", lambda m: f"an {m.group(1)}"),
    # "its" vs "it's" — common misuse
    (r"\bits'(?!\w)", "its"),
    # Double spaces
    (r"  +", " "),
    # Missing space after period (end of sentence)
    (r"\.([A-Z])", lambda m: f". {m.group(1)}"),
    # "i.e." no space variants
    (r"i\.e\.,", "i.e.,"),
    (r"e\.g\.,", "e.g.,"),
    # "et al." -> properly formatted
    (r"\bet al\b", "et al."),
]

FORMATTING_FIXES = [
    # Unmatched braces
    (r"\\textbf\{([^}]*)\}", lambda m: f"\\\\textbf{{{m.group(1)}}}"),
    # Section headings without proper spacing
    (r"\\section\*?\{", r"\\section{"),
    # Inline math that should have proper spacing
    (r"\\cite\s*\{", r"\\cite{"),
    (r"\\ref\s*\{", r"\\ref{"),
    (r"\\label\s*\{", r"\\label{"),
]


# ─── Review Templates ────────────────────────────────────────────────────────

REVIEWER_PERSONAS = [
    {
        "name": "Reviewer 1",
        "style": "constructive",
        "bias": {"novelty": -0.3, "technical_soundness": 0.2, "experimental_rigor": 0.4},
    },
    {
        "name": "Reviewer 2",
        "style": "critical",
        "bias": {"novelty": 0.2, "technical_soundness": -0.4, "experimental_rigor": -0.3},
    },
    {
        "name": "Reviewer 3",
        "style": "balanced",
        "bias": {"novelty": 0.0, "technical_soundness": 0.0, "experimental_rigor": 0.0},
    },
]


# ─── Paper Analysis ──────────────────────────────────────────────────────────

def read_tex(path):
    """Read a .tex file and return its content as a string."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def extract_sections(content):
    """Extract section headings and their line numbers."""
    sections = []
    for i, line in enumerate(content.split("\n"), 1):
        m = re.match(r"\\section\*?\{(.+?)\}", line)
        if m:
            sections.append((i, m.group(1)))
    return sections


def extract_abstract(content):
    """Extract the abstract content."""
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", content, re.DOTALL)
    if m:
        return m.group(1).strip()
    # fallback: \abstract{...}
    m = re.search(r"\\abstract\{(.*?)\}", content, re.DOTALL)
    return m.group(1).strip() if m else ""


def count_words(content):
    """Count words in LaTeX content (strips commands first)."""
    stripped = re.sub(r"\\(?:[a-zA-Z]+|.)", " ", content)
    stripped = re.sub(r"\{|\}", " ", stripped)
    stripped = re.sub(r"\\\[.*?\\\]", " ", stripped, flags=re.DOTALL)
    stripped = re.sub(r"\$.*?\$", " ", stripped)
    return len(stripped.split())


def count_references(content):
    """Count bib entries or \\bibitem entries."""
    bibitems = re.findall(r"\\bibitem\s*(\[.*?\])?\s*\{.*?\}", content)
    if bibitems:
        return len(bibitems)
    # Check for .bib file usage
    bibs = re.findall(r"\\bibliography\{(.+?)\}", content)
    # Check for thebibliography
    env = re.findall(r"\\begin\{thebibliography\}(.*?)\\end\{thebibliography\}", content, re.DOTALL)
    if env:
        return len(re.findall(r"\\bibitem", env[0]))
    return len(bibs)  # can't count actual refs if external bib


def count_figures(content):
    """Count figures and tables."""
    figs = len(re.findall(r"\\begin\{figure\}", content))
    tables = len(re.findall(r"\\begin\{table\}", content))
    return figs, tables


def count_citations(content):
    """Count unique citations."""
    cites = re.findall(r"\\cite(?:t|p|author)?\{([^}]+)\}", content)
    unique = set()
    for c in cites:
        for ref in c.split(","):
            unique.add(ref.strip())
    return len(unique)


def detect_baselines(content):
    """Detect mentioned baselines."""
    baselines = []
    patterns = [
        r"(?:compare|baseline|benchmark|state-of-the-art|SOTA)",
        r"\\cite.*?(?:ResNet|VGG|DenseNet|UNet|ViT|CNN|Transformer|EfficientNet)",
        r"(?:ablation)",
    ]
    for p in patterns:
        if re.search(p, content, re.IGNORECASE):
            baselines.append(p)
    return baselines


def count_experiments(content):
    """Count datasets mentioned and experiment sections."""
    datasets = re.findall(r"(?:dataset|benchmark|corpus)[^}]*\{(.+?)\}", content, re.IGNORECASE)
    named_datasets = []
    for d in datasets:
        # attempt to extract dataset name
        m = re.search(r"([A-Z][a-zA-Z0-9]*(?:-[A-Z][a-zA-Z0-9]*)*)", d)
        if m:
            named_datasets.append(m.group(1))
    return named_datasets


def extract_claims(content):
    """Extract contribution/claim statements."""
    claims = []
    # Look in \contributions or \highlight or similar
    contrib_section = re.search(
        r"\\(?:contributions?|highlights?|contributions)\s*\{(.*?)\}",
        content, re.DOTALL
    )
    if contrib_section:
        items = re.findall(r"\\item\s+(.*?)(?:\\item|$)", contrib_section.group(1))
        claims.extend(items)
    # If declared in text
    claim_patterns = [
        r"(?:contribute|propose|introduce|present|develop)\s+(.+?)(?:\.|,)",
        r"(?:first|novel|new)\s+(.+?)(?:\.|,)",
        r"(?:to our knowledge|to the best of our knowledge)[^.]*\.",
    ]
    for p in claim_patterns:
        matches = re.findall(p, content, re.IGNORECASE)
        claims.extend(matches[:5])
    return claims[:10]  # cap


def has_code_link(content):
    """Check if the paper mentions code availability."""
    return bool(re.search(r"(?:code|implementation).*(?:github|available|public|open.?source|https?)", content, re.IGNORECASE))


def has_hyperparams(content):
    """Check if hyperparameters are reported."""
    return bool(re.search(r"(?:hyperparameter|learning.?rate|batch.?size|epoch|optimizer|weight.?decay)", content, re.IGNORECASE))


def has_statistical_tests(content):
    """Check for statistical significance testing."""
    return bool(re.search(r"(?:p-value|p <|p\s*=|t-test|paired|bootstra|confidence interval|statistical(?:ly)?\s+(?:signif|test))", content, re.IGNORECASE))


# ─── Auto-fixes ──────────────────────────────────────────────────────────────

def apply_typo_fixes(content):
    """Apply typo fixes using regex substitution."""
    changes = []
    fixed = content
    for pattern, replacement in TYPO_MAP.items():
        new_content = re.sub(pattern, replacement, fixed, flags=re.IGNORECASE)
        if new_content != fixed:
            changes.append(f"Typo fix: '{pattern}' -> '{replacement}'")
            fixed = new_content
    return fixed, changes


def apply_grammar_fixes(content):
    """Apply grammar fixes."""
    changes = []
    fixed = content
    for pattern, replacement in GRAMMAR_PATTERNS:
        new_content = re.sub(pattern, replacement, fixed)
        if new_content != fixed:
            changes.append(f"Grammar fix: pattern '{pattern}'")
            fixed = new_content
    return fixed, changes


def apply_formatting_fixes(content):
    """Apply formatting fixes."""
    changes = []
    fixed = content
    for pattern, replacement in FORMATTING_FIXES:
        new_content = re.sub(pattern, replacement, fixed)
        if new_content != fixed:
            changes.append(f"Formatting fix: pattern '{pattern}'")
            fixed = new_content
    return fixed, changes


def auto_fix(content):
    """Run all auto-fixes and return (fixed_text, list_of_changes)."""
    all_changes = []
    content, typo_changes = apply_typo_fixes(content)
    all_changes.extend(typo_changes)
    content, grammar_changes = apply_grammar_fixes(content)
    all_changes.extend(grammar_changes)
    content, fmt_changes = apply_formatting_fixes(content)
    all_changes.extend(fmt_changes)
    return content, all_changes


# ─── Reviewer Score Simulation ───────────────────────────────────────────────

def compute_scores(stats, reviewer):
    """Compute scores for each criterion based on paper stats and reviewer bias."""
    scores = {}

    # Novelty: claims, baselines, uniqueness
    base_novelty = 3.0
    if len(stats["claims"]) >= 3:
        base_novelty += 0.5
    if stats["has_code"]:
        base_novelty += 0.3
    if stats["num_datasets"] >= 2:
        base_novelty += 0.3
    scores["novelty"] = max(1, min(5, round(base_novelty + reviewer["bias"]["novelty"])))

    # Technical soundness: baselines, datasets, structure
    base_tech = 3.0
    if stats["num_datasets"] >= 2:
        base_tech += 0.5
    if stats["num_sections"] >= 5:
        base_tech += 0.3
    if stats["has_baselines"]:
        base_tech += 0.3
    scores["technical_soundness"] = max(1, min(5, round(base_tech + reviewer["bias"]["technical_soundness"])))

    # Experimental rigor: datasets, baselines, statistical tests, ablations
    base_exp = 3.0
    if stats["num_datasets"] >= 3:
        base_exp += 0.5
    elif stats["num_datasets"] >= 2:
        base_exp += 0.2
    if stats["has_baselines"]:
        base_exp += 0.3
    if stats["has_stats_tests"]:
        base_exp += 0.5
    if stats["num_figures"] + stats["num_tables"] >= 6:
        base_exp += 0.3
    scores["experimental_rigor"] = max(1, min(5, round(base_exp + reviewer["bias"]["experimental_rigor"])))

    # Clarity: word count, sections, abstract quality
    base_clarity = 3.0
    if 4000 <= stats["word_count"] <= 12000:
        base_clarity += 0.3
    if stats["num_sections"] >= 5:
        base_clarity += 0.3
    if len(stats["abstract"]) > 100:
        base_clarity += 0.3
    scores["clarity"] = max(1, min(5, round(base_clarity)))

    # Reproducibility: code link, hyperparams
    base_reprod = 3.0
    if stats["has_code"]:
        base_reprod += 1.0
    if stats["has_hyperparams"]:
        base_reprod += 0.5
    scores["reproducibility"] = max(1, min(5, round(base_reprod)))

    return scores


def generate_reviewer_comments(scores, stats, reviewer):
    """Generate structured comments for a single reviewer."""
    comments = []
    strengths = []
    weaknesses = []

    def _criterion_feedback(criterion, score):
        if score >= 4:
            return f"Good {criterion.replace('_', ' ')}."
        elif score >= 3:
            return f"Adequate {criterion.replace('_', ' ')} but could be improved."
        else:
            return f"Weak {criterion.replace('_', ' ')} — needs significant improvement."

    for criterion in MICCAI_CRITERIA:
        score = scores[criterion]
        fb = _criterion_feedback(criterion, score)
        if score >= 4:
            strengths.append(fb)
        elif score <= 2:
            weaknesses.append(fb)

    # Generate concrete issues based on stats
    if not stats["has_code"]:
        weaknesses.append("No code/data availability link provided — crucial for reproducibility.")
    if not stats["has_hyperparams"]:
        weaknesses.append("Hyperparameters are not reported — training details are missing.")
    if not stats["has_stats_tests"]:
        weaknesses.append("No statistical significance testing reported.")
    if stats["num_datasets"] == 0:
        weaknesses.append("No datasets explicitly mentioned — experimentation appears absent.")
    elif stats["num_datasets"] == 1:
        weaknesses.append("Only one dataset tested — generalization is questionable.")
    if not stats["has_baselines"]:
        weaknesses.append("No baselines or comparisons mentioned.")
    if stats["num_figures"] + stats["num_tables"] < 3:
        weaknesses.append("Very few figures/tables — results are hard to evaluate.")

    if reviewer["style"] == "constructive":
        tone_prefix = "I appreciate the effort. "
        tone_suffix = " I believe with revisions this work could be strengthened significantly."
    elif reviewer["style"] == "critical":
        tone_prefix = ""
        tone_suffix = " The paper has fundamental issues that need to be addressed before acceptance."
    else:
        tone_prefix = "The paper addresses an interesting problem. "
        tone_suffix = " With appropriate revisions, it could be a solid contribution."

    summary = tone_prefix + tone_suffix
    overall_score = round(sum(scores.values()) / len(scores), 1)

    return {
        "reviewer": reviewer["name"],
        "style": reviewer["style"],
        "scores": scores,
        "overall": overall_score,
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "questions": [
            f"How does the proposed method generalize across different patient populations?",
            f"Can the authors provide more ablation studies on {stats.get('claims', ['the method'])[0] if stats.get('claims') else 'key components'}?",
            f"What are the failure cases of the proposed approach?",
        ],
        "decision": "Weak Accept" if overall_score >= 3.5 else "Borderline" if overall_score >= 2.5 else "Weak Reject",
    }


def generate_revision_suggestions(scores, stats):
    """Generate specific revision suggestions based on analysis."""
    suggestions = []

    if scores.get("experimental_rigor", 3) <= 2:
        if stats["num_datasets"] <= 1:
            suggestions.append("Add at least one more external dataset to demonstrate generalization across domains.")
        if not stats["has_baselines"]:
            suggestions.append("Include comparisons with at least 3 state-of-the-art baselines.")
        if not stats["has_stats_tests"]:
            suggestions.append("Add statistical significance testing (e.g., paired t-test, McNemar's test) for main results.")

    if scores.get("reproducibility", 3) <= 2:
        if not stats["has_code"]:
            suggestions.append("Add a 'Code Availability' statement with a GitHub link. If private for now, note 'available upon request'.")
        if not stats["has_hyperparams"]:
            suggestions.append("Report all hyperparameters: learning rate, batch size, optimizer, weight decay, number of epochs, and GPU specs.")

    if scores.get("novelty", 3) <= 2:
        suggestions.append("More clearly articulate the novelty — differentiate from existing methods with a comparison table.")
        suggestions.append("Consider adding a 'Comparison to Prior Work' subsection in the method.")

    if scores.get("clarity", 3) <= 2:
        suggestions.append("Improve overall clarity: add a high-level figure explaining the pipeline, and ensure each section motivates the next.")

    return suggestions


# ─── Reporting ───────────────────────────────────────────────────────────────

def compute_stats(content):
    """Compute paper statistics from content."""
    sections = extract_sections(content)
    abstract = extract_abstract(content)
    word_count = count_words(content)
    refs = count_references(content)
    num_figures, num_tables = count_figures(content)
    num_citations = count_citations(content)
    baselines = detect_baselines(content)
    datasets = count_experiments(content)
    claims = extract_claims(content)

    return {
        "sections": sections,
        "abstract": abstract,
        "word_count": word_count,
        "num_references": refs,
        "num_figures": num_figures,
        "num_tables": num_tables,
        "num_citations": num_citations,
        "num_sections": len(sections),
        "has_baselines": len(baselines) > 0,
        "num_datasets": len(datasets),
        "datasets": datasets,
        "has_code": has_code_link(content),
        "has_hyperparams": has_hyperparams(content),
        "has_stats_tests": has_statistical_tests(content),
        "claims": claims,
    }


def generate_report(stats, reviewers_output, revision_suggestions, diff_lines):
    """Generate the full review report as markdown."""
    lines = []
    lines.append("# Reviewer Simulation Report\n")
    lines.append(f"**Paper Statistics:**\n")
    lines.append(f"- Word count: {stats['word_count']}")
    lines.append(f"- Sections: {stats['num_sections']}")
    lines.append(f"- Figures: {stats['num_figures']}, Tables: {stats['num_tables']}")
    lines.append(f"- References: {stats['num_references']}")
    lines.append(f"- Datasets mentioned: {stats['num_datasets']} ({', '.join(stats['datasets']) if stats['datasets'] else 'none'})")
    lines.append(f"- Claims extracted: {len(stats['claims'])}")
    lines.append(f"- Code availability: {'Yes' if stats['has_code'] else 'No'}")
    lines.append(f"- Hyperparameters reported: {'Yes' if stats['has_hyperparams'] else 'No'}")
    lines.append(f"- Statistical tests: {'Yes' if stats['has_stats_tests'] else 'No'}")
    lines.append("")

    lines.append("---\n")

    # Per-reviewer reports
    all_scores = []
    for review in reviewers_output:
        lines.append(f"## {review['reviewer']} (Style: {review['style']})")
        lines.append(f"**Decision:** {review['decision']}")
        lines.append(f"**Overall Score:** {review['overall']}/5.0\n")

        lines.append("### Scores")
        for criterion in MICCAI_CRITERIA:
            score = review['scores'][criterion]
            bar = "#" * score + "-" * (5 - score)
            lines.append(f"- {CRITERION_LABELS[criterion]}: {score}/5 [{bar}]")
        lines.append("")

        lines.append("### Summary")
        lines.append(review['summary'])
        lines.append("")

        if review['strengths']:
            lines.append("### Strengths")
            for s in review['strengths']:
                lines.append(f"- {s}")
            lines.append("")

        if review['weaknesses']:
            lines.append("### Weaknesses")
            for w in review['weaknesses']:
                lines.append(f"- {w}")
            lines.append("")

        if review['questions']:
            lines.append("### Questions for Authors")
            for q in review['questions']:
                lines.append(f"- {q}")
            lines.append("")

        all_scores.append(review['overall'])

    lines.append("---\n")
    lines.append("## Aggregated Scores\n")
    for i, criterion in enumerate(MICCAI_CRITERIA):
        vals = [r['scores'][criterion] for r in reviewers_output]
        avg = sum(vals) / len(vals)
        lines.append(f"- {CRITERION_LABELS[criterion]}: {avg:.1f}/5.0")
    lines.append(f"\n**Average Overall:** {sum(all_scores)/len(all_scores):.1f}/5.0")
    lines.append("")

    # Revision suggestions
    lines.append("---\n")
    lines.append("## Revision Suggestions\n")
    for s in revision_suggestions:
        lines.append(f"- {s}")
    lines.append("")

    # Diff
    lines.append("---\n")
    lines.append("## Auto-Fixes Applied\n")
    if diff_lines:
        lines.append(f"```diff")
        for d in diff_lines:
            lines.append(d)
        lines.append("```")
    else:
        lines.append("No auto-fixes were needed or applied.")
    lines.append("")

    return "\n".join(lines)


def generate_diff(original, fixed, context=3):
    """Generate a diff between original and fixed text, returning diff lines."""
    original_lines = original.split("\n")
    fixed_lines = fixed.split("\n")
    diff = list(difflib.unified_diff(
        original_lines, fixed_lines,
        fromfile="original", tofile="fixed",
        n=context
    ))
    return diff


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python skills.py path/to/paper.tex")
        sys.exit(1)

    tex_path = Path(sys.argv[1])
    if not tex_path.exists():
        print(f"Error: File not found: {tex_path}")
        sys.exit(1)

    print(f"Reviewing: {tex_path}")

    # Read paper
    content = read_tex(str(tex_path))

    # Compute stats
    stats = compute_stats(content)
    print(f"  Word count: {stats['word_count']}")
    print(f"  Sections: {stats['num_sections']}")
    print(f"  Datasets: {stats['num_datasets']}")
    print(f"  Claims: {len(stats['claims'])}")

    # Auto-fix
    fixed_content, fix_changes = auto_fix(content)
    print(f"  Auto-fixes applied: {len(fix_changes)}")

    # Generate reviewer reports
    reviewers_output = []
    for reviewer_tpl in REVIEWER_PERSONAS:
        scores = compute_scores(stats, reviewer_tpl)
        report = generate_reviewer_comments(scores, stats, reviewer_tpl)
        reviewers_output.append(report)
        print(f"  {report['reviewer']}: {report['overall']}/5.0 ({report['decision']})")

    # Revision suggestions
    avg_scores = {}
    for criterion in MICCAI_CRITERIA:
        vals = [r['scores'][criterion] for r in reviewers_output]
        avg_scores[criterion] = sum(vals) / len(vals)
    revision_suggestions = generate_revision_suggestions(avg_scores, stats)

    # Diff
    diff_lines = generate_diff(content, fixed_content)

    # Write outputs
    stem = tex_path.stem
    out_dir = tex_path.parent

    # Fixed TeX
    fixed_path = out_dir / f"{stem}.reviewer.fixed.tex"
    with open(fixed_path, "w", encoding="utf-8") as f:
        f.write(fixed_content)
    print(f"  Fixed TeX: {fixed_path}")

    # Diff
    diff_path = out_dir / f"{stem}.reviewer.diff.md"
    with open(diff_path, "w", encoding="utf-8") as f:
        f.write("# Diff of Auto-Fixes\n\n")
        if diff_lines:
            f.write("```diff\n")
            for d in diff_lines:
                f.write(d + "\n")
            f.write("```\n")
        else:
            f.write("No changes were made.\n")
    print(f"  Diff: {diff_path}")

    # Report
    report = generate_report(stats, reviewers_output, revision_suggestions, diff_lines)
    report_path = out_dir / f"{stem}.reviewer.report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Report: {report_path}")

    print("\nDone. Review complete.")


if __name__ == "__main__":
    main()
