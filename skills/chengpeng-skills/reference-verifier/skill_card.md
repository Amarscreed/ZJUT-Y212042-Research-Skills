# Skill Card: reference-verifier

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | reference-verifier |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 文献审计 / Reference Audit |
| Target Users | 论文作者、审稿人、课程作业检查者 |
| GitHub 路径 | chengpeng-skills/reference-verifier/ |

## 2. Research Pain Point

LLM 生成的论文有时会编造参考文献——DOI 不存在、会议年份错误、作者不符。人工逐条核查费时费力。

## 3. What This Skill Does

### This skill can:
1. 解析 LaTeX thebibliography 或 .bib 文件
2. 检查引用是否来自已知学术会议/期刊
3. 验证 arXiv ID 格式是否合法
4. 检测可疑的引用条目（年份不符、venue 拼写错误）
5. 生成 JSON 和 Markdown 双格式验证报告

### This skill does not aim to:
1. 不做论文内容的事实核查
2. 不检查引用是否与论文论点相关
3. 不连网验证 arXiv 论文是否仍在线上

## 4. Required Inputs

The skill expects one or more of the following inputs:
- 论文 .tex 文件
- Bibliography .bib 文件

### Example input files:
```
examples/input/
├── paper.tex
```

## 5. Expected Outputs

The skill produces:
- 参考验证报告 .md
- 参考验证报告 .json

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
1. 解析文献条目，提取 venue、year、作者、arXiv ID 等元数据
2. 对照已知 venue 数据库（MICCAI, CVPR, AAAI, NeurIPS 等 14 种）
3. 检查年份是否在 venue 成立范围内
4. 检查 arXiv ID 格式（YYMM.NNNNN）
5. 标记可疑条目
6. 生成 MD + JSON 报告

## 7. Group-Specific Feature

内置 14 种顶会/顶刊的年表数据库，能检测年份和 venue 不匹配

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| Detection rate | Percentage of fake/mismatched references caught |
| False positive rate | Valid references incorrectly flagged |
| Coverage | Number of venue databases covered |

## 10. Limitations

This skill may fail when:
- 无法连网实时查询 arXiv API
- 无法验证引用内容是否与论文主张一致
- 对非标准 venue 名称可能误报

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the research task
- Store or expose personal data
- Fabricate experimental results or paper references
- Claim certainty when evidence is insufficient

## 12. Future Improvements

- 连接开源学术 API（Semantic Scholar, CrossRef）
- 增加论文内容-引用一致性检查
- 支持更多会议/期刊数据库

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/reference-verifier/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
