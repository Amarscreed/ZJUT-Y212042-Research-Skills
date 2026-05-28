# Skill Card: reviewer-response

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | reviewer-response |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 审稿回应 / Reviewer Response |
| Target Users | 收到审稿意见的研究生、论文作者 |
| GitHub 路径 | chengpeng-skills/reviewer-response/ |

## 2. Research Pain Point

收到 3 个审稿人的意见后，需要逐条回复并修改论文。人工整理审稿意见-证据-回复矩阵费时，容易遗漏或组织不清晰，导致审稿人不满。

## 3. What This Skill Does

### This skill can:
1. 解析审稿意见文本，按审稿人分类
2. 提取每条意见的核心关切和具体问题
3. 将意见映射到论文章节和具体位置
4. 生成回复建议（包含证据引用、修改方案）
5. 输出结构化证据-回复矩阵

### This skill does not aim to:
1. 不自动生成回复内容（只提供结构框架）
2. 不判断审稿意见的合理性
3. 不修改论文本身

## 4. Required Inputs

The skill expects:
- 审稿意见文本 (.txt/.md)
- 论文 PDF 或 .tex 文件
- 编辑决策信件（可选）

### Example input files:
```
examples/input/
```

## 5. Expected Outputs

The skill produces:
- 审稿意见证据矩阵 (.md/.csv)
- 回复草稿 .md

### Example output structure:
1. Task summary
2. Key findings with evidence
3. Confidence levels per finding
4. Analysis / Diagnosis
5. Suggested next steps
6. Limitations

## 6. Workflow

1. 解析审稿意见，按审稿人编号分组
2. 对每条意见提取：类型（实验/方法/写作）、核心关切、问题等级
3. 将每条意见映射到论文章节和具体段落
4. 对每条意见生成回复框架：感谢 → 理解问题 → 证据/修改 → 结果
5. 生成结构化证据-回复矩阵
6. 标记需要重点关注的 CRITICAL 意见

## 7. Group-Specific Feature

将审稿意见与论文具体位置双向映射，生成证据-回复矩阵，确保没有遗漏任何审稿人关切

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

### How to Run
```bash
cd skills/reviewer-response
python skills.py --input examples/input/
```

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| 覆盖度 | 是否捕获了所有审稿意见 |
| 映射准确性 | 意见到章节的映射是否合理 |
| 回复框架有用性 | 回复模板是否能节省用户时间 |

## 10. Limitations

- 无法理解高度专业化的审稿术语
- 回复建议需要用户根据专业知识调整
- 无法判断回复策略是否最优

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the task
- Store or expose personal data
- Fabricate results or references
- Claim HIGH confidence when evidence is insufficient

## 12. Future Improvements

- 支持多轮审稿的版本对比
- 增加常见审稿意见模板库
- 集成到 Overleaf 或 LaTeX 工作流

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/reviewer-response/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
