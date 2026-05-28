# Skill Card: novelty-checker

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | novelty-checker |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 创新性评估 / Novelty Assessment |
| Target Users | 论文作者、导师、课程评审 |
| GitHub 路径 | chengpeng-skills/novelty-checker/ |

## 2. Research Pain Point

研究生写论文时常陷入『自我感觉创新 vs. 审稿人认为创新不够』的困境。缺乏客观的贡献评估工具。

## 3. What This Skill Does

### This skill can:
1. 提取论文的贡献声明、基线方法列表、使用的数据集
2. 在 5 个维度（新颖性、贡献度、实验严谨性、清晰度、可复现性）上分别打分 1-5
3. 检查声明是否有实验证据支撑
4. 检测薄弱环节（缺基线对比、消融不完整、数据不足）
5. 输出 MD + JSON 双格式报告

### This skill does not aim to:
1. 不判断论文是否应该被接收
2. 不做实验数据真实性核查
3. 不评估论文的写作质量

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
- 创新性评估报告 .md
- 创新性评估报告 .json

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
1. 解析 .tex 文件提取统计信息（贡献数、基线、数据集、代码链接）
2. 分析新颖性（是否有『首次』『创新』等表述，是否与现有工作对比）
3. 分析贡献度（声明数量、是否有实验支撑、数据集是否充分）
4. 分析实验严谨性（基线数量、数据集数量、消融研究）
5. 分析清晰度（章节结构、图表数量、表格可读性）
6. 分析可复现性（代码链接、参数设置、实现细节）
7. 生成警告列表和结构化报告

## 7. Group-Specific Feature

5 维度的结构化评估 + 证据匹配检查，可定位具体薄弱环节

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| Coverage | Do the 5 dimensions capture all reviewer concerns? |
| Evidence support | Are scores backed by text evidence? |
| Actionability | Does the output point to specific improvements? |

## 10. Limitations

This skill may fail when:
- 对真正突破性工作的识别能力有限（依赖『首次』等关键词）
- 无法评估实验设计是否合理
- 基线检测基于预定义列表，可能遗漏领域特定基线

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the research task
- Store or expose personal data
- Fabricate experimental results or paper references
- Claim certainty when evidence is insufficient

## 12. Future Improvements

- 接入论文引用网络分析
- 增加领域特定的基线数据库
- 支持多轮评估（修改前后对比）

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/novelty-checker/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
