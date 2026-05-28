# Skill Card: submission-formatter

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | submission-formatter |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 投稿格式化 / Submission Formatting |
| Target Users | 准备投稿的研究生、论文作者 |
| GitHub 路径 | chengpeng-skills/submission-formatter/ |

## 2. Research Pain Point

不同会议/期刊有不同格式要求（单双栏、字数限制、引用格式）。手动调整费时且容易出错。

## 3. What This Skill Does

### This skill can:
1. 检测当前论文的 LaTeX 模板和格式
2. 调整列布局（单栏/双栏）
3. 调整字数/页数限制
4. 转换引用格式（样式中英文）
5. 统一图表编号和标题格式

### This skill does not aim to:
1. 不做内容修改（只调整格式）
2. 不保证完全符合所有模板要求
3. 不处理投稿系统操作

## 4. Required Inputs

The skill expects one or more of the following inputs:
- 论文 .tex 文件

### Example input files:
```
examples/input/
├── paper.tex
```

## 5. Expected Outputs

The skill produces:
- 格式化后的 .tex 文件
- 格式修改报告 .md

### Example output structure:
1. Task summary
2. Key findings
3. Evidence
4. Analysis / Diagnosis
5. Suggested next steps
6. Limitations

### Example output files:
```
examples/output/
└── report.md
```

## 6. Workflow

The skill follows this workflow:
1. 检测当前模板和格式
2. 根据目标 venue 确定格式要求
3. 执行格式转换（布局、字号、引用样式、页数限制）
4. 输出格式化后的文件 + 修改报告

## 7. Group-Specific Feature

内置 LNCS/MICCAI、CVPR、AAAI 等多种模板的格式规则库

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| Template compatibility | Does output compile with target template? |
| Format completeness | Are all required format changes applied? |
| Content preservation | Is all content preserved without loss? |

## 10. Limitations

This skill may fail when:
- 对高度自定义的模板支持有限
- 可能无法处理使用非标准包的 .tex 文件
- 引用格式转换基于规则，可能不完美

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the research task
- Store or expose personal data
- Fabricate experimental results or paper references
- Claim certainty when evidence is insufficient

## 12. Future Improvements

- 增加更多模板支持（NeurIPS, ICML, ICLR）
- 支持图表尺寸自动调整
- 支持 .docx 格式输出

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/submission-formatter/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
