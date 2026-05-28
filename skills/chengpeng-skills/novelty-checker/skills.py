#!/usr/bin/env python3

"""

novelty-checker: Analyze a LaTeX paper for novelty, contribution, and

experimental thoroughness.



Usage:

    python skills.py path/to/paper.tex



Output:

    - paper.novelty.report.md    (detailed report)

    - paper.novelty.report.json  (structured scores)

"""



import re

import os

import sys

import json

from pathlib import Path





# ─── Paper Parsing ───────────────────────────────────────────────────────────



def read_tex(path):

    """Read a .tex file."""

    with open(path, "r", encoding="utf-8", errors="replace") as f:

        return f.read()





def extract_sections(content):

    """Extract section headings."""

    sections = {}

    current_section = "preamble"

    sections[current_section] = []

    for line in content.split("\n"):

        m = re.match(r"\\(?:section|subsection)\*?\{(.+?)\}", line)

        if m:

            current_section = m.group(1).strip().lower()

            sections[current_section] = []

        else:

            sections[current_section].append(line)

    return sections





def extract_abstract(content):

    """Extract abstract text."""

    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", content, re.DOTALL)

    if m:

        return m.group(1).strip()

    m = re.search(r"\\abstract\{(.*?)\}", content, re.DOTALL)

    return m.group(1).strip() if m else ""





def extract_introduction(content):

    """Extract introduction section."""

    sections = extract_sections(content)

    for key in sections:

        if "introduction" in key:

            return "\n".join(sections[key])

    return ""





def extract_method(content):

    """Extract method section."""

    sections = extract_sections(content)

    for key in sections:

        if "method" in key or "approach" in key:

            return "\n".join(sections[key])

    return ""





def extract_experiments(content):

    """Extract experiments section."""

    sections = extract_sections(content)

    for key in sections:

        if "experiment" in key or "evaluation" in key or "result" in key:

            return "\n".join(sections[key])

    return ""





def extract_contributions(content):

    """Extract explicitly listed contributions."""

    contributions = []



    # Look for \contributions or enumerated lists in intro

    patterns = [

        r"\\(?:contributions?|highlights?|summary)\s*\{(.*?)\}",

        r"Our (?:main |primary |core )?contributions? are.*?(?:\n\n|\\section)",

        r"(?:summary|overview) of (?:our )?contributions.*?(?:\n\n|\\section)",

        r"In summary,.*?(?:contribute|propose|present).*?(?:\n\n|\\section)",

    ]

    for p in patterns:

        m = re.search(p, content, re.DOTALL | re.IGNORECASE)

        if m:

            text = m.group(0) if m.lastindex is None else m.group(1)

            # Extract bullet or enumerated items

            items = re.findall(r"\\item\s+(.*?)(?:\\item|\\end|$)", text, re.DOTALL)

            contributions.extend([i.strip() for i in items if i.strip()])

            # Also look for numbered: (1) (2) (3)

            items = re.findall(r"(?:\(?\d\)\s+|\(\d\))\s*([A-Z][^.]*\.)", text)

            contributions.extend([i.strip() for i in items if i.strip()])

            if contributions:

                break



    # Fallback: look for contribution keywords in intro

    if not contributions:

        intro = extract_introduction(content)

        cont_phrases = re.findall(

            r"(?:contribute|propose|introduce|present|develop)\s+(.+?)(?:\.|;|,\s+(?:and|which))",

            intro, re.IGNORECASE

        )

        contributions = [c.strip() for c in cont_phrases[:5]]



    return contributions[:10]





def count_words(text):

    """Count words in plain text."""

    stripped = re.sub(r"\\(?:[a-zA-Z]+|.)", " ", text)

    stripped = re.sub(r"\{|\}", " ", stripped)

    stripped = re.sub(r"\$.*?\$", " ", stripped)

    return len(stripped.split())





def extract_citations(text):

    """Extract citation keys from text."""

    cites = re.findall(r"\\cite(?:t|p|author)?\{([^}]+)\}", text)

    unique = set()

    for c in cites:

        for ref in c.split(","):

            unique.add(ref.strip())

    return unique





# ─── Baseline Detection ─────────────────────────────────────────────────────



KNOWN_BASELINES = {

    "CNN-based": ["CNN", "convolutional neural network", "ConvNet"],

    "ResNet": ["ResNet", "residual network", "ResNet50", "ResNet101", "ResNet152"],

    "VGG": ["VGG", "VGG16", "VGG19"],

    "DenseNet": ["DenseNet", "DenseNet121", "DenseNet169", "DenseNet201"],

    "UNet": ["UNet", "U-Net", "U-Net++", "Attention U-Net"],

    "ViT": ["ViT", "Vision Transformer", "vision transformer"],

    "Swin": ["Swin", "Swin Transformer", "swin transformer"],

    "Transformer": ["Transformer", "transformer"],

    "EfficientNet": ["EfficientNet", "EfficientNet-B", "EfficientNetV2"],

    "ResNeXt": ["ResNeXt", "ResNeXt-101"],

    "MobileNet": ["MobileNet", "MobileNetV2", "MobileNetV3"],

    "YOLO": ["YOLO", "YOLOv5", "YOLOv8"],

    "GAN": ["GAN", "generative adversarial", "CycleGAN", "StyleGAN"],

    "BERT": ["BERT", "BioBERT", "ClinicalBERT", "PubMedBERT"],

    "LSTM": ["LSTM", "long short-term memory", "BiLSTM", "GRU"],

    "CLIP": ["CLIP", "contrastive language-image"],

    "DINO": ["DINO", "DINOv2"],

    "MAE": ["MAE", "masked autoencoder"],

    "SAM": ["SAM", "Segment Anything"],

    "MedSAM": ["MedSAM"],

}





def detect_baselines(text):

    """Detect which baselines are mentioned in the text."""

    found = []

    for name, patterns in KNOWN_BASELINES.items():

        for pat in patterns:

            if re.search(re.escape(pat), text, re.IGNORECASE):

                found.append(name)

                break

    return found





def detect_comparisons(text):

    """Detect if the paper compares to baselines."""

    comp_patterns = [

        r"(?:compare|comparison|versus|vs\.?)\s+",

        r"(?:outperform|surpass|improve|better than|state-of-the-art|SOTA)",

        r"(?:baseline|benchmark)",

        r"(?:Table\s+\d+|Figure\s+\d+).*(?:compare|result|performance)",

    ]

    return any(re.search(p, text, re.IGNORECASE) for p in comp_patterns)





def detect_ablation(text):

    """Detect ablation studies."""

    patterns = [

        r"ablation",

        r"component.?wise",

        r"(?:without|w/o|w\.?\/?o\.?)\s",

        r"(?:contribution|importance|effect|impact)\s+(?:of|from)\s+(?:each|individual|different)",

        r"(?:remov|add|vary|modify)\s+(?:component|module|block|part)",

    ]

    return any(re.search(p, text, re.IGNORECASE) for p in patterns)





def count_datasets(text):

    """Count named datasets in the experiments section."""

    # Dataset name patterns: usually acronyms all-caps

    dataset_patterns = [

        r"(?:dataset|benchmark|corpus)\s+([A-Z][A-Za-z0-9-]*)",

        r"\b(ChestX-ray14|ChestX-ray|MIMIC-CXR|MIMIC|NIH|CXR|CheXpert|PadChest|RSNA|SIIM-ACR|VinDr|Open-i|IU-X-ray|COVID-19|CC-CCII|BIMCV|Pneumonia|Montgomery|Shenzhen|JSRT|Indiana)\b",

        r"on\s+(?:the\s+)?([A-Z][A-Za-z0-9]*)\s+(?:dataset|benchmark|corpus)",

    ]

    datasets = set()

    for pat in dataset_patterns:

        matches = re.findall(pat, text, re.IGNORECASE)

        for m in matches:

            datasets.add(m)

    return list(datasets)





def has_statistical_tests(text):

    """Check for statistical significance testing."""

    patterns = [

        r"(?:p-value|p\s*[<]\s*0[.\s]0?5)",

        r"(?:t-test|t test|paired\s+t)",

        r"(?:bootstra|bootstrapping)",

        r"(?:confidence\s+interval)",

        r"(?:statistical(?:ly)?\s+(?:signif|test))",

        r"(?:Wilcoxon|Mann-Whitney|ANOVA|Friedman)",

        r"(?:Cohen|kappa|Fleiss|ICC)",

        r"(?:McNemar|Chi-square|chi.squared)",

    ]

    return any(re.search(p, text, re.IGNORECASE) for p in patterns)





def has_code_link(text):

    """Check for code availability."""

    patterns = [

        r"(?:code|implementation).*(?:github|available|public|open.?source|https?://)",

        r"(?:github\.com|gitlab\.com)",

        r"(?:https?://github)",

        r"(?:code\s+(?:will\s+be\s+|is\s+)available)",

    ]

    return any(re.search(p, text, re.IGNORECASE) for p in patterns)





def has_hyperparams(text):

    """Check if hyperparameters are reported."""

    patterns = [

        r"(?:learning.?rate|lr|batch.?size|epoch|optimizer|weight.?decay|dropout|momentum)",

        r"(?:learning.rate|learning_rate|learning-rate)",

        r"(?:batch.size|batch_size|batch-size)",

    ]

    return any(re.search(p, text, re.IGNORECASE) for p in patterns)





def has_limitations(text):

    """Check if the paper discusses limitations."""

    sections = extract_sections(text)

    for key in sections:

        if "limitation" in key or "discussion" in key or "future" in key:

            section_text = "\n".join(sections[key])

            return len(section_text) > 100

    return False





def has_reproducibility_section(text):

    """Check for reproducibility or implementation details section."""

    patterns = [

        r"(?:implementation\s+details|experimental\s+setup|training\s+details)",

        r"(?:reproducibility|reproducible)",

        r"(?:code\s+availability|data\s+availability)",

    ]

    sections = extract_sections(text)

    for key in sections:

        if any(re.search(p, key, re.IGNORECASE) for p in patterns):

            return True

    # Also check in text

    for p in patterns:

        if re.search(p, text[:10000], re.IGNORECASE):

            return True

    return False





# ─── Novelty Analysis ───────────────────────────────────────────────────────



def analyze_novelty(content, contributions, baselines):

    """Score novelty (1-5)."""

    score = 3

    evidence = []

    issues = []



    # Check contribution specificity

    if len(contributions) >= 3:

        score += 0.5

        evidence.append(f"Has {len(contributions)} specific contributions listed")

    elif len(contributions) >= 1:

        evidence.append(f"Has {len(contributions)} contribution(s) listed")

    else:

        score -= 0.5

        issues.append("No explicit contributions listed ?novelty unclear")



    # Check for "first" or "novel" language

    if re.search(r"\b(first|novel|new|to our knowledge|state-of-the-art)\b", content[:5000], re.IGNORECASE):

        evidence.append("Novelty language detected in introduction")



    # Check if the paper positions itself against existing work

    if re.search(r"(?:limitation|drawback|issue|problem|challenge|gap)\s+(?:of|in|with)\s+(?:existing|current|prior|previous|traditional|conventional)", content[:8000], re.IGNORECASE):

        evidence.append("Clearly identifies gaps in prior work")



    # Check number of baselines

    if len(baselines) >= 3:

        score += 0.3

        evidence.append(f"Compared against {len(baselines)} known baselines")

    elif len(baselines) == 0:

        score -= 0.3

        issues.append("No baselines detected ?cannot assess improvement over prior work")



    # Check for ablation studies

    if detect_ablation(content):

        score += 0.3

        evidence.append("Ablation studies present")

    else:

        issues.append("No ablation studies detected ?hard to attribute improvement to specific components")



    # Check for limitations section

    if has_limitations(content):

        evidence.append("Limitations discussed ?demonstrates understanding of scope")



    return max(1, min(5, round(score))), evidence, issues





def analyze_contribution(content, contributions, experiments_text):

    """Score contribution significance (1-5)."""

    score = 3

    evidence = []

    issues = []



    if len(contributions) >= 3:

        score += 0.5

        evidence.append(f"{len(contributions)} contributions claimed")

    elif len(contributions) == 0:

        score -= 1.0

        issues.append("No contributions claimed ?purpose of paper unclear")

        return max(1, min(5, round(score))), evidence, issues



    # Check if contributions are backed by experiments

    if experiments_text and contributions:

        # Count how many contributions have supporting evidence

        supported = 0

        for c in contributions:

            # Check if the contribution's keywords appear in experiments

            keywords = re.findall(r"\b([A-Z][a-z]{2,})\b", c[:100])

            for kw in keywords:

                if kw.lower() in experiments_text.lower():

                    supported += 1

                    break

        if supported >= 2:

            evidence.append(f"At least {supported} contributions supported by experimental evidence")

        elif supported == 0:

            issues.append("Claims not explicitly supported by experimental results")



    # Check for state-of-the-art language

    if re.search(r"(?:outperform|improve|better|state-of-the-art|SOTA)", content, re.IGNORECASE):

        evidence.append("Claims improvement over prior work")



    # Check if paper makes modest vs. grand claims

    if re.search(r"(?:significant|substantial|major|important|novel|first)", content[:10000], re.IGNORECASE):

        evidence.append("Significance of contribution is emphasized")



    # Size of contribution section

    contrib_section = re.search(r"(?:contribution|contribution)", content, re.IGNORECASE)

    if contrib_section:

        evidence.append("Dedicated contributions section present")



    return max(1, min(5, round(score))), evidence, issues





def analyze_experimental_rigor(content, experiments_text, datasets):

    """Score experimental rigor (1-5)."""

    score = 3

    evidence = []

    issues = []



    # Dataset count

    if len(datasets) >= 3:

        score += 0.5

        evidence.append(f"Tested on {len(datasets)} datasets ({', '.join(datasets[:5])})")

    elif len(datasets) >= 2:

        score += 0.3

        evidence.append(f"Tested on {len(datasets)} datasets ({', '.join(datasets[:3])})")

    elif len(datasets) == 1:

        score -= 0.3

        issues.append(f"Only {len(datasets)} dataset tested ?weak generalization evidence")

        if datasets:

            issues.append(f"Dataset: {datasets[0]}")

    elif len(datasets) == 0:

        score -= 1.0

        issues.append("No datasets detected ?experimental section may be missing or underspecified")



    # Baselines

    baselines = detect_baselines(experiments_text if experiments_text else content)

    if len(baselines) >= 3:

        score += 0.3

        evidence.append(f"Compared against {len(baselines)} baselines")

    elif len(baselines) <= 1:

        issues.append("Too few baselines compared against")



    # Comparisons

    if detect_comparisons(experiments_text if experiments_text else content):

        evidence.append("Quantitative comparisons with baselines present")



    # Ablation

    if detect_ablation(experiments_text if experiments_text else content):

        score += 0.3

        evidence.append("Ablation studies present")

    else:

        issues.append("Missing ablation studies ?cannot verify component contributions")



    # Statistical tests

    if has_statistical_tests(content):

        score += 0.5

        evidence.append("Statistical significance tests reported")

    else:

        issues.append("No statistical significance tests ?results may not be robust")



    # Tables and figures

    tables = len(re.findall(r"\\begin\{table\}", content))

    figures = len(re.findall(r"\\begin\{figure\}", content))

    if tables + figures >= 6:

        score += 0.3

        evidence.append(f"Good visualization ({tables} tables, {figures} figures)")

    elif tables + figures <= 2:

        issues.append("Few tables/figures ?limited result presentation")



    # Number of experiments

    if re.search(r"\\begin\{table\}.*?\\end\{table\}", content, re.DOTALL):

        # Check for numbers in tables

        pass



    return max(1, min(5, round(score))), evidence, issues





def analyze_clarity(content):

    """Score clarity (1-5)."""

    score = 3

    evidence = []

    issues = []



    word_count = count_words(content)

    if 4000 <= word_count <= 12000:

        evidence.append(f"Paper length reasonable ({word_count} words)")

    elif word_count > 12000:

        score -= 0.3

        issues.append(f"Paper is long ({word_count} words) ?ensure conciseness")

    elif word_count < 2000:

        score -= 0.3

        issues.append(f"Paper is short ({word_count} words) ?may lack sufficient detail")



    # Structure

    sections = extract_sections(content)

    section_count = len([s for s in sections if s != "preamble"])

    if section_count >= 6:

        evidence.append(f"Well-structured with {section_count} sections")

    elif section_count <= 3:

        score -= 0.3

        issues.append("Too few sections ?paper may lack proper structure")



    # Abstract quality

    abstract = extract_abstract(content)

    if abstract and len(abstract) > 100:

        evidence.append("Abstract present with adequate length")

    elif not abstract:

        score -= 0.5

        issues.append("No abstract found")



    # Figures/tables

    tables = len(re.findall(r"\\begin\{table\}", content))

    figures = len(re.findall(r"\\begin\{figure\}", content))

    if figures >= 2:

        evidence.append(f"{figures} figures present")

    else:

        issues.append("Too few figures ?consider adding a pipeline/architecture figure")



    # Equation count as measure of technical depth

    equations = len(re.findall(r"\$.*?\$|\\\[.*?\\\]|\\begin\{equation\}", content, re.DOTALL))

    if equations >= 5:

        evidence.append(f"{equations} equations ?adequate mathematical formulation")



    # Check for clear motivation in first paragraph

    first_para = content[:2000]

    if re.search(r"(?:however|but|yet|despite|although|while)\s", first_para, re.IGNORECASE):

        evidence.append("Problem motivation clearly articulated with contrast to existing work")



    return max(1, min(5, round(score))), evidence, issues





def analyze_reproducibility(content):

    """Score reproducibility (1-5)."""

    score = 3

    evidence = []

    issues = []



    if has_code_link(content):

        score += 1.0

        evidence.append("Code availability mentioned")



    if has_hyperparams(content):

        score += 0.5

        evidence.append("Hyperparameters reported")

    else:

        issues.append("Hyperparameters not reported")



    if has_reproducibility_section(content):

        score += 0.3

        evidence.append("Implementation details section present")

    else:

        issues.append("No dedicated implementation details section")



    if has_limitations(content):

        score += 0.3

        evidence.append("Limitations discussed")



    # Check for data availability

    if re.search(r"(?:data\s+(?:is|are|will\s+be)\s+(?:available|public|released))", content, re.IGNORECASE):

        score += 0.3

        evidence.append("Data availability mentioned")



    # Method section length as proxy for detail

    method_section = extract_method(content)

    if method_section and count_words(method_section) >= 300:

        evidence.append("Method section has sufficient detail")

    elif method_section and count_words(method_section) < 100:

        score -= 0.3

        issues.append("Method section too brief ?insufficient for replication")



    return max(1, min(5, round(score))), evidence, issues





# ─── Story Analysis ─────────────────────────────────────────────────────────



def analyze_story(content):

    """Analyze the narrative flow of the paper."""

    observations = []



    sections = extract_sections(content)

    section_names = [s for s in sections if s != "preamble"]



    # Check section structure

    expected_sections = ["introduction", "related", "method", "experiment", "discussion", "conclusion"]

    present = []

    for expected in expected_sections:

        for name in section_names:

            if expected in name.lower():

                present.append(expected)

                break



    if len(present) >= 4:

        observations.append(f"Good narrative structure: {', '.join(present)}")

    elif len(present) >= 2:

        observations.append(f"Partial structure: {', '.join(present)}")

        missing = [s for s in expected_sections if s not in present]

        observations.append(f"Missing sections: {', '.join(missing)}")

    else:

        observations.append("Paper lacks standard scientific paper structure")



    # Check if paper tells a coherent story

    if "introduction" in present and "method" in present and "experiment" in present:

        observations.append("Story arc present: problem ?method ?evidence")



    # Check for clear problem statement

    intro = extract_introduction(content)

    if intro:

        if re.search(r"(?:problem|challenge|gap|issue|limitation|question)", intro, re.IGNORECASE):

            observations.append("Clear problem statement in introduction")



    # Check for conclusion

    for name in section_names:

        if "conclusion" in name.lower():

            conclusion_text = "\n".join(sections[name])

            if len(conclusion_text) > 100:

                observations.append("Substantive conclusion with summary and takeaways")



    return observations





# ─── Warning Flags ──────────────────────────────────────────────────────────



def generate_warnings(content, novelty, contribution, rigor, datasets, baselines):

    """Generate specific warning flags about weak areas."""

    warnings = []



    # Missing baselines

    if "ResNet" not in baselines and "CNN" not in baselines and "UNet" not in baselines:

        if "X-ray" in content or "CXR" in content or "medical" in content.lower():

            warnings.append("Not compared to standard baselines (e.g., ResNet, DenseNet, U-Net)")



    # Only one dataset

    if novelty <= 2 and len(datasets) <= 1:

        warnings.append("Low novelty combined with limited evaluation ?contribution may be too incremental")



    # Overclaiming

    if contribution >= 4 and rigor <= 2:

        warnings.append("Claims of significant contribution not backed by sufficient experimental evidence")



    # Missing ablation

    if not detect_ablation(content) and novelty >= 3:

        warnings.append("Novel method without ablation studies ?unclear which components contribute to performance")



    # Method description

    method = extract_method(content)

    if method and not has_code_link(content) and not has_hyperparams(content):

        warnings.append("Method described but missing implementation details for reproducibility")



    # No experiments section at all

    experiments = extract_experiments(content)

    if not experiments:

        warnings.append("No experiments/evaluation section detected")



    # Missing statistical tests

    if len(datasets) >= 2 and not has_statistical_tests(content):

        warnings.append("Multiple datasets but no statistical tests ?significance of results unclear")



    # Generated content patterns

    ai_phrases = [

        r"(?:it is worth noting that)",

        r"(?:importantly|notably),",

        r"(?:as we can see)",

        r"(?:in this paper, we)",

    ]

    for phrase in ai_phrases:

        matches = re.findall(phrase, content[:10000], re.IGNORECASE)

        if len(matches) > 5:

            warnings.append("Repetitive phrasing pattern detected ?consider varying language")

            break



    # References

    refs = extract_citations(content)

    if len(refs) < 10:

        warnings.append(f"Only {len(refs)} unique citations ?potential related work gap")



    return warnings





# ─── Report Generation ──────────────────────────────────────────────────────



def generate_report(input_path, scores_evidence, story_obs, warnings):

    """Generate markdown report."""

    path = Path(input_path)

    lines = []

    lines.append(f"# Novelty Check Report: `{path.name}`\n")



    # Summary

    lines.append("## Summary Scores\n")

    lines.append("| Dimension | Score | Assessment |")

    lines.append("|-----------|-------|------------|")

    total = 0

    count = len(scores_evidence)

    for dim_name, dim_label, score, ev, issues in scores_evidence:

        if score >= 4:

            assessment = "?Strong"

        elif score >= 3:

            assessment = "?Adequate"

        elif score >= 2:

            assessment = "[!] Weak"

        else:

            assessment = "?Critical"

        lines.append(f"| {dim_label} | {score}/5 | {assessment} |")

        total += score

    avg = total / count if count > 0 else 0

    lines.append(f"| **Overall** | **{avg:.1f}/5** | **{'?Strong' if avg >= 4 else '?Adequate' if avg >= 3 else '[!] Needs Work' if avg >= 2 else '?Weak'}** |")

    lines.append("")



    # Detailed analysis

    lines.append("## Detailed Analysis\n")

    for dim_name, dim_label, score, evidence, issues in scores_evidence:

        lines.append(f"### {dim_label}: {score}/5\n")

        if evidence:

            lines.append("**Evidence:**")

            for e in evidence:

                lines.append(f"- ?{e}")

            lines.append("")

        if issues:

            lines.append("**Issues:**")

            for i in issues:

                lines.append(f"- [!] {i}")

            lines.append("")



    # Story

    lines.append("## Narrative Analysis\n")

    if story_obs:

        for obs in story_obs:

            lines.append(f"- {obs}")

        lines.append("")

    else:

        lines.append("Limited narrative structure detected.\n")



    # Warnings

    lines.append("## Warning Flags\n")

    if warnings:

        for w in warnings:

            lines.append(f"- [!] {w}")

        lines.append("")

    else:

        lines.append("No major warning flags detected.\n")



    # Improvement suggestions

    lines.append("## Improvement Suggestions\n")

    suggestions = [

        s for dim_name, dim_label, score, evidence, issues in scores_evidence

        for s in issues

    ]

    suggestions.extend(warnings)

    if suggestions:

        seen = set()

        for s in suggestions:

            if s not in seen:

                lines.append(f"- {s}")

                seen.add(s)

        lines.append("")

    else:

        lines.append("No specific improvements suggested ?paper appears well-rounded.\n")



    return "\n".join(lines)





def generate_json_report(scores_evidence, story_obs, warnings):

    """Generate JSON report."""

    scores = {}

    for dim_name, dim_label, score, ev, issues in scores_evidence:

        scores[dim_name] = {

            "label": dim_label,

            "score": score,

            "evidence": ev,

            "issues": issues,

        }

    report = {

        "scores": scores,

        "overall": round(sum(s["score"] for s in scores.values()) / len(scores), 1) if scores else 0,

        "narrative": story_obs,

        "warnings": warnings,

    }

    return json.dumps(report, indent=2, ensure_ascii=False)





# ─── Main ────────────────────────────────────────────────────────────────────



def main():

    if len(sys.argv) < 2:

        print("Usage: python skills.py path/to/paper.tex")

        sys.exit(1)



    tex_path = Path(sys.argv[1])

    if not tex_path.exists():

        print(f"Error: File not found: {tex_path}")

        sys.exit(1)



    print(f"Analyzing: {tex_path}")



    content = read_tex(str(tex_path))

    word_count = count_words(content)

    sections = extract_sections(content)



    print(f"  Word count: {word_count}")

    print(f"  Sections: {len([s for s in sections if s != 'preamble'])}")



    # Extract data

    contributions = extract_contributions(content)

    datasets = count_datasets(content)

    baselines = detect_baselines(content)

    experiments_text = extract_experiments(content)



    print(f"  Contributions: {len(contributions)}")

    print(f"  Datasets: {len(datasets)} ({', '.join(datasets[:5]) if datasets else 'none'})")

    print(f"  Baselines: {len(baselines)} ({', '.join(baselines[:5]) if baselines else 'none'})")



    # Analyze each dimension

    novelty_score, novelty_ev, novelty_iss = analyze_novelty(content, contributions, baselines)

    contribution_score, contribution_ev, contribution_iss = analyze_contribution(content, contributions, experiments_text)

    rigor_score, rigor_ev, rigor_iss = analyze_experimental_rigor(content, experiments_text, datasets)

    clarity_score, clarity_ev, clarity_iss = analyze_clarity(content)

    repro_score, repro_ev, repro_iss = analyze_reproducibility(content)



    scores_evidence = [

        ("novelty", "Novelty", novelty_score, novelty_ev, novelty_iss),

        ("contribution", "Contribution", contribution_score, contribution_ev, contribution_iss),

        ("experimental_rigor", "Experimental Rigor", rigor_score, rigor_ev, rigor_iss),

        ("clarity", "Clarity", clarity_score, clarity_ev, clarity_iss),

        ("reproducibility", "Reproducibility", repro_score, repro_ev, repro_iss),

    ]



    story_obs = analyze_story(content)

    warnings = generate_warnings(content, novelty_score, contribution_score, rigor_score, datasets, baselines)



    # Print summary

    avg_score = sum(s[2] for s in scores_evidence) / len(scores_evidence)

    print(f"\n  Novelty: {novelty_score}/5")

    print(f"  Contribution: {contribution_score}/5")

    print(f"  Experimental Rigor: {rigor_score}/5")

    print(f"  Clarity: {clarity_score}/5")

    print(f"  Reproducibility: {repro_score}/5")

    print(f"  Overall: {avg_score:.1f}/5")



    if warnings:

        print(f"\n  [!]  Warnings ({len(warnings)}):")

        for w in warnings:

            print(f"    - {w}")



    # Write reports

    stem = tex_path.stem

    out_dir = tex_path.parent



    md_report = generate_report(str(tex_path), scores_evidence, story_obs, warnings)

    md_path = out_dir / f"{stem}.novelty.report.md"

    with open(md_path, "w", encoding="utf-8") as f:

        f.write(md_report)

    print(f"\n  Report: {md_path}")



    json_report = generate_json_report(scores_evidence, story_obs, warnings)

    json_path = out_dir / f"{stem}.novelty.report.json"

    with open(json_path, "w", encoding="utf-8") as f:

        f.write(json_report)

    print(f"  JSON: {json_path}")



    print("\nDone.")





if __name__ == "__main__":

    main()

