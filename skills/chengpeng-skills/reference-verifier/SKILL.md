# reference-verifier

## name
reference-verifier

## description
Verify that references cited in academic papers are real, traceable publications. This skill parses thebibliography environments from .tex files or .bib files, extracts metadata (venue, year, authors, arXiv ID), cross-references against a database of 14 known academic venues with their year ranges, validates arXiv ID format, and flags suspicious entries (e.g., venue doesn't exist, year outside venue range, inconsistent author count).


### Real-world usage
This skill processes real LobsterCXR research files: 验证 LobsterCXR 论文的 21 条参考文献，14 种 venue 年表数据库校验
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
- Clearly label each reference as VERIFIED / UNCERTAIN / SUSPICIOUS