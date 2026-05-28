"""Enrich all 12 existing skills with richer SKILL.md and skill_card.md content."""
import os, re, shutil

BASE = r"C:\Users\17588\.openclaw\workspace\skills"
SKILLS_EN = r"C:\Users\17588\.openclaw\workspace\skills_en"

# Richer content for each existing skill
RICH_DESCRIPTIONS = {
    "humanize-writing": {
        "sketch": """# humanize-writing

## name
humanize-writing

## description
Convert AI-generated academic text to natural human writing style while preserving technical accuracy. This skill systematically detects and removes common AI-typical phrasing patterns: over-hedging ("may potentially", "it should be noted that"), redundant transitions ("furthermore", "moreover"), formulaic sentence openings, and passive voice overuse. It then applies a structured humanization pipeline with sentence-level transformations.

## When to use this skill
- Paper Writing: You've used LLM to draft a paper and need to remove the AI-味 before submission
- Revision: Your advisor said the writing "sounds like ChatGPT" and you need to fix it
- Before submission: Run this as a final quality check on all sections
- When translating: Convert Chinese academic writing to natural English

## Inputs
- Paper .tex file (the target section or full paper)

## Workflow
1. Scan text for AI-ism patterns (hedging words list, empty transitions list, formulaic templates)
2. Calculate AI-ism density (pattern count per 100 words)
3. Apply priority-ordered transformations:
   a) Remove hedge words (cut: notably, importantly, interestingly, significantly, remarkably)
   b) Vary sentence openings (< 40% same-start sentences)
   c) Break sentences longer than 35 words
   d) Remove redundant transitions (therefore, furthermore, moreover)
   e) Add strategic authorial voice ("we argue", "our key insight")
4. Generate before/after diff
5. Calculate post-fix AI-ism density
6. Output: fixed .tex, diff .md, report .md

## Output format
- Fixed .tex file
- Diff report .md (showing each change with old/new)
- Humanization report .md (AI-ism density before/after, sentence stats, readability scores)

## Safety and limitations
- Preserves ALL technical content, citations, equations
- Does not change scientific meaning
- May over-simplify domain-specific terminology
- Cannot verify factual accuracy

## Example trigger
- "Humanize the introduction section of my paper"
- "Remove AI-味 from the abstract"
- "Run humanization on the entire .tex file"

## Constraints
- Preserve all LaTeX commands, citations, and equations
- Do not change numbers, metrics, or technical claims
- Maintain formal academic tone (not conversational)""",
        "card_extra": "| Criterion | Description |\n|-----------|-------------|\n| AI-ism removal rate | Percentage of detected patterns removed |\n| False positive rate | Non-AI patterns incorrectly modified |\n| Readability improvement | Flesch Reading Ease change before/after |"
    },
    "reference-verifier": {
        "sketch": """# reference-verifier

## name
reference-verifier

## description
Verify that references cited in academic papers are real, traceable publications. This skill parses thebibliography environments from .tex files or .bib files, extracts metadata (venue, year, authors, arXiv ID), cross-references against a database of 14 known academic venues with their year ranges, validates arXiv ID format, and flags suspicious entries (e.g., venue doesn't exist, year outside venue range, inconsistent author count).

## When to use this skill
- After using LLM to generate references: LLMs often hallucinate fake papers
- Before submission: Ensure all citations point to real venues
- During paper review: Check if the cited papers actually exist
- When adapting a paper: Verify transferred references

## Inputs
- Paper .tex file (thebibliography environment)
- Bibliography .bib file

## Workflow
1. Parse thebibliography or .bib entries via regex
2. Extract per-entry: authors, title, venue abbreviation, year, arXiv ID, DOI
3. Match each venue against known database (MICCAI, CVPR, AAAI, NeurIPS, EMNLP, NAACL, ISBI, JBHI, Scientific Data, etc.)
4. Validate year against venue's active year range
5. Validate arXiv ID format (YYMM.NNNNN or YYMM.NNNNNvN)
6. Flag suspicious items (venue not in database, year mismatch, malformed arXiv ID)
7. Generate MD report with per-reference status: VERIFIED / UNCERTAIN / SUSPICIOUS

## Output format
- Reference verification report .md (per-reference table with status + reason)
- JSON report .json (machine-readable version)

## Safety and limitations
- Cannot query arXiv API for real-time existence check
- Cannot verify if reference content matches paper claims
- Non-standard venue abbreviations may be flagged as UNKNOWN

## Example trigger
- "Verify all references in my paper"
- "Check if the LLM-generated bibliography is real"
- "Audit references before submission"

## Constraints
- Do not modify the .tex file
- Clearly label each reference as VERIFIED / UNCERTAIN / SUSPICIOUS""",
        "card_extra": "| Criterion | Description |\n|-----------|-------------|\n| Detection rate | Percentage of fake/mismatched references caught |\n| False positive rate | Valid references incorrectly flagged |\n| Coverage | Number of venue databases covered |"
    },
    "reviewer-simulator": {
        "sketch": """# reviewer-simulator

## name
reviewer-simulator

## description
Simulate three MICCAI reviewer personas (constructive, critical, balanced) to provide pre-submission feedback on a LaTeX paper. Each reviewer scores five dimensions (novelty, technical soundness, experimental rigor, clarity, reproducibility) from 1-5 and generates structured reviewer comments. The skill also auto-fixes typos, grammar, and LaTeX formatting issues.

## When to use this skill
- Before submitting to MICCAI or similar conferences
- After completing the first full draft
- When you want to preempt reviewer concerns
- To identify weak sections before asking for real feedback

## Inputs
- Paper .tex file

## Workflow
1. Parse .tex file for paper statistics (word count, sections, datasets, baselines, claims)
2. Apply auto-fixes: typos, grammar, LaTeX formatting
3. For each reviewer persona, compute base scores from paper statistics:
   - Novelty: based on claims count, dataset diversity, uniqueness of approach
   - Technical soundness: based on baselines, datasets, section structure
   - Experimental rigor: based on ablation studies, statistical tests, dataset size
   - Clarity: based on figures, tables, section organization
   - Reproducibility: based on code availability, implementation details
4. Apply persona bias adjustments
5. Generate per-reviewer comments with specific section references
6. Output comprehensive review report

## Output format
- Fixed .tex file (with auto-corrections)
- Diff .md (showing all auto-fix changes)
- Review report .md (3 reviewers, 5-dimension scores, detailed comments)

## Safety and limitations
- Scores based on statistical rules, not semantic understanding
- Cannot evaluate experimental design validity
- Auto-fixes may break LaTeX in rare cases

## Example trigger
- "Simulate 3 MICCAI reviewers on my paper"
- "Get pre-submission review feedback"
- "Check if my paper meets MICCAI standards"

## Constraints
- Scores are simulated, not actual reviewer judgment
- Do not use as replacement for human review""",
        "card_extra": "| Criterion | Description |\n|-----------|-------------|\n| Score diversity | Do the 3 reviewers produce meaningfully different scores? |\n| Comment relevance | Are generated comments related to actual paper content? |\n| Actionability | Do comments suggest concrete improvements? |"
    },
    "novelty-checker": {
        "sketch": """# novelty-checker

## name
novelty-checker

## description
Analyze a paper's novelty, contribution, experimental rigor, clarity, and reproducibility across five dimensions (1-5 scoring). The skill extracts contributions, baselines, datasets, and experiments from the .tex file, then checks whether claims are backed by experimental evidence, whether appropriate baselines are compared, and whether ablation studies are conducted.

## When to use this skill
- Before submission to check if your contribution is convincing enough
- When reviewers flagged "lack of novelty" in a previous submission
- As a self-assessment tool before sending to your advisor
- To identify weak points in your experimental validation

## Inputs
- Paper .tex file

## Workflow
1. Parse .tex: extract contributions, baselines, datasets, experiment sections
2. Novelty scoring:
   - Check for novelty language ("first", "novel", "to our knowledge")
   - Count unique contributions
   - Check positioning against existing work
3. Contribution scoring:
   - Do claims match the evidence?
   - Are datasets sufficient?
   - Are contributions clearly stated?
4. Experimental rigor scoring:
   - Number and diversity of baselines
   - Ablation studies present?
   - Statistical tests reported?
5. Clarity scoring:
   - Section organization
   - Figure and table quality
   - Writing clarity
6. Reproducibility scoring:
   - Code availability
   - Implementation details
   - Random seed, hardware reported?
7. Generate warning flags for weak areas

## Output format
- Novelty assessment report .md (5 dimension scores + evidence + issues)
- JSON report .json (machine-readable version)

## Safety and limitations
- Limited to keyword-based novelty detection ("first", "novel" detection)
- Cannot assess experimental design quality
- Baseline detection relies on predefined list

## Example trigger
- "Check the novelty of my paper"
- "Is my contribution strong enough for MICCAI?"
- "Find weak spots in my experimental validation"

## Constraints
- Scores are relative guides, not absolute judgments
- Clearly separate objective findings from subjective assessments""",
        "card_extra": "| Criterion | Description |\n|-----------|-------------|\n| Coverage | Do the 5 dimensions capture all reviewer concerns? |\n| Evidence support | Are scores backed by text evidence? |\n| Actionability | Does the output point to specific improvements? |"
    },
    "literature-miner": {
        "sketch": """# literature-miner

## name
literature-miner

## description
Search and analyze recent (2025-2026) top-venue papers in CXR report generation, medical multi-agent systems, and medical AI education. Contains a curated database of 20+ verified papers from MICCAI, CVPR, AAAI, ISBI, JBHI, and other venues. In search mode, finds papers by topic. In analyze mode, reads the user's paper and generates concrete innovation enhancement suggestions with references to inspiring papers.

## When to use this skill
- When writing Related Work section
- When looking for innovation inspiration
- Before submission to ensure up-to-date literature coverage
- After receiving reviewer feedback suggesting missing related work

## Inputs
- Paper .tex file (analyze mode)
- Topic keywords (search mode)

## Workflow
Search mode:
1. Parse topic keywords
2. Match against curated paper database (title, innovation, keywords)
3. Return ranked list of relevant papers
4. Generate structured markdown report

Analyze mode:
1. Parse paper's method section and identify current approach components
2. Check for existing literature coverage gaps
3. Cross-reference with known papers to generate enhancement suggestions
4. Each suggestion includes: area, inspiration paper, concrete adaptation method
5. Generate structured report

## Output format
- Literature mining report .md (search mode)
- Innovation enhancement suggestions .md (analyze mode, with 5-8 concrete suggestions)

## Safety and limitations
- Database is static (20+ papers) and needs manual updates
- Suggestions are rule-generated and may not fit all papers
- Cannot access real-time literature databases

## Example trigger
- "Find papers on multi-agent medical AI published in 2025-2026"
- "Suggest innovations for my paper based on recent SOTA"
- "Search for CXR report generation papers"

## Constraints
- All paper entries in database are verified as real publications
- Enhancement suggestions are inspiration, not guaranteed improvements""",
        "card_extra": "| Criterion | Description |\n|-----------|-------------|\n| Relevance | Do search results match the topic? |\n| Suggestion quality | Are enhancement suggestions concrete and actionable? |\n| Coverage | Does the database cover the main research directions? |"
    },
    "submission-formatter": {
        "sketch": """# submission-formatter

## name
submission-formatter

## description
Adapt academic paper formatting to match target venue requirements. Supports LNCS/MICCAI, CVPR, AAAI, and general two-column templates. Adjusts column layout, font size, margins, citation style, section naming conventions, and reference format.

## When to use this skill
- When switching target venue (e.g., from MICCAI to CVPR)
- When venue updates template requirements
- When converting a technical report to submission format
- When you need to check page limit compliance

## Inputs
- Paper .tex file

## Workflow
1. Detect current template (LNCS, CVPR, AAAI, or custom)
2. Read target venue requirements from template database
3. Apply format transformations:
   - Document class and options
   - Column layout (single/double)
   - Font size and spacing
   - Citation style (author-year vs numbered)
   - Section numbering style
   - Reference format
4. Check page/word count against venue limits
5. Output formatted .tex + modification report

## Output format
- Formatted .tex file
- Format modification report .md

## Safety and limitations
- Limited to template database; new templates require additions
- May not handle complex custom LaTeX packages
- Page count estimate is approximate

## Example trigger
- "Convert my paper from MICCAI template to CVPR"
- "Format this paper for AAAI submission"
- "Check if the paper meets the page limit"

## Constraints
- Preserve all content; only adjust formatting
- Maintain compilability of the .tex file""",
        "card_extra": "| Criterion | Description |\n|-----------|-------------|\n| Template compatibility | Does output compile with target template? |\n| Format completeness | Are all required format changes applied? |\n| Content preservation | Is all content preserved without loss? |"
    }
}


def update_skill(key, data):
    base_dir = os.path.join(BASE, key)
    
    # Update SKILL.md
    sk_path = os.path.join(base_dir, "SKILL.md")
    if key in RICH_DESCRIPTIONS:
        with open(sk_path, 'w', encoding='utf-8') as f:
            f.write(RICH_DESCRIPTIONS[key]["sketch"])
        print(f"  [OK] {key}/SKILL.md updated ({len(RICH_DESCRIPTIONS[key]['sketch'])} chars)")
    
    # Update skill_card.md
    sc_path = os.path.join(base_dir, "skill_card.md")
    if os.path.exists(sc_path):
        # Read the existing card and append richer evaluation
        with open(sc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # If the card's evaluation section is generic, replace it
        if "| Criterion | Description |" in content and key in RICH_DESCRIPTIONS:
            old_eval_start = content.find("| Criterion | Description |")
            if old_eval_start > 0:
                old_eval_end = content.find("\n\n", old_eval_start)
                if old_eval_end > old_eval_start:
                    new_eval = RICH_DESCRIPTIONS[key]["card_extra"]
                    content = content[:old_eval_start] + new_eval + content[old_eval_end:]
                    with open(sc_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  [OK] {key}/skill_card.md evaluation updated")
    
    # Create skills.py placeholder if none exists
    py_path = os.path.join(base_dir, "skills.py")
    if not os.path.exists(py_path):
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(f'''#!/usr/bin/env python3
"""skills.py for {key} — {data.get('description', 'A research skill')}"""
import sys, os

def main():
    print(f"[i] {key}: {data.get('description', '')[:60]}...")
    input_path = sys.argv[1] if len(sys.argv) > 1 else "examples/input/"
    print(f"[i] Processing: {{input_path}}")
    print(f"[i] See SKILL.md for full workflow description.")

if __name__ == "__main__":
    main()
''')
        print(f"  [OK] {key}/skills.py created")
    
    # Mirror to skills_en
    en_dir = os.path.join(SKILLS_EN, key)
    if os.path.exists(en_dir):
        for fn in ['SKILL.md', 'skill_card.md', 'skills.py']:
            src = os.path.join(base_dir, fn)
            dst = os.path.join(en_dir, fn)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"  [OK] mirrored {fn} to skills_en/{key}/")


# Update each skill with richer content
for key, data in RICH_DESCRIPTIONS.items():
    print(f"\n--- {key} (enriching) ---")
    update_skill(key, data)

print("\nDone enriching existing skills!")
