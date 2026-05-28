# Skill Card: dataset-auditor

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | dataset-auditor |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 数据集审计 / Dataset Audit |
| Target Users | 研究生、实验者、数据集构建者 |
| GitHub 路径 | chengpeng-skills/dataset-auditor/ |

## 2. Research Pain Point

医学影像数据集从公开网站下载后，常存在患者重叠（data leakage）、标签分布不均、train/test 分布偏移等问题。人工审计需要写大量 Python 脚本，领域知识要求高。

## 3. What This Skill Does

### This skill can:
1. 检查患者级数据泄露（同一患者在不同 split 中出现）
2. 分析标签分布（长尾、缺失、不平衡度）
3. 检查 train/test 集的属性分布偏移（年龄、性别、设备型号）
4. 验证预处理流程一致性（图像尺寸、归一化参数）
5. 输出结构化审计报告，含风险等级标记

### This skill does not aim to:
1. 不自动修复数据问题
2. 不重新划分数据集
3. 不提供数据增强建议

## 4. Required Inputs

The skill expects:
- 数据集目录结构 (file listing .txt/.csv)
- 元数据文件 (.csv/.json, 含 patient_id, label, demographic)
- 数据加载脚本 (.py, 预处理流程)
- 图像样本 (少量抽样以验证预处理)
- 数据集 README / 论文 PDF (含数据划分描述)

### Example input files:
```
examples/input/
```

## 5. Expected Outputs

The skill produces:
- 数据集审计报告 (.md)
- 审计摘要 JSON (.json)

### Example output structure:
1. Task summary
2. Key findings with evidence
3. Confidence levels per finding
4. Analysis / Diagnosis
5. Suggested next steps
6. Limitations

## 6. Workflow

1. 读取目录结构，验证 split 文件分布
2. 解析元数据，检查 patient_id 在不同 split 中是否有重叠
3. 统计标签分布，计算不平衡度和长尾指标
4. 对比 train/test 的人口统计学属性分布
5. 读取预处理脚本，提取图像尺寸、归一化参数
6. 抽样检查预处理后的图像，验证一致性
7. 汇总风险等级（CRITICAL / WARNING / INFO）
8. 输出审计报告

## 7. Group-Specific Feature

专门针对医学影像数据集设计，自动检测患者级数据泄露（同一患者在不同 split）——这是医学 AI 中最常见但最容易被忽略的问题

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

### How to Run
```bash
cd skills/dataset-auditor
python skills.py --input examples/input/
```

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| 泄露检测率 | 能否发现已知的患者级数据泄露 |
| 分布偏移检测 | 能否正确识别 train/test 分布差异 |
| 标签分析深度 | 不平衡度报告是否包含 actionable 指标 |

## 10. Limitations

- 需要用户提供 patient_id 列才能检测患者级泄露
- 无法自动识别所有的预处理问题
- 对无结构化的数据集（纯目录、无元数据）审计能力有限

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the task
- Store or expose personal data
- Fabricate results or references
- Claim HIGH confidence when evidence is insufficient

## 12. Future Improvements

- 集成医学影像格式解析（DICOM header, NIfTI）
- 支持 CheXpert / MIMIC-CXR / NIH ChestX-ray 等标准数据集的自动审计模板
- 增加数据增强策略合理性评估

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/dataset-auditor/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
