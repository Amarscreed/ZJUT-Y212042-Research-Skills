# LobsterCXR 论文编译与实验说明

## 文件结构

```
research/
├── paper_draft.md              # 中文完整论文（含占位数据）
├── paper_draft_en.md           # 英文完整论文
├── method_design.md            # 方法设计书（含完整伪代码）
├── lobstercxr_paper.tex        # LaTeX 可编译源文件 (MICCAI模板) ✓
├── lobstercxr_paper.pdf        # 编译输出 PDF ✓
├── lobstercxr_paper_zh.tex     # 中文版 LaTeX (xeCJK) ✓
├── lobstercxr_paper_zh.pdf     # 中文版 PDF ✓
├── llncs.cls                   # LNCS 模板
├── splncs04.bst                # BibTeX 样式
├── scripts/
│   └── generate_placeholders.py  # 占位图生成脚本
├── figures/
│   ├── architecture.mmd        # Mermaid 架构图源码
│   ├── ddx_chain.mmd           # Mermaid 鉴别思考链图源码
│   ├── architecture.png        # 占位架构图 ✓
│   └── ddx_chain.png           # 占位鉴别链图 ✓
└── experiments/                # 实验代码
    ├── configs/                 # YAML 配置文件
    ├── models/                  # 各 Agent 模型定义
    ├── utils/                   # 损失函数 & 评估指标
    ├── data/                    # 数据集模块
    ├── train_stage1.py          # 阶段1: Agent A+B 预训练 ✓
    ├── train_stage2.py          # 阶段2: Agent C 专业化训练 ✓
    ├── train_stage3.py          # 阶段3: 全系统联合微调 ✓
    └── evaluate.py              # 推理与评估 ✓
```

## 渲染 Mermaid 图

```bash
# 安装 Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# 渲染架构图
mmdc -i figures/architecture.mmd -o figures/architecture.png -t neutral -w 1200

# 渲染鉴别思考链
mmdc -i figures/ddx_chain.mmd -o figures/ddx_chain.png -t neutral -w 800
```

## 编译 LaTeX

```bash
# 需要安装 LaTeX (TeX Live / MiKTeX)
# 需要 LNCS 模板 (llncs.cls) — 从 Springer 官网下载

xelatex lobstercxr_paper.tex
bibtex lobstercxr_paper
xelatex lobstercxr_paper.tex
xelatex lobstercxr_paper.tex
```

## 实验运行

```bash
# Stage 1: Agent A+B 预训练
python experiments/train_stage1.py --config configs/stage1.yaml

# Stage 2: Agent C 专业化
python experiments/train_stage2.py --config configs/stage2.yaml

# Stage 3: 全系统联合微调
python experiments/train_stage3.py --config configs/stage3.yaml

# 推理与评估
python experiments/evaluate.py --checkpoint runs/best.pt
```
