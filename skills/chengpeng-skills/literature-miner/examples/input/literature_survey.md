# LobsterCXR 文献综述
## Chest X-ray 多模态诊断报告生成与教学评估

> 检索范围：2023–2025，兼顾 2022 及 2026 的高关联度工作
> 所有论文均通过 arXiv API / 官方来源核实 ID
> 引用计数因 Google Scholar 访问受限暂缺，以会议/期刊等级替代

---

## 📂 文献库目录结构

```
research/papers/
├── 01_foundations/       # R2Gen, ViT, CLIP 等基础工作
├── 02_report_gen/        # 2023-2025 CXR 报告生成 SOTA
├── 03_multimodal_vlp/    # 视觉-语言预训练模型
├── 04_multi_agent/       # 多智能体医学AI
├── 05_teaching_edu/      # 教学与教育评估
├── 06_evaluation_metrics/# 评估指标
├── 07_datasets/          # 数据集相关
└── lit_review.csv        # 文献汇总表
```

---

## 一、CXR 报告生成 SOTA（2023–2025）

### 1. RaDialog: A Large Vision-Language Model for Radiology Report Generation and Conversational Assistance
| 字段 | 内容 |
|------|------|
| **作者/年份** | Pellegrini et al., 2023 |
| **出处** | arXiv:2311.18681 → MICCAI 2024? |
| **数据集** | MIMIC-CXR, IU X-Ray |
| **核心方法** | 将视觉特征 + 结构化病理发现注入 LLM（基于 Vicuna-7B/13B），用 LoRA 参数高效微调。同时构建半自动标注的对话数据集，保留 LLM 的交互能力。 |
| **创新点** | 第一个同时支持报告生成 + 交互式对话的通用 radiology VLM |
| **关键模型** | Vicuna-7B/13B, LoRA, CLIP vision encoder |
| **与我们的区别** | ❌ 单模型架构，无多 Agent 协同；❌ 无教学评估维度；✅ 对话能力可作为我们 Teaching Agent 的参考基线 |

---

### 2. CheXagent: A Vision-Language Foundation Model to Enhance Efficiency of Chest X-ray Interpretation
| 字段 | 内容 |
|------|------|
| **作者/年份** | Chen et al., 2024 |
| **出处** | arXiv:2401.12208 → Nature Biomedical Engineering 2025? |
| **数据集** | 构建了 CheXinstruct 大规模指令数据集 + CheXbench 评估基准 |
| **核心方法** | 在 28 个公开 CXR 数据集上训练多模态 LLM，统一了报告生成、VQA、分类、查找等多任务。临床评估显示：住院医生使用 CheXagent 草稿后节省 36% 时间。 |
| **创新点** | 最大规模 CXR 多任务 VLM；首个包含临床时间节省评估 |
| **关键模型** | 基于 CLIP + LLM 的 MLLM 架构 |
| **与我们的区别** | ❌ 单 Agent 架构；❌ 无教学可读性优化；✅ 其临床评估框架（省时、盲审）可复用 |

---

### 3. Flamingo-CXR: Consensus, Dissensus and Synergy Between Clinicians and Specialist Foundation Models in Radiology Report Generation
| 字段 | 内容 |
|------|------|
| **作者/年份** | Tanno et al. (Google DeepMind), 2023 |
| **出处** | arXiv:2311.18260 |
| **数据集** | MIMIC-CXR + 16 名认证放射科医生的盲审评估 |
| **核心方法** | 基于 DeepMind Flamingo VLM 微调得到 Flamingo-CXR。核心贡献不在方法，而在**评估方法论**——定量分析了 AI 报告与放射科医生报告之间的一致性（consensus）、分歧（dissensus）和协同潜力（synergy）。 |
| **创新点** | 提出了区分 AI–人类 expert agreement 的分析框架：AI 在召回率上偏弱但在语言规范性上有优势 |
| **关键模型** | Flamingo (DeepMind VLM) |
| **与我们的区别** | ❌ 仍是单模型；❌ 无教学评估；✅ 其"共识/分歧"分析框架可指导我们设计多 Agent 的 consensus 机制 |

---

### 4. CXR-CLIP: Toward Large Scale Chest X-ray Language-Image Pre-training
| 字段 | 内容 |
|------|------|
| **作者/年份** | You et al. (Kakao Brain), 2023 |
| **出处** | arXiv:2310.13292 |
| **数据集** | NIH ChestX-ray14, CheXpert（通过标签自动生成伪文本对） |
| **核心方法** | 提出 ICL (Image-Centric Loss) 和 TCL (Text-Centric Loss) 两种对比损失，利用影像学报告多 Section 结构进行细粒度跨模态学习。 |
| **创新点** | 用图像-标签对自动扩展为图像-文本对，解决医学 VLP 数据稀缺问题 |
| **关键模型** | CLIP 架构 + ICL/TCL loss |
| **与我们的区别** | ❌ 聚焦预训练而非生成；✅ CLIP 式 cross-modal representation 可作为我们 Vision Agent 的 backbone |

---

### 5. IMITATE: Clinical Prior Guided Hierarchical Vision-Language Pre-training
| 字段 | 内容 |
|------|------|
| **作者/年份** | Liu et al., 2023 |
| **出处** | arXiv:2310.07355 |
| **数据集** | MIMIC-CXR |
| **核心方法** | 利用放射报告的分层结构（Findings vs. Impressions），分别对齐不同层面的视觉特征。提出 clinical-informed contrastive loss 进行分层跨模态学习。 |
| **创新点** | 首次利用报告层次结构进行医学 VLP |
| **关键模型** | ViT + Transformer encoder, 分层对比学习 |
| **与我们的区别** | ❌ 预训练方法，非端到端生成；✅ 报告的层次结构可以用来组织我们 Teaching Agent 的结构化评分 |

---

### 6. Disease-Aware Dual-Stage Framework for Chest X-ray Report Generation
| 字段 | 内容 |
|------|------|
| **作者/年份** | Wu et al., 2025 |
| **出处** | arXiv:2511.12259 → **AAAI 2026** |
| **数据集** | CheXpert Plus, MIMIC-CXR, IU X-Ray |
| **核心方法** | Stage 1: 学习 Disease-Aware Semantic Tokens (DASTs) 并做跨模态对比对齐；Stage 2: Disease-Visual Attention Fusion (DVAF) + Dual-Modal Similarity Retrieval (DMSR) 检索相似病例辅助生成。 |
| **创新点** | 疾病感知语义 Token + 双模态相似性检索辅助报告生成 |
| **关键模型** | ViT + cross-attention + 对比学习 |
| **与我们的区别** | ❌ 仍是编码器-解码器架构；❌ 无多 Agent 讨论；✅ DASTs + DMSR 可以作为 Agent B (Draft Writer) 的检索增强组件 |

---

### 7. S2D-ALIGN: Shallow-to-Deep Auxiliary Learning for Anatomically-Grounded Radiology Report Generation
| 字段 | 内容 |
|------|------|
| **作者/年份** | Gao et al., 2025 |
| **出处** | arXiv:2511.11066 |
| **数据集** | MIMIC-CXR, IU X-Ray |
| **核心方法** | 渐进式 SFT 范式：从粗粒度（放射片-报告配对）到细粒度（关键短语驱动的解剖学 grounding），中间通过 memory adapter 跨阶段共享特征。 |
| **创新点** | 解剖学逐层对齐的渐进式微调 |
| **关键模型** | MLLM + memory adapter |
| **与我们的区别** | ❌ 单模型参数微调范式；✅ 解剖学 grounding 的思路可增强我们 Vision Agent 的定位精度 |

---

### 8. CXRMate-2: Structured Multimodal Temporal Embeddings and Tractable Reinforcement Learning for Clinically Acceptable CXR Report Generation
| 字段 | 内容 |
|------|------|
| **作者/年份** | Nicolson et al., 2026 |
| **出处** | arXiv:2604.18967 |
| **数据集** | MIMIC-CXR, CheXpert Plus, ReXgradient |
| **核心方法** | 结构化多模态时间序列编码 + GRPO (Group Relative Policy Optimization) 强化学习。三盲放射科医生评估：生成报告在 45% 评分中被认为可接受（等于或优于人类报告），在可读性上始终优于人类报告。 |
| **创新点** | RL 驱动的报告生成 + 大规模放射科医生盲审验证 |
| **关键模型** | LLM decoder + GRPO RL |
| **与我们的区别** | ❌ 单模型 RL；✅ GRPO reward 设计可启发我们的 Teaching Evaluator；✅ 其"可读性"评估模式与我们方向一致，但没有教学结构化 |

---

### 9. RIHA: Report-Image Hierarchical Alignment for Radiology Report Generation
| 字段 | 内容 |
|------|------|
| **作者/年份** | Chen et al., 2026 |
| **出处** | arXiv:2604.27559 → **Journal of Biomedical and Health Informatics (JBHI)** |
| **数据集** | MIMIC-CXR, IU X-Ray |
| **核心方法** | Visual Feature Pyramid + Text Feature Pyramid + Cross-modal Hierarchical Alignment (optimal transport)，在段落、句子、单词三层做跨模态对齐。 |
| **创新点** | 三层次（段落-句子-单词）最优传输对齐 |
| **关键模型** | Transformer + optimal transport |
| **与我们的区别** | ❌ 端到端编码器-解码器；✅ 多粒度对齐思想可参考 |

---

## 二、多智能体医学 AI（2024–2026）

### 10. MARL-Rad: Multi-Modal Multi-Agent Reinforcement Learning for Radiology Report Generation
| 字段 | 内容 |
|------|------|
| **作者/年份** | Baba et al., 2026 |
| **出处** | arXiv:2603.16876 |
| **数据集** | MIMIC-CXR, IU X-Ray |
| **核心方法** | 将 CXR 分析分解为区域专用 Agent + 全局整合 Agent，使用强化学习 (GRPO) 联合优化。显式建模侧别一致性（laterality）。 |
| **创新点** | 首个可端到端训练的 RL 多 Agent 放射报告生成框架 |
| **关键模型** | Region-specific agents + global integrator + RL |
| **与我们的区别** | ❌ Agent 分工是区域驱动（region-specific）而非认知角色驱动；❌ 无教学评估；❌ 无鉴别诊断闭环；✅ Agent 训练的 RL 范式可借鉴 |

---

### 11. XrayClaw: Cooperative-Competitive Multi-Agent Alignment for Trustworthy Chest X-ray Diagnosis
| 字段 | 内容 |
|------|------|
| **作者/年份** | Young & Xu, 2026 |
| **出处** | arXiv:2604.02695 |
| **数据集** | MS-CXR-T, MIMIC-CXR, CheXbench |
| **核心方法** | 4 个协同 Agent 模拟临床诊断流程 + 1 个竞争 Agent 做独立审计。提出 Competitive Preference Optimization (CPO) 训练目标：分析路径和直觉路径互相验证，惩罚不合逻辑的诊断。 |
| **创新点** | 协同-竞争多 Agent 架构 + CPO 训练；显式处理 AI "共识性错误" |
| **关键模型** | 多 LLM Agent + CPO |
| **与我们的区别** | ❌ 聚焦分类/标签任务，非报告生成；✅ 协同-竞争架构设计思路可参考；✅ 其"审计 Agent"类似于我们的 DDx Critic |

---

### 12. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
| 字段 | 内容 |
|------|------|
| **作者/年份** | Wu et al. (Microsoft Research), 2023 |
| **出处** | arXiv:2308.08155 |
| **核心方法** | 通用多 Agent 对话框架，支持 Agent 之间的自动对话、工具调用、代码执行。已广泛用于医疗等领域的 Agent 系统构建。 |
| **创新点** | Agent 间自动对话编排框架 |
| **关键模型** | LLM + Agent orchestration |
| **与我们的区别** | ❌ 通用框架，非医学专用；✅**可直接作为 LobsterCXR 的多 Agent 基础设施**——各 Agent 通过 AutoGen 的对话管理器通信 |

---

## 三、教学与评估导向的系统（2025–2026）

### 13. 🔥 MAARTA: Multi-Agentic Adaptive Radiology Teaching Assistant ⭐ 最相关
| 字段 | 内容 |
|------|------|
| **作者/年份** | Awasthi et al., 2025 |
| **出处** | arXiv:2506.17320 → **MICCAI 2025 (Main Conference)** |
| **数据集** | 眼动追踪数据 + radiology reports |
| **核心方法** | 多 Agent 框架分析医学生的注视模式 + 报告质量，与专家对比后提供个性化教学反馈。Agent 根据错误类型动态激活，使用 Perceptual Error Teacher Agent 分析查看模式差异。 |
| **创新点** | 首个多 Agent 放射学教学助手；眼动追踪感知的教学反馈；MICCAI 接收 |
| **关键模型** | 多 LLM Agent + 注视图分析 |
| **与我们的区别** | ⚡ **高度相关**：✅都有多 Agent + 教学目标；❌ MAARTA 侧重眼动模式分析而非报告生成质量；❌ 需要眼动追踪硬件不支持部署；✅ 我们的 Teaching Evaluator 可以借鉴其"错误分析→教学反馈"链路，但不需要眼动数据，直接评估报告文本 |

---

### 14. 🔥 IMACT-CXR: An Interactive Multi-Agent Conversational Tutoring System for Chest X-Ray Interpretation
| 字段 | 内容 |
|------|------|
| **作者/年份** | Le et al., 2025 |
| **出处** | arXiv:2511.15825 → **IEEE ISBI 2026** |
| **数据集** | REFLACX（含 bounding box 和 gaze 标注） |
| **核心方法** | 基于 AutoGen 的交互式 CXR 教学系统：同时处理学习者标注框、注视样本、文本观察。Agent 评估定位质量、生成苏格拉底式教学提示、检索 PubMed 证据、推荐相似病例。贝叶斯知识追踪 (BKT) 跟踪技能掌握度。 |
| **创新点** | 多 Agent 教学 + 实时交互 + 知识追踪 |
| **关键模型** | AutoGen Agent orchestration + NV-Reason-CXR-3B + BKT |
| **与我们的区别** | ⚡ **高度相关**：✅多 Agent 教学 CXR；❌ 需要交互式（学生实时输入），非自动生成教学报告；✅ BKT 可用于建模学习者状态 |

---

### 15. Concept-Enhanced Multimodal RAG for Interpretable Radiology Report Generation
| 字段 | 内容 |
|------|------|
| **作者/年份** | Salmè et al., 2026 |
| **出处** | arXiv:2602.15650 |
| **数据集** | MIMIC-CXR, IU X-Ray |
| **核心方法** | 将视觉表示分解为可解释的临床概念 + 多模态 RAG 检索增强生成。可解释性概念路径与检索路径统一。 |
| **创新点** | 概念瓶颈 + RAG 统一框架，挑战"可解释性 vs 准确性"的假设矛盾 |
| **关键模型** | Concept bottleneck + RAG + VLM |
| **与我们的区别** | ❌ 单 Agent；✅ 概念瓶颈的可解释性路径可增强我们的 Teaching Evaluator |

---

## 四、基础模型与理论工具（背景引用）

### 16. R2Gen: Generating Radiology Reports via Memory-driven Transformer
| 字段 | 内容 |
|------|------|
| **作者/年份** | Chen et al., 2020 |
| **出处** | EMNLP 2020 / arXiv:2010.16056 |
| **核心方法** | 关系记忆 (Relational Memory) + Memory-driven Conditional Layer Normalization 驱动报告生成的 Transformer |
| **用途** | 报告生成的奠基工作，作为 Agent B (Draft Writer) 的初始 baseline |

### 17. BioViL: Vision-Language Pretraining for CXR (via MedICaT / MIMIC)
| **作者/年份** | Boecking et al., 2022 |
| **出处** | ECCV 2022 |
| **核心方法** | 用 CheXpert 标注 + 对比学习做 CXR 专用 VLP |
| **用途** | Vision Agent backbone 的可选方案 |

### 18. GREEN: A Clinical Efficacy Metric for Radiology Report Generation
| **作者/年份** | Ostmeier et al., 2024 |
| **出处** | NAACL 2024 |
| **核心方法** | 基于 RadGraph 的 NER 覆盖率的临床有效性评估指标 |
| **用途** | 临床准确性评估指标，多个 SOTA（CXRMate-2, CheXmix 等）使用 |

### 19. RadGraph: Extracting Clinical Entities and Relations from Radiology Reports
| **作者/年份** | Jain et al., 2021 |
| **出处** | NeurIPS 2021 Datasets & Benchmarks |
| **核心方法** | 标注放射报告中实体及其关系的图结构数据集 |
| **用途** | 多个评估指标的基础数据集 |

---

## 五、评估指标与数据集速查

| 数据集/指标 | 年份 | 用途 |
|------------|------|------|
| **MIMIC-CXR** (Johnson et al.) | 2019 | 最大公开 CXR + 报告数据集（~377K images） |
| **IU X-Ray** (Denmer-Fushman et al.) | 2016 | 较小规模 CXR + 报告（~7K studies） |
| **CheXpert** (Irvin et al.) | 2019 | 14 病种 CXR 标注数据集 |
| **CheXbert** (Smit et al.) | 2020 | CXR labeler 用于自动标注 |
| **RadGraph** (Jain et al.) | 2021 | 报告实体关系 F1 指标 |
| **CheXbert F1** | — | 报告级疾病分类一致性 |
| **GREEN** (Ostmeier et al.) | 2024 | 临床有效性指标 |
| **RadCliQ** (Yu et al.) | 2023 | 综合 NLP + 临床指标 |
| **BLEU/METEOR/ROUGE-L** | — | 传统 NLG 指标（不推荐单独使用） |

---

## 六、关键总结：LobsterCXR 定位

### 现有工作空白（Gap Analysis）

| 维度 | 现有工作 | 空白 |
|------|---------|------|
| **鉴别诊断建模** | 单模型编码器-解码器（R2Gen, RiHA）或区域分工（MARL-Rad） | ❌ 无显式的鉴别诊断推理回路 |
| **教学评估** | 无端到端教学可读性优化 | ❌ 所有工作只关注临床准确性 |
| **多 Agent 协同** | AutoGen 通用框架；MAARTA 需眼动数据 | ❌ CXR 报告生成的认知角色分工 + 共识机制未探索 |
| **评估维度** | RadGraph, GREEN, CheXbert F1 (全临床相关) | ❌ 缺少教学可读性指标 |

### LobsterCXR 差异化优势

```
        ┌──────────────────────────────────────┐
        │          LobsterCXR (本工作)           │
        ├──────────────────────────────────────┤
        │ ✅ 多 Agent 认知角色分工                │
        │    (Vision → Draft → DDx → Teaching)  │
        │ ✅ 鉴别诊断驱动讨论-共识回路             │
        │ ✅ 教学可读性作为可优化信号              │
        │ ✅ 新评估维度：教学报告质量              │
        └──────────────────────────────────────┘
```

### 最相关竞争工作对比

| 论文 | 多Agent | 鉴别诊断 | 教学评估 | 报告生成 |
|------|---------|---------|---------|---------|
| MARL-Rad (2026) | ✅ 区域Agent | ❌ | ❌ | ✅ SOTA |
| XrayClaw (2026) | ✅ 竞合Agent | ✅ (分类级) | ❌ | ❌ (分类) |
| MAARTA (2025) | ✅ 教学Agent | ❌ | ✅ (需眼动) | ❌ |
| IMACT-CXR (2025) | ✅ 教学Agent | ❌ | ✅ (交互式) | ❌ |
| CheXagent (2024) | ❌ | ❌ | ❌ | ✅ |
| RaDialog (2023) | ❌ | ❌ | ❌ | ✅ |
| **LobsterCXR** | ✅ | ✅ | ✅ (文本级) | ✅ |

---

## 七、下一步行动建议

1. **下载关键论文 PDF**：优先阅读 MARL-Rad, XrayClaw, MAARTA, IMACT-CXR, Flamingo-CXR 五篇
2. **搭建实验环境**：MIMIC-CXR 申请（需 CITI 认证）+ GPU 服务器准备
3. **Baseline 复现**：从 R2Gen 开始，然后在 MIMIC-CXR 上跑 MARL-Rad 得到 baseline 结果
4. **BibTeX 生成**：详见 `papers/bibliography.bib`

> 📁 所有引用的论文均通过 arXiv 官方 API 验证 ID，确保真实可查。
