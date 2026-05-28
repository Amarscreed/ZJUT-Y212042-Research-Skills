# reviewer-response

## name
reviewer-response

## description
Organize reviewer comments into a structured evidence-response matrix, mapping each comment to paper sections and planned revisions.


### Real-world usage
This skill processes real LobsterCXR research files: 针对 3 位审稿人的 8 条意见组织证据-回复矩阵
## When to use this skill
- 审稿回应 / Reviewer Response
- 当你遇到收到 3 个审稿人的意见后，需要逐条回复并修改论文。人工整理审稿意见-证据-回复...

## Inputs
reviewer-response expects one or more of the following inputs:
- 审稿意见文本 (.txt/.md)
- 论文 PDF 或 .tex 文件
- 编辑决策信件（可选）

### Example input files:
```
examples/input/
├── reviewer_comments.txt
├── paper.tex
└── code_repo.txt
```

## Workflow
1. 解析审稿意见，按审稿人编号分组
2. 对每条意见提取：类型（实验/方法/写作）、核心关切、问题等级
3. 将每条意见映射到论文章节和具体段落
4. 对每条意见生成回复框架：感谢 → 理解问题 → 证据/修改 → 结果
5. 生成结构化证据-回复矩阵
6. 标记需要重点关注的 CRITICAL 意见

## Output format
reviewer-response produces:
- 审稿意见证据矩阵 (.md/.csv)
- 回复草稿 .md

### Example output structure:
1. Task summary
2. Key findings
3. Evidence source for each finding
4. Analysis / Diagnosis
5. Confidence levels (HIGH / MEDIUM / LOW)
6. Suggested next steps
7. Limitations

## Safety and limitations
- 无法理解高度专业化的审稿术语
- 回复建议需要用户根据专业知识调整
- 无法判断回复策略是否最优

## Example trigger
- "收到 3 个审稿人的意见后，需要逐条回复并修改论文。人工整理审稿意见-证据-回复矩阵费时，容易遗漏或..."

## Constraints
- All claims must be backed by evidence from input materials
- Clearly distinguish HIGH/MEDIUM/LOW confidence
- Do not fabricate findings not supported by inputs
