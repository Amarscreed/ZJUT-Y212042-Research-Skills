# novelty-checker

## name
novelty-checker

## description
Analyze a paper's novelty, contribution, experimental rigor, clarity, and reproducibility across five dimensions (1-5 scoring). The skill extracts contributions, baselines, datasets, and experiments from the .tex file, then checks whether claims are backed by experimental evidence, whether appropriate baselines are compared, and whether ablation studies are conducted.


### Real-world usage
This skill processes real LobsterCXR research files: 5 维度创新评估：新颖性 3/5, 贡献度 2/5, 实验严谨性 5/5, 清晰度 3/5, 可复现性 4/5
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
- Clearly separate objective findings from subjective assessments