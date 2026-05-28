# humanize-writing

## name
humanize-writing

## description
Convert AI-generated academic text to natural human writing style while preserving technical accuracy. This skill systematically detects and removes common AI-typical phrasing patterns: over-hedging ("may potentially", "it should be noted that"), redundant transitions ("furthermore", "moreover"), formulaic sentence openings, and passive voice overuse. It then applies a structured humanization pipeline with sentence-level transformations.


### Real-world usage
This skill processes real LobsterCXR research files: 对 LobsterCXR 论文进行 AI 味检测与消除，产出 21 项自动人化变换
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
- Maintain formal academic tone (not conversational)