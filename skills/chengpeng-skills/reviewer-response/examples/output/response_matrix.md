# OpenClaw Research Skill 期末报告

## LobsterCXR: 多智能体 CXR 鉴别诊断与教学报告生成框架

---

## 1. Skill 基本信息

| 项目 | 内容 |
|------|------|
| Skill 名称 | LobsterCXR Research Skill Suite |
| 小组编号 | 课程项目（个人） |
| 小组成员 | 个人项目 |
| 所属科研场景 | 论文写作辅助、文献审计、审稿模拟、创新性评估、文献挖掘、投稿格式化、实验诊断、数据集审计、论文复现拆解、审稿回应、消融实验设计、结果一致性检查 |
| GitHub 路径 | skills/（包含 12 个子 skill） |

### Skill 总览

| 序号 | Skill 名称 | 科研环节 | 输入材料 | 输出结果 |
|:----:|-----------|---------|---------|---------|
| 1 | humanize-writing | 论文写作 | .tex 文件 | 修改后 .tex + 差异报告 |
| 2 | reference-verifier | 文献审计 | .tex / .bib 文件 | 验证报告 .md + .json |
| 3 | reviewer-simulator | 投稿准备 | .tex 文件 | 审稿报告 + 5 维评分 |
| 4 | novelty-checker | 创新性评估 | .tex 文件 | 评估报告 .md + .json |
| 5 | literature-miner | 文献调研 | .tex + 关键词 | 文献报告 + 增强建议 |
| 6 | submission-formatter | 投稿格式化 | .tex 文件 | 格式化后 .tex + 报告 |
| **7** | **experiment-diagnosis** | **实验诊断** | **日志 + config + metrics + git diff** | **诊断报告 + 根因分析** |
| **8** | **dataset-auditor** | **数据集审计** | **元数据 + 目录结构 + 预处理脚本** | **审计报告 + 风险标记** |
| **9** | **paper-reproducibility** | **论文复现拆解** | **论文 PDF + 补充材料** | **复现检查清单 + 缺失项** |
| **10** | **reviewer-response** | **审稿回应** | **审稿意见 + 论文 .tex** | **证据-回复矩阵** |
| **11** | **ablation-designer** | **消融实验设计** | **方法描述 + GPU 预算** | **设计表 + 优先级排序** |
| **12** | **result-consistency** | **结果一致性检查** | **.tex + 实验数据表** | **声明-证据对照表** |

---

## 2. 这个 Skill 解决什么科研问题？

### 2.1 问题出现的科研环节

本 Skill Suite 覆盖了**从论文写作到最终投稿发表**的完整科研论文生产链。12 个 Skill 对应 12 个具体的高频痛点环节：

| 环节 | Skill | 具体痛点 |
|------|-------|---------|
| **写作阶段** | humanize-writing | AI 生成文本有 AI 味、过度 hedging、公式化过渡 |
| **文献调研** | literature-miner | 阅读大量最新顶会论文时间有限，可能遗漏重要工作 |
| **实验阶段** | experiment-diagnosis | 训练失败或性能异常，难以快速定位根因 |
| **数据准备** | dataset-auditor | 公开数据集可能存在患者泄露、分布偏移、标签不均 |
| **方法设计** | ablation-designer | 不知道哪些模块需要消融、如何设计对比实验 |
| **论文写作** | submission-formatter | 不同会议格式不同，手动调整容易出错 |
| **文献审计** | reference-verifier | LLM 可能编造参考文献，人工逐条核查费时 |
| **结果检查** | result-consistency | 论文声明的结论与表格数据可能不一致 |
| **复现验证** | paper-reproducibility | 论文常遗漏关键实现细节，复现困难 |
| **创新评估** | novelty-checker | 缺少客观的贡献评估工具 |
| **投稿准备** | reviewer-simulator | 投稿前无法预知审稿人反馈 |
| **审稿回应** | reviewer-response | 收到审稿意见后，组织回复耗时且容易遗漏 |

### 2.2 研究生为什么会遇到这些问题？

1. **AI 辅助写作的双刃剑**：LLM 能快速生成论文初稿，但输出有明显的 AI 味，需要大量人工润色
2. **论文生产环节多**：从实验到投稿涉及数据、代码、论文、审稿多个环节，每个环节都有重复性工作
3. **资源有限**：GPU 预算有限，需要精打细算设计实验；一个人无法读完全部相关论文
4. **经验不足**：研究生第一次投稿，不知道审稿人会关注哪些方面
5. **格式要求多**：每个会议/期刊模板不同，格式调整工作重复性高

### 2.3 没有 Skill 时需要做的重复性工作

- humanize-writing → 逐句检查并修改 AI 味表达
- reference-verifier → 逐条核对参考文献 venue 和年份
- reviewer-simulator → 找学长/导师预审并等待反馈
- novelty-checker → 凭感觉评估论文创新性
- experiment-diagnosis → 手动翻日志、对比 config、查 diff
- dataset-auditor → 手写 Python 脚本检查数据泄露
- paper-reproducibility → 手动整理缺失的实现细节
- ablation-designer → 凭经验猜测需要哪些消融实验

### 2.4 输入和输出是否明确？

**是。每个 Skill 都有明确的输入规范和输出标准。**

| Skill | 输入 | 格式 | 输出 | 格式 |
|-------|------|------|------|------|
| experiment-diagnosis | 训练日志 + config + metrics + git diff | .log/.txt/.yaml/.csv/.patch | 诊断报告 + 根因分析 | .md + .json |
| dataset-auditor | 元数据 + 目录结构 + 预处理脚本 | .csv/.txt/.py | 审计报告 + 风险标记 | .md + .json |
| paper-reproducibility | 论文 PDF + 补充材料 | .pdf | 复现检查清单 | .md |
| reviewer-response | 审稿意见 + 论文 .tex | .txt + .tex | 证据-回复矩阵 | .md/.csv |
| ablation-designer | 方法描述 + GPU 预算 | .md/.txt | 消融实验设计表 | .md + .json |
| result-consistency | 论文 .tex + 实验数据表 | .tex + .csv | 声明-证据对照表 | .md + .json |

---

## 3. 它和普通 ChatGPT 问答有什么区别？

### 3.1 核心对比

| 对比项 | 普通 ChatGPT 问答 | 本 Skill Suite |
|--------|-----------------|----------------|
| **任务目标** | 临时回答一个问题 | 固化 12 个科研流程 |
| **输入材料** | 用户随意描述 | 严格要求 .tex / .log / .csv / .yaml / .pdf 等结构化输入 |
| **分析流程** | 不固定，取决于聊天上下文 | 每个 Skill 有固定步骤，可复现 |
| **输出格式** | 不稳定，每次可能不同 | 有规定结构（结构化报告 + JSON） |
| **可复用性** | 依赖用户提问能力 | 其他同学可直接一键运行 |
| **可验证性** | 较弱，输出难以追溯 | 每条结论标注证据来源、置信度、行号 |
| **结果回溯** | 聊天记录难以复用 | 输出文件可保存、分享、复查 |
| **流程固化** | 每次都要从头描述问题 | Skill 封装了完整的分析流程 |
| **领域特化** | 通用知识，不针对特定领域 | 专门针对医学影像 AI 研究设计 |

### 3.2 本 Skill Suite 的核心价值

本 Skill Suite 的价值**不在于"让大模型回答得更漂亮"**，而在于：

1. **把 12 个高频科研任务转化为标准化、可复用、可检查的智能体能力**
2. **每个 Skill 都有一致的输入规范、固定的分析流程、标准化的输出格式和内置的证据检查机制**
3. **Skill 之间可以串联使用** — 例如 experiment-diagnosis 的输出可以作为 novelty-checker 的输入，forming a research quality assurance pipeline

### 3.3 为什么不是普通的 prompt 工程？

普通的 prompt 工程是：「帮我分析这个日志文件」。问题是：
- 日志格式千变万化，每次都要重新描述
- 输出格式不固定，难以批次处理
- 没有证据检查机制，可能产生幻觉

而一个 Skill：
- 封装了日志解析器、规则引擎、证据检查机制
- 输出格式标准化，支持批量和自动化
- 每条结论标记置信度和证据来源

---

## 4. 它的输出怎么验证？

### 4.1 证据列设计

每个 Skill 的输出都包含标准化的"证据列"：

```
| 结论 | 证据来源 | 置信度 | 是否需要人工确认 |
|------|---------|--------|----------------|
| 学习率可能过大 | config 中 lr=1e-3；epoch 8 后 loss 变为 NaN | HIGH | 否 |
| 数据泄露 | patient P001 同时出现在 train 和 test 中 | HIGH | 否 |
| 随机种子未报告 | 论文实验章节未提及种子设置 | HIGH | 是，需检查补充材料 |
| 声明 SOTA 但表中非最优 | Table 1: 基线 B 的准确率 90.1% > 本文 89.5% | HIGH | 否 |
```

### 4.2 置信度等级

| 等级 | 含义 | 示例 |
|------|------|------|
| **HIGH** | 有明确的输入材料证据支持 | 「config 中 lr=1e-3」|
| **MEDIUM** | 有间接证据，但需交叉验证 | 「loss 曲线异常，可能与数据增强有关」|
| **LOW** | 推测性结论，无直接证据 | 「可能是模型容量不够」|

### 4.3 验证方法

1. **证据可追溯** — 每条结论标注了对应的输入文件、行号或配置项
2. **区分确定与推测** — 通过置信度标签（HIGH / MEDIUM / LOW）明确区分
3. **提供 Demo 用例** — 每个 Skill 都有 examples/input/ 和 examples/output/
4. **可复查** — 老师或同学可以根据原始输入材料复查输出结论
5. **不自创事实** — Skill 不会编造不存在的文献或实验结果
6. **多 Skill 交叉验证** — 一个 Skill 的输出可作为另一个 Skill 的检查依据

---

## 5. 输入、输出和工作流程

### 5.1 输入材料（完整列表）

| Skill | 输入材料 | 格式 |
|-------|---------|------|
| humanize-writing | 论文源文件 | .tex |
| reference-verifier | 论文源文件 / 引用库 | .tex / .bib |
| reviewer-simulator | 论文源文件 | .tex |
| novelty-checker | 论文源文件 | .tex |
| literature-miner | 论文源文件 + 搜索关键词 | .tex + string |
| submission-formatter | 论文源文件 | .tex |
| **experiment-diagnosis** | 训练日志 + 配置文件 + 指标表格 + Git diff | .log/.txt/.yaml/.csv/.patch |
| **dataset-auditor** | 元数据表 + 目录结构 + 预处理脚本 + 图像样本 | .csv/.txt/.py/.png |
| **paper-reproducibility** | 论文 PDF + 补充材料 PDF + 代码链接 | .pdf + .txt |
| **reviewer-response** | 审稿意见 + 论文源文件 + 编辑决策信件 | .txt + .tex |
| **ablation-designer** | 方法描述 + GPU 预算 + 现有实验结果 | .md/.txt |
| **result-consistency** | 论文源文件 + 实验结果数据表 | .tex + .csv |

### 5.2 输出结果（完整列表）

| Skill | 输出 | 格式 |
|-------|------|------|
| humanize-writing | 修改后论文 + 差异对比报告 | .tex + .md |
| reference-verifier | 引用验证报告 | .md + .json |
| reviewer-simulator | 审稿报告 + 5 维评分 | .md |
| novelty-checker | 创新评估报告 + 证据列表 | .md + .json |
| literature-miner | 文献挖掘报告 + 增强建议 | .md |
| submission-formatter | 格式化后论文 + 修改报告 | .tex + .md |
| **experiment-diagnosis** | **实验诊断报告 + 根因分析** | **.md + .json** |
| **dataset-auditor** | **数据集审计报告 + 风险等级标记** | **.md + .json** |
| **paper-reproducibility** | **复现检查清单 + 缺失项标记** | **.md** |
| **reviewer-response** | **审稿意见证据矩阵 + 回复草稿** | **.md/.csv** |
| **ablation-designer** | **消融实验设计表 + 优先级排序** | **.md + .json** |
| **result-consistency** | **声明-证据对照表 + 不一致性报告** | **.md + .json** |

### 5.3 工作流程（通用框架）

所有 Skill 遵循以下标准化工作流：

```
Step 1: 识别用户任务
  → 判断用户需要哪个 Skill 处理什么科研任务

Step 2: 解析输入材料
  → 读取指定格式的输入文件（.tex / .log / .csv / .pdf / .txt）
  → 提取与任务相关的关键信息

Step 3: 抽取任务相关证据
  → 从输入材料中定位与任务相关的证据项
  → 记录证据来源（行号、文件名、配置项）

Step 4: 执行结构化分析
  → 按 Skill 特定的规则引擎进行分析
  → 区分事实性结论和推断性结论

Step 5: 生成标准化输出
  → 按预定义的输出格式生成报告
  → 每条结论标注证据来源和置信度

Step 6: 证据链检查
  → 检查每条结论是否有输入材料中的直接证据支撑
  → 无直接证据的结论降级为 LOW 置信度

Step 7: 标注不确定性和局限性
  → 明确区分 HIGH / MEDIUM / LOW 置信度
  → 说明需要人工确认的项目
```

---

## 6. 本组特色设计

### 6.1 核心特色

#### 特色 1: 覆盖科研全流程
12 个 Skill 覆盖从实验设计 → 数据准备 → 论文写作 → 文献调研 → 投稿准备 → 审稿回应的整条科研论文生产链。这是单一 Skill 无法做到的。

#### 特色 2: 多样化的输入输出类型
输入类型涵盖 .tex / .log / .csv / .yaml / .patch / .pdf / .txt，不局限于论文文本。这种多样性使其能真正融入科研工作流。

#### 特色 3: 证据链检查机制
每个 Skill 的输出都有标准化的证据列：
- 证据来源 → 可追溯
- 置信度 → 区分确定与推测
- 是否需要人工确认 → 明确告知

#### 特色 4: 领域特化
所有 Skill 围绕医学影像 AI 这个具体领域设计：
- CXR 报告生成术语库
- CheXpert / MIMIC-CXR 数据集的自动审计模板
- MICCAI / MedIA 审稿标准和评分规则
- 20 篇 2025-2026 顶会/顶刊论文数据库

#### 特色 5: 双语言 + 完整镜像
所有 Skill 文件均有中英文版本：
- `skills/` — 英文版
- `skills_en/` — 中文版（完全镜像的目录结构）

### 6.2 Skill 间协作示例

```
实验阶段: experiment-diagnosis + dataset-auditor + ablation-designer
  → 诊断实验问题 → 审计数据质量 → 设计消融实验

论文写作: humanize-writing + result-consistency + novelty-checker
  → 润色语言 → 检查声明-数据一致性 → 评估创新性

投稿准备: reference-verifier + reviewer-simulator + reviewer-response
  → 验证引用 → 模拟审稿 → 准备回应

文献调研: literature-miner + paper-reproducibility
  → 发现相关论文 → 拆解复现细节
```

---

## 7. Demo 展示

### 7.1 Demo 输入

使用 LobsterCXR 论文（`research/lobstercxr_paper.tex`）作为测试材料：

```bash
# 1. 实验诊断（模拟日志）
cd skills/experiment-diagnosis
python skills.py --input examples/input/

# 2. 数据集审计
cd skills/dataset-auditor
python skills.py --input examples/input/

# 3. 论文复现拆解
cd skills/paper-reproducibility
python skills.py --input "..\..\research\lobstercxr_paper.tex"

# 4. 结果一致性检查
cd skills/result-consistency
python skills.py --input "..\..\research\lobstercxr_paper.tex"

# 5. 消融实验设计
cd skills/ablation-designer
python skills.py --input examples/input/

# 6. 审稿回应
cd skills/reviewer-response
python skills.py --input examples/input/
```

### 7.2 Demo 输出

| Skill | 输出文件 | 核心发现 |
|-------|---------|---------|
| experiment-diagnosis | report.md | NaN at epoch 9, likely lr too high |
| dataset-auditor | report.md | CRITICAL: patient P001 in both train and test |
| paper-reproducibility | report.md | 5/10 score, missing: random seed, hardware |
| result-consistency | report.md | 1 overclaim found (SOTA without evidence) |
| ablation-designer | report.md | 8 variants prioritized within 48h budget |
| reviewer-response | report.md | 3 reviewers, 8 comments, 6 CRITICAL items |
| humanize-writing | .tex + diff.md | 21 humanization edits applied |
| reference-verifier | report.md + .json | 21 references, all verified |
| reviewer-simulator | report.md | ~3.8/5, Weak Accept |
| novelty-checker | report.md + .json | 4/3/5/3/4 scores |
| literature-miner | report.md | 13 papers found, 7 suggestions |

### 7.3 Demo 结果分析

- **任务理解正确** — 每个 Skill 正确解析了输入文件并提取了关键信息
- **输出结构清晰** — 所有输出均为结构化 Markdown 报告，含证据列
- **置信度标注合理** — HIGH / MEDIUM / LOW 标签与证据强度匹配
- **存在需要人工确认的项** — 如 `MISSING EVIDENCE` 标记的项目

---

## 8. 局限性和改进方向

### 8.1 当前局限性

1. **对输入材料质量依赖** — 输入文件不完整或格式不规范时，Skill 只能给出 LOW 置信度判断
2. **领域知识有限** — 虽然特化于医学影像，但对高度专业化的影像发现仍需人工判断
3. **Demo 样例有限** — 当前使用 LobsterCXR 论文作为主测试材料，尚未覆盖复杂异常情况
4. **无连网验证** — reference-verifier 和 literature-miner 基于本地规则，未连接学术 API
5. **无实时更新** — literature-miner 的论文数据库需要手动更新
6. **评分基于规则** — reviewer-simulator 和 novelty-checker 的评分基于统计规则而非语义理解
7. **无自动评测** — 缺少标准测试集来衡量 Skill 的准确率和召回率

### 8.2 改进方向

1. **接入学术 API** — 连接 Semantic Scholar / CrossRef / OpenAlex 实现引用实时验证
2. **自动化评测平台** — 构建标准测试集，自动验证每个 Skill 的准确率和召回率
3. **多论文对比** — 支持多篇论文同时比较（文献定位、方法对比）
4. **Git 集成** — 自动读取 Git diff 跟踪论文修改历史和实验变更
5. **Web UI** — 构建可视化界面降低使用门槛
6. **LLM 增强评分** — 使用 LLM 替代规则引擎提高 reviewer-simulator 和 novelty-checker 的评分质量
7. **跨 Skill 编排** — 支持自动串联多个 Skill 形成完整工作流

---

## 9. GitHub 提交说明

### 提交文件结构

```
skills/                          # 英文版 Skill 目录
├── humanize-writing/            # Skill 1: 论文 AI 味消除
│   ├── SKILL.md                 # 使用说明
│   ├── skill_card.md            # 信息卡片
│   ├── skills.py                # 实现代码
│   ├── references/              # 参考资料
│   ├── scripts/                 # 工具脚本
│   └── examples/
│       ├── input/               # 示例输入
│       └── output/              # 示例输出
├── reference-verifier/          # Skill 2: 引用验证
├── reviewer-simulator/          # Skill 3: 审稿模拟
├── novelty-checker/             # Skill 4: 创新评估
├── literature-miner/            # Skill 5: 文献挖掘
├── submission-formatter/        # Skill 6: 投稿格式化
├── experiment-diagnosis/        # Skill 7: 实验诊断  [新增]
├── dataset-auditor/             # Skill 8: 数据集审计 [新增]
├── paper-reproducibility/       # Skill 9: 论文复现    [新增]
├── reviewer-response/           # Skill 10: 审稿回应   [新增]
├── ablation-designer/           # Skill 11: 消融设计   [新增]
└── result-consistency/          # Skill 12: 结果一致性 [新增]

skills_en/                       # 中文版 Skill 目录（完全镜像）
├── humanize-writing/
├── reference-verifier/
├── ...
└── result-consistency/
```

Pull Request 链接：**（待提交）**

---

## 10. 总结

### 本组 Skill 解决了什么问题？

本组构建了 **12 个相互关联的 Research Skill**，面向医学影像 AI 论文研究的全生命周期：
- **写作阶段**：humanize-writing → 消除 AI 味
- **实验阶段**：experiment-diagnosis → 诊断实验失败原因；dataset-auditor → 审计数据质量问题；ablation-designer → 规划消融实验
- **论文写作**：result-consistency → 检查声明与数据是否一致；novelty-checker → 评估创新性
- **文献调研**：literature-miner → 发现相关顶会论文；paper-reproducibility → 拆解复现细节
- **投稿周期**：reference-verifier → 验证引用；reviewer-simulator → 模拟审稿；reviewer-response → 组织审稿回应；submission-formatter → 调整格式

### 它为什么不是普通 ChatGPT 问答？

1. **规范化输入** — 不是用户自由描述，而是严格要求 .tex / .log / .csv / .yaml / .pdf 等结构化文件
2. **固定分析流程** — 每个 Skill 有 7 步标准工作流，可复现
3. **结构化输出** — 标准化 Markdown + JSON 双格式输出
4. **证据可追溯** — 每条结论标注文件位置、行号、置信度
5. **可复用** — 其他同学可直接一键运行，无需重新描述问题
6. **领域特化** — 面向医学影像 AI 领域，非通用问答

### 它如何保证输出可验证？

- **证据列** — 每条结论标注输入文件位置和置信度（HIGH / MEDIUM / LOW）
- **区分确定与推测** — 置信度标签明确告知哪些是确定结论、哪些需要人工确认
- **Demo 可复查** — 每个 Skill 提供示例输入/输出供复查
- **不自创事实** — 无证据支撑的结论不会伪装为事实
- **多 Skill 交叉验证** — 可以通过多个 Skill 从不同角度验证同一结论

### 后续还能怎样扩展？

- 接入学术 API 实现引用实时验证和自动更新
- 构建 Web UI 降低使用门槛
- 增加自动评测脚本和标准测试集
- 支持跨论文对比分析和多轮迭代优化
- 集成到 CI/CD 工作流，实现论文质量自动检查

---

*报告生成日期：2026-05-28*
*项目仓库：https://github.com/YOUR_REPO/lobstercxr（待提交）*
