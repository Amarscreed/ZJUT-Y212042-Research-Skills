# Skill Card: result-consistency

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | result-consistency |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 结果一致性检查 / Result Consistency Check |
| Target Users | 论文作者、审稿人、课程评审 |
| GitHub 路径 | chengpeng-skills/result-consistency/ |

## 2. Research Pain Point

论文中常出现结论与实验结果不对应的情况：声称 SOTA 但表中不是最高、描述『显著提升』但无统计检验、消融缺少关键对比。人工逐条对照耗时且容易遗漏。

## 3. What This Skill Does

### This skill can:
1. 解析实验结果表格，提取数值指标
2. 提取论文中的性能声明（『优于』『超越』『SOTA』等）
3. 将声明与表格中的实际数值进行对照
4. 检测过度声明（声称第一但表格中不是）
5. 检查统计显著性报告是否完整

### This skill does not aim to:
1. 不验证实验结果的真实性
2. 不判断实验设计是否合理
3. 不提供实验数据

## 4. Required Inputs

The skill expects:
- 论文 .tex 或 PDF
- 实验结果表格文本（LaTeX tabular 或 CSV）

### Example input files:
```
examples/input/
```

## 5. Expected Outputs

The skill produces:
- 声明-证据对照表 (.md)
- 不一致性报告 (.json)

### Example output structure:
1. Task summary
2. Key findings with evidence
3. Confidence levels per finding
4. Analysis / Diagnosis
5. Suggested next steps
6. Limitations

## 6. Workflow

1. 解析 .tex 文件，提取所有实验结果表格中的数值
2. 标记每个指标的 Top-1 / Top-2 / 基线等
3. 提取所有性能相关的 claim 语句（『优于』『SOTA』『最佳』等）
4. 将每个 claim 与对应表格中的实际排名进行对照
5. 检测不一致：声称 SOTA 但非最优、声称提升但无数字
6. 检测过度声明：语义超出数据支撑范围
7. 检查消融实验是否声称了非消融组件的效果
8. 输出声明-证据对照表 + 不一致性报告

## 7. Group-Specific Feature

将论文中的语言声明与表格中的实际数值进行自动对照，检测『说得好听但数据不支持』的不一致——审稿人最常发现的论文问题之一

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

### How to Run
```bash
cd skills/result-consistency
python skills.py --input examples/input/
```

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| 不一致检测率 | 能否发现已知的声明-数据不一致 |
| 误报率 | 是否将合理声明标记为不一致 |
| 覆盖度 | 是否覆盖了所有实验结果表格 |

## 10. Limitations

- 对复杂的跨表引用（『见图 X』）解析能力有限
- 无法判断统计检验是否合理
- 对非数值型声明（『可视化结果表明』）无法验证

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the task
- Store or expose personal data
- Fabricate results or references
- Claim HIGH confidence when evidence is insufficient

## 12. Future Improvements

- 接入统计检验自动计算
- 支持图表中数值的 OCR 提取
- 增加领域特定的性能基线数据库

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/result-consistency/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
