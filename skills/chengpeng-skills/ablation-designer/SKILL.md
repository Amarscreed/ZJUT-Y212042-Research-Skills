# ablation-designer

## name
ablation-designer

## description
Design comprehensive ablation experiments based on a paper's method description and baseline comparisons, with GPU budget constraints.


### Real-world usage
This skill processes real LobsterCXR research files: 基于 LobsterCXR 的 6 个组件设计 8 个消融变体，按 GPU 预算排序
## When to use this skill
- 消融实验设计 / Ablation Design
- 当你遇到写论文时需要设计消融实验来验证每个模块的贡献，但不知道：哪些模块需要消融、基线怎...

## Inputs
ablation-designer expects one or more of the following inputs:
- 论文 .tex 或 PDF（含方法描述）
- GPU 预算描述（小时数或数量）
- 当前实验结果表（可选）

### Example input files:
```
examples/input/
├── method_section.md
├── paper.tex
└── code_repo.txt
```

## Workflow
1. 解析方法章节，提取模块化组件列表
2. 构建组件依赖图（哪些组件可以独立 / 组合消融）
3. 设计消融变体：去除/替换/增强每种组件
4. 检查现有实验是否覆盖了关键消融组合
5. 根据 GPU 预算对消融实验排序（优先级、预计耗时、预期信息量）
6. 生成消融实验设计表和父/子实验关系树

## Output format
ablation-designer produces:
- 消融实验设计表 (.md)
- 优先级排序 (.json)

### Example output structure:
1. Task summary
2. Key findings
3. Evidence source for each finding
4. Analysis / Diagnosis
5. Confidence levels (HIGH / MEDIUM / LOW)
6. Suggested next steps
7. Limitations

## Safety and limitations
- 消融实验的价值高度依赖问题领域
- 无法预测消融实验的具体结果
- 预算估算基于经验公式，实际耗时可能有出入

## Example trigger
- "写论文时需要设计消融实验来验证每个模块的贡献，但不知道：哪些模块需要消融、基线怎么选、在有限的 GP..."

## Constraints
- All claims must be backed by evidence from input materials
- Clearly distinguish HIGH/MEDIUM/LOW confidence
- Do not fabricate findings not supported by inputs
