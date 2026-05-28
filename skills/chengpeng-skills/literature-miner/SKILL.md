# literature-miner

## name
literature-miner

## description
Search and analyze recent (2025-2026) top-venue papers in CXR report generation, medical multi-agent systems, and medical AI education. Contains a curated database of 20+ verified papers from MICCAI, CVPR, AAAI, ISBI, JBHI, and other venues. In search mode, finds papers by topic. In analyze mode, reads the user's paper and generates concrete innovation enhancement suggestions with references to inspiring papers.


### Real-world usage
This skill processes real LobsterCXR research files: 基于 20+ 篇 2025-2026 顶会论文分析 LobsterCXR，产出 7 条增强建议
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
- Enhancement suggestions are inspiration, not guaranteed improvements