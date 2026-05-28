# Skill Card: ablation-designer

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | ablation-designer |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 消融实验设计 / Ablation Design |
| Target Users | 研究生、实验设计者、论文作者 |
| GitHub 路径 | chengpeng-skills/ablation-designer/ |

## 2. Research Pain Point

写论文时需要设计消融实验来验证每个模块的贡献，但不知道：哪些模块需要消融、基线怎么选、在有限的 GPU 预算下如何优先级排序。

## 3. What This Skill Does

### This skill can:
1. 解析论文的方法章节，提取模块化组件
2. 分析不同组件之间的依赖关系
3. 根据 GPU 预算生成消融实验优先级排序
4. 检查现有实验是否遗漏关键的消融组合
5. 输出消融实验设计表

### This skill does not aim to:
1. 不自动运行消融实验
2. 不保证每个消融组合都有意义
3. 不提供统计显著性测试

## 4. Required Inputs

The skill expects:
- 论文 .tex 或 PDF（含方法描述）
- GPU 预算描述（小时数或数量）
- 当前实验结果表（可选）

### Example input files:
```
examples/input/
```

## 5. Expected Outputs

The skill produces:
- 消融实验设计表 (.md)
- 优先级排序 (.json)

### Example output structure:
1. Task summary
2. Key findings with evidence
3. Confidence levels per finding
4. Analysis / Diagnosis
5. Suggested next steps
6. Limitations

## 6. Workflow

1. 解析方法章节，提取模块化组件列表
2. 构建组件依赖图（哪些组件可以独立 / 组合消融）
3. 设计消融变体：去除/替换/增强每种组件
4. 检查现有实验是否覆盖了关键消融组合
5. 根据 GPU 预算对消融实验排序（优先级、预计耗时、预期信息量）
6. 生成消融实验设计表和父/子实验关系树

## 7. Group-Specific Feature

引入 GPU 预算约束和优先级排序，帮助用户在有限资源下选择信息量最大的消融实验组合

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

### How to Run
```bash
cd skills/ablation-designer
python skills.py --input examples/input/
```

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| 覆盖度 | 消融变体是否覆盖所有核心组件 |
| 优先级合理性 | 在预算约束下的优先级排序是否有逻辑依据 |
| 依赖图正确性 | 组件依赖关系是否与论文描述一致 |

## 10. Limitations

- 消融实验的价值高度依赖问题领域
- 无法预测消融实验的具体结果
- 预算估算基于经验公式，实际耗时可能有出入

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the task
- Store or expose personal data
- Fabricate results or references
- Claim HIGH confidence when evidence is insufficient

## 12. Future Improvements

- 接入超参数搜索框架（Optuna / Ray Tune）
- 增加统计功效分析
- 支持多轮迭代的实验设计更新

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/ablation-designer/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
