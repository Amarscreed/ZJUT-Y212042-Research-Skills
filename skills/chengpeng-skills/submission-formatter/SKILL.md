# submission-formatter

## name
submission-formatter

## description
Adapt academic paper formatting to match target venue requirements. Supports LNCS/MICCAI, CVPR, AAAI, and general two-column templates. Adjusts column layout, font size, margins, citation style, section naming conventions, and reference format.


### Real-world usage
This skill processes real LobsterCXR research files: LNCS/MICCAI 模板适配，13 页零报错编译
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
- Maintain compilability of the .tex file