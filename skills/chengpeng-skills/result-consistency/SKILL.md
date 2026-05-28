# result-consistency

## name
result-consistency

## description
Cross-reference claims in the paper with experimental results in tables/figures to check for overclaiming, missing evidence, and numerical inconsistencies.


### Real-world usage
This skill processes real LobsterCXR research files: 对照 LobsterCXR 论文的 12 个声明与实验表格数值的一致性
## When to use this skill
- 结果一致性检查 / Result Consistency Check
- 当你遇到论文中常出现结论与实验结果不对应的情况：声称 SOTA 但表中不是最高、描述『显...

## Inputs
result-consistency expects one or more of the following inputs:
- 论文 .tex 或 PDF
- 实验结果表格文本（LaTeX tabular 或 CSV）

### Example input files:
```
examples/input/
├── paper.tex
├── paper.tex
└── code_repo.txt
```

## Workflow
1. 解析 .tex 文件，提取所有实验结果表格中的数值
2. 标记每个指标的 Top-1 / Top-2 / 基线等
3. 提取所有性能相关的 claim 语句（『优于』『SOTA』『最佳』等）
4. 将每个 claim 与对应表格中的实际排名进行对照
5. 检测不一致：声称 SOTA 但非最优、声称提升但无数字
6. 检测过度声明：语义超出数据支撑范围
7. 检查消融实验是否声称了非消融组件的效果
8. 输出声明-证据对照表 + 不一致性报告

## Output format
result-consistency produces:
- 声明-证据对照表 (.md)
- 不一致性报告 (.json)

### Example output structure:
1. Task summary
2. Key findings
3. Evidence source for each finding
4. Analysis / Diagnosis
5. Confidence levels (HIGH / MEDIUM / LOW)
6. Suggested next steps
7. Limitations

## Safety and limitations
- 对复杂的跨表引用（『见图 X』）解析能力有限
- 无法判断统计检验是否合理
- 对非数值型声明（『可视化结果表明』）无法验证

## Example trigger
- "论文中常出现结论与实验结果不对应的情况：声称 SOTA 但表中不是最高、描述『显著提升』但无统计检验..."

## Constraints
- All claims must be backed by evidence from input materials
- Clearly distinguish HIGH/MEDIUM/LOW confidence
- Do not fabricate findings not supported by inputs
