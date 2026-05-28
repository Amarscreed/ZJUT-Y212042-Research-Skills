# Skill Card: reviewer-simulator

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | reviewer-simulator |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 审稿模拟 / Review Simulation |
| Target Users | 准备投稿的研究生、论文作者 |
| GitHub 路径 | chengpeng-skills/reviewer-simulator/ |

## 2. Research Pain Point

投稿前不知道审稿人会如何看待论文。找人预审麻烦、耗时，且预审人可能不了解会议标准。

## 3. What This Skill Does

### This skill can:
1. 解析论文 .tex 文件，统计字数、章节数、数据集数量、基线数量
2. 模拟 3 个不同风格的审稿人（建设型、批判型、平衡型）
3. 对新颖性、技术合理性、实验严谨性、清晰度、可复现性 5 维度打分
4. 自动修正拼写、语法、格式问题
5. 输出修正版 .tex、差异对比 .md、审稿报告 .md

### This skill does not aim to:
1. 不替代真实审稿人的领域专业知识
2. 不判断论文是否应该被接收
3. 不做实验数据的事实核查

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
- 修正版 .tex 文件
- 修改差异 .md
- 审稿报告 .md

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
1. 解析论文统计信息（字数、章节、数据集、基线、声明数）
2. 应用自动修正（拼写、语法、格式）
3. 对 5 个维度计算基准分 + reviewer bias 调整
4. 生成每个审稿人的评语和分数
5. 输出审稿报告

## 7. Group-Specific Feature

3 种审稿人 persona（建设型/批判型/平衡型），提供多维度的反馈模拟

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| Score diversity | Do the 3 reviewers produce meaningfully different scores? |
| Comment relevance | Are generated comments related to actual paper content? |
| Actionability | Do comments suggest concrete improvements? |

## 10. Limitations

This skill may fail when:
- 评分基于统计规则而非真正理解论文内容
- 无法评估实验设计的合理性
- 自动修正可能破坏 LaTeX 命令

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the research task
- Store or expose personal data
- Fabricate experimental results or paper references
- Claim certainty when evidence is insufficient

## 12. Future Improvements

- 接入 LLM 生成更语义化的审稿意见
- 支持更多会议模板（CVPR, AAAI, NeurIPS）
- 增加审稿意见分类和优先级排序

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/reviewer-simulator/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
