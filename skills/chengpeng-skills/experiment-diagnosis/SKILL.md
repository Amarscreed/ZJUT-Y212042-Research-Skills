# experiment-diagnosis

## name
experiment-diagnosis

## description
Analyze training logs, config files, and metric tables to diagnose why an experiment failed or why a change affected performance.


### Real-world usage
This skill processes real LobsterCXR research files: 诊断实验代码结构和配置合理性，识别潜在训练问题
## When to use this skill
- 实验诊断 / Experiment Diagnosis
- 当你遇到训练实验跑完后，性能不达标或出现 NaN，但很难快速定位是学习率、数据划分、模型...

## Inputs
experiment-diagnosis expects one or more of the following inputs:
- training log (.log/.txt)
- config file (.yaml/.json/.py)
- metrics table (.csv/.json)
- Git diff output (.diff/.patch)
- TensorBoard event files (optional)

### Example input files:
```
examples/input/
├── training_log.txt
├── config.yaml
└── metrics.csv
```

## Workflow
1. 读取日志文件，解析 loss 曲线和异常点（NaN、发散）
2. 读取配置文件，提取关键超参数（lr, bs, optimizer, scheduler）
3. 读取指标表，对比多组实验的最终性能和趋势
4. 读取 Git diff，定位代码/配置变更
5. 综合分析各维度证据，定位最可能的失败根因
6. 生成诊断报告，含证据链、置信度和修复建议

## Output format
experiment-diagnosis produces:
- 实验诊断报告 (.md)
- 诊断摘要 JSON (.json)

### Example output structure:
1. Task summary
2. Key findings
3. Evidence source for each finding
4. Analysis / Diagnosis
5. Confidence levels (HIGH / MEDIUM / LOW)
6. Suggested next steps
7. Limitations

## Safety and limitations
- 日志解析依赖格式一致性，不同框架（PyTorch Lightning vs raw）需要不同解析器
- 无法访问训练数据，可能遗漏数据相关问题
- 对稀疏日志（每 epoch 仅记录一次）的诊断能力有限

## Example trigger
- "训练实验跑完后，性能不达标或出现 NaN，但很难快速定位是学习率、数据划分、模型结构还是代码改动导致..."

## Constraints
- All claims must be backed by evidence from input materials
- Clearly distinguish HIGH/MEDIUM/LOW confidence
- Do not fabricate findings not supported by inputs
