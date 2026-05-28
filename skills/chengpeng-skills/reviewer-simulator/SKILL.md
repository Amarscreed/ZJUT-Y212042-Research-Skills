# reviewer-simulator

## name
reviewer-simulator

## description
Simulate three MICCAI reviewer personas (constructive, critical, balanced) to provide pre-submission feedback on a LaTeX paper. Each reviewer scores five dimensions (novelty, technical soundness, experimental rigor, clarity, reproducibility) from 1-5 and generates structured reviewer comments. The skill also auto-fixes typos, grammar, and LaTeX formatting issues.


### Real-world usage
This skill processes real LobsterCXR research files: 3 位 MICCAI 审稿人模拟，5 维度评分（3.6-4.0/5），含自动修正
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
- Do not use as replacement for human review