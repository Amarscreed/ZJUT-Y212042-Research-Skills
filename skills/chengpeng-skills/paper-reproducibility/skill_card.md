# Skill Card: paper-reproducibility

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | paper-reproducibility |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 论文复现拆解 / Paper Reproduction |
| Target Users | 研究生、复现实验者、论文评审者 |
| GitHub 路径 | chengpeng-skills/paper-reproducibility/ |

## 2. Research Pain Point

读论文时想复现实验，但论文中常遗漏关键实现细节（网络结构具体层数、超参数搜索范围、预处理随机种子、硬件配置）。人工整理复现清单费时且容易遗漏。

## 3. What This Skill Does

### This skill can:
1. 解析论文 PDF 全文，提取方法描述和实验设置
2. 识别缺失的关键实现细节（网络结构、超参数、预处理、随机种子）
3. 检测实验基线、数据集和评估指标是否完整定义
4. 检查论文的代码和数据是否公开
5. 输出结构化复现清单，含缺失项标记和不确定性等级

### This skill does not aim to:
1. 不自动运行复现实验
2. 不判断论文结果的真实性
3. 不评估论文的写作质量

## 4. Required Inputs

The skill expects:
- 论文 PDF
- 补充材料 PDF
- 代码仓库 README 或链接

### Example input files:
```
examples/input/
```

## 5. Expected Outputs

The skill produces:
- 复现检查清单 (.md)
- 复现摘要 JSON (.json)

### Example output structure:
1. Task summary
2. Key findings with evidence
3. Confidence levels per finding
4. Analysis / Diagnosis
5. Suggested next steps
6. Limitations

## 6. Workflow

1. 解析论文 PDF，提取方法章节和相关工作
2. 识别缺失信息：数据集下载链接、预处理参数、超参数设置、随机种子、硬件配置
3. 检查实验设置：基线是否报告、消融是否完整、统计显著性是否报告
4. 检查可复现性要素：代码是否公开、README 是否完整
5. 生成复现清单，每个项目标注（FOUND / MISSING / UNCLEAR）
6. 汇总可复现性评分和优先补充项

## 7. Group-Specific Feature

系统地标注每个复现要素的状态（FOUND / MISSING / UNCLEAR），生成量化的可复现性评分，帮助用户优先补充最关键缺失信息

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

### How to Run
```bash
cd skills/paper-reproducibility
python skills.py --input examples/input/
```

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| 覆盖度 | 是否涵盖论文复现的所有关键要素 |
| 定位准确性 | 能否正确识别缺失信息的位置 |
| 评分合理性 | 可复现性评分是否反映实际复现难度 |

## 10. Limitations

- PDF 解析依赖文本提取质量，扫描版 PDF 可能无法解析
- 无法判断论文中的技术路线是否合理
- 缺失项的多寡不完全等同于复现难度

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the task
- Store or expose personal data
- Fabricate results or references
- Claim HIGH confidence when evidence is insufficient

## 12. Future Improvements

- 接入 PapersWithCode API 自动查找代码
- 支持代码仓库自动 Clone 和目录分析
- 增加不同领域（CV / NLP / Medical）的复现模板

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/paper-reproducibility/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
