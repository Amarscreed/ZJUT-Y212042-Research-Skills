# Skill Card: experiment-diagnosis

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | experiment-diagnosis |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 实验诊断 / Experiment Diagnosis |
| Target Users | 研究生、实验者、项目成员 |
| GitHub 路径 | chengpeng-skills/experiment-diagnosis/ |

## 2. Research Pain Point

训练实验跑完后，性能不达标或出现 NaN，但很难快速定位是学习率、数据划分、模型结构还是代码改动导致的。人工翻日志和 config 逐个排查效率极低。

## 3. What This Skill Does

### This skill can:
1. 解析训练日志（loss 曲线、NaN 检测、收敛趋势）
2. 解析配置文件（学习率、batch size、优化器参数）
3. 对比多组实验的指标表格（metrics.csv）
4. 分析 Git diff 定位代码/配置变更
5. 输出结构化诊断报告，含根因分析和修复建议

### This skill does not aim to:
1. 不修改实验代码
2. 不自动调参
3. 不保证诊断 100% 准确

## 4. Required Inputs

The skill expects:
- training log (.log/.txt)
- config file (.yaml/.json/.py)
- metrics table (.csv/.json)
- Git diff output (.diff/.patch)
- TensorBoard event files (optional)

### Example input files:
```
examples/input/
```

## 5. Expected Outputs

The skill produces:
- 实验诊断报告 (.md)
- 诊断摘要 JSON (.json)

### Example output structure:
1. Task summary
2. Key findings with evidence
3. Confidence levels per finding
4. Analysis / Diagnosis
5. Suggested next steps
6. Limitations

## 6. Workflow

1. 读取日志文件，解析 loss 曲线和异常点（NaN、发散）
2. 读取配置文件，提取关键超参数（lr, bs, optimizer, scheduler）
3. 读取指标表，对比多组实验的最终性能和趋势
4. 读取 Git diff，定位代码/配置变更
5. 综合分析各维度证据，定位最可能的失败根因
6. 生成诊断报告，含证据链、置信度和修复建议

## 7. Group-Specific Feature

将实验日志分析与 Git diff 和配置文件变更结合，实现实验溯因——不仅发现异常，还定位异常来自哪次变更

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

### How to Run
```bash
cd skills/experiment-diagnosis
python skills.py --input examples/input/
```

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| 根因定位率 | 能否正确识别导致实验失败的主要因素 |
| 证据完整性 | 诊断结论是否有日志行 / 配置项 / diff 行支撑 |
| 建议可操作性 | 修复建议是否具体到可执行 |

## 10. Limitations

- 日志解析依赖格式一致性，不同框架（PyTorch Lightning vs raw）需要不同解析器
- 无法访问训练数据，可能遗漏数据相关问题
- 对稀疏日志（每 epoch 仅记录一次）的诊断能力有限

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the task
- Store or expose personal data
- Fabricate results or references
- Claim HIGH confidence when evidence is insufficient

## 12. Future Improvements

- 支持 TensorBoard event 文件解析
- 增加 wandb / MLflow 集成
- 构建常见失败模式的规则库（梯度爆炸、过拟合、欠拟合）

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/experiment-diagnosis/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
