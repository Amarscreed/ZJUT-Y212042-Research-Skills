# dataset-auditor

## name
dataset-auditor

## description
Audit medical imaging datasets for data leakage, train/test distribution shift, label imbalance, and preprocessing consistency.


### Real-world usage
This skill processes real LobsterCXR research files: 审计 LobsterCXR 所用数据集（MIMIC-CXR / IU X-Ray / CheXpert Plus）
## When to use this skill
- 数据集审计 / Dataset Audit
- 当你遇到医学影像数据集从公开网站下载后，常存在患者重叠（data leakage）、标签...

## Inputs
dataset-auditor expects one or more of the following inputs:
- 数据集目录结构 (file listing .txt/.csv)
- 元数据文件 (.csv/.json, 含 patient_id, label, demographic)
- 数据加载脚本 (.py, 预处理流程)
- 图像样本 (少量抽样以验证预处理)
- 数据集 README / 论文 PDF (含数据划分描述)

### Example input files:
```
examples/input/
├── metadata.csv
├── dataset_structure.txt
└── data_loader.py
```

## Workflow
1. 读取目录结构，验证 split 文件分布
2. 解析元数据，检查 patient_id 在不同 split 中是否有重叠
3. 统计标签分布，计算不平衡度和长尾指标
4. 对比 train/test 的人口统计学属性分布
5. 读取预处理脚本，提取图像尺寸、归一化参数
6. 抽样检查预处理后的图像，验证一致性
7. 汇总风险等级（CRITICAL / WARNING / INFO）
8. 输出审计报告

## Output format
dataset-auditor produces:
- 数据集审计报告 (.md)
- 审计摘要 JSON (.json)

### Example output structure:
1. Task summary
2. Key findings
3. Evidence source for each finding
4. Analysis / Diagnosis
5. Confidence levels (HIGH / MEDIUM / LOW)
6. Suggested next steps
7. Limitations

## Safety and limitations
- 需要用户提供 patient_id 列才能检测患者级泄露
- 无法自动识别所有的预处理问题
- 对无结构化的数据集（纯目录、无元数据）审计能力有限

## Example trigger
- "医学影像数据集从公开网站下载后，常存在患者重叠（data leakage）、标签分布不均、train..."

## Constraints
- All claims must be backed by evidence from input materials
- Clearly distinguish HIGH/MEDIUM/LOW confidence
- Do not fabricate findings not supported by inputs
