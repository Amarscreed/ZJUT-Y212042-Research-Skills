# paper-reproducibility

## name
paper-reproducibility

## description
Deconstruct a paper from PDF into a structured reproduction checklist with critical implementation details.


### Real-world usage
This skill processes real LobsterCXR research files: 拆解 LobsterCXR 论文复现要素，含 19 个实验代码文件和完整训练流水线
## When to use this skill
- 论文复现拆解 / Paper Reproduction
- 当你遇到读论文时想复现实验，但论文中常遗漏关键实现细节（网络结构具体层数、超参数搜索范围...

## Inputs
paper-reproducibility expects one or more of the following inputs:
- 论文 PDF
- 补充材料 PDF
- 代码仓库 README 或链接

### Example input files:
```
examples/input/
├── paper.pdf
├── supplementary.pdf
└── code_repo.txt
```

## Workflow
1. 解析论文 PDF，提取方法章节和相关工作
2. 识别缺失信息：数据集下载链接、预处理参数、超参数设置、随机种子、硬件配置
3. 检查实验设置：基线是否报告、消融是否完整、统计显著性是否报告
4. 检查可复现性要素：代码是否公开、README 是否完整
5. 生成复现清单，每个项目标注（FOUND / MISSING / UNCLEAR）
6. 汇总可复现性评分和优先补充项

## Output format
paper-reproducibility produces:
- 复现检查清单 (.md)
- 复现摘要 JSON (.json)

### Example output structure:
1. Task summary
2. Key findings
3. Evidence source for each finding
4. Analysis / Diagnosis
5. Confidence levels (HIGH / MEDIUM / LOW)
6. Suggested next steps
7. Limitations

## Safety and limitations
- PDF 解析依赖文本提取质量，扫描版 PDF 可能无法解析
- 无法判断论文中的技术路线是否合理
- 缺失项的多寡不完全等同于复现难度

## Example trigger
- "读论文时想复现实验，但论文中常遗漏关键实现细节（网络结构具体层数、超参数搜索范围、预处理随机种子、硬..."

## Constraints
- All claims must be backed by evidence from input materials
- Clearly distinguish HIGH/MEDIUM/LOW confidence
- Do not fabricate findings not supported by inputs
