# LobsterCXR 方法设计书

## 多智能体协同鉴别诊断与教学报告生成框架

> 对应综述空白：① 鉴别诊断推理回路缺失 ② 教学可读性未纳入优化 ③ 三者统一框架缺失
> 版本：v1.0 | 2026-05-21

---

## 目录

1. [总体架构](#1-总体架构)
2. [Agent A：Vision Analyst（视觉分析师）](#2-agent-a-vision-analyst视觉分析师)
3. [Agent B：Draft Writer（报告起草师）](#3-agent-b-draft-writer报告起草师)
4. [Agent C：DDx Critic（鉴别诊断批评师）](#4-agent-c-ddx-critic鉴别诊断批评师)
5. [Agent D：Teaching Evaluator（教学评估师）](#5-agent-d-teaching-evaluator教学评估师)
6. [Consensus 融合机制](#6-consensus-融合机制)
7. [训练范式与损失函数](#7-训练范式与损失函数)
8. [与现有工作的核心区别](#8-与现有工作的核心区别)
9. [创新点清单](#9-创新点清单)
10. [实验方案](#10-实验方案)
11. [附录：Skill 备忘——投稿格式适配](#11-附录skill-备忘投稿格式适配)

---

## 1. 总体架构

### 1.1 设计理念

LobsterCXR 的 Agent 划分基于放射科医生的 **认知角色**，而非解剖区域。放射科医生阅片-写报告的认知流程可分解为：

```
观察（扫视影像、定位异常）→ 撰写（形成报告初稿）→ 鉴别（验证诊断、考虑鉴别诊断）→ 教学（结构化呈现、便于学习者理解）
```

对应四个 Agent：

```
                     ┌──────────────────────────────────────────┐
                     │          LobsterCXR 框架                  │
                     │                                          │
  CXR Image ──────►  │  ┌──────────┐     ┌───────────┐         │
                     │  │  Agent A │────►│  Agent B  │────┐     │
                     │  │  Vision  │     │   Draft   │    │     │
                     │  │  Analyst │     │   Writer  │    │     │
                     │  └──────────┘     └───────────┘    │     │
                     │       │                ▲           │     │
                     │       │                │           ▼     │
                     │       ▼          ┌──────────┐  ┌──────┐ │
                     │  ┌──────────┐    │ Agent C │◄─┤Cons. │ │
                     │  │ Consensus│◄──►│  DDx    │  │Gate  │ │
                     │  │  Memory  │    │  Critic │  └──────┘ │
                     │  └──────────┘    └──────────┘     │     │
                     │       │                ▲           │     │
                     │       ▼                │           ▼     │
                     │  ┌──────────┐    ┌──────────┐  ┌──────┐ │
                     │  │ Agent D │    │  Agent C │  │Final │ │
                     │  │Teaching │◄───┤  (revise) │  │Report│ │
                     │  │Evaluator│    └──────────┘  └──────┘ │
                     │  └──────────┘                           │
                     └──────────────────────────────────────────┘
```

### 1.2 消息传递与迭代流程

```
Round 0 (生成):
  A → B: 视觉特征 F_v + 疾病置信度向量 D_A
  B → Report: 初稿报告 R_0

Round 1 (鉴别-修订):
  C ← [F_v, D_A, R_0]: DDx Critic 分析 R_0
  C → Consensus Memory: 鉴别诊断反馈 (DDx_feedback)
  Consensus Gate 判断分歧度 → 决定是否修订
  若分歧 > τ: B ← C 的 DDx_feedback → 生成 R_1

Round 2 (教学评估-修订):
  D ← R_k: Teaching Evaluator 评分
  D → Consensus Memory: 教学评分向量 S = (s_struct, s_read, s_teach)
  if any s_i < teaching_threshold → B ← D 的教学建议 → 生成 R_{k+1}

Final:
  Consensus → 输出最终报告 R_final + DDx 说明 + 教学评分报告
```

---

## 2. Agent A：Vision Analyst（视觉分析师）

### 2.1 角色定义

将输入的 CXR 影像编码为多粒度视觉表示，输出结构化发现列表及疾病置信度。核心目标：**提供 Draft Writer 与 DDx Critic 所需的全部视觉证据**。

### 2.2 Backbone 选型

| 组件 | 模型来源 | 文献依据 | 选择理由 |
|------|---------|---------|---------|
| 视觉编码器 | **CheXagent 视觉编码器**（CLIP ViT-L/14，在 28 个 CXR 数据集上预训练） | Chen et al., 2024 [6] | 最大规模 CXR 多任务 VLM 的视觉 backbone，已经过大规模临床数据适配 |
| 多尺度特征 | **Visual Feature Pyramid**（3 级：16× / 32× / 64× 下采样） | RIHA, Chen et al., 2026 [10] | 多尺度同时捕捉全局对称性和局部病灶细节 |
| 疾病检测头 | CheXpert 14 类分类头 + 置信度校准（温度缩放） | CheXpert, Irvin et al., 2019; CXRMate-2 [9] | 输出校准后的疾病置信度，供 DDx Critic 和 Consensus 使用 |

### 2.3 输入与输出

**输入：** CXR 正位像（1 张），resize 至 224×224（与 ViT 兼容）

**输出：**
- `F_v`：视觉特征张量，形状 (L, d)，L = 图像 patch 数（196），d = 特征维度（768）
- `F_v_pyramid`：多尺度特征金字塔，{16×, 32×, 64×} 三级别
- `D_A`：疾病置信度向量，长度为 CheXpert 14 类，（sigmoid 校准后概率）
- `H_v`：视觉 attention map（用于 DDx Critic 的定位可视化）

### 2.4 实现细节

```python
class VisionAnalyst(nn.Module):
    def __init__(self):
        self.backbone = CheXagentViT(pretrained=True)  # ViT-L/14
        self.pyramid = VisualFeaturePyramid(
            in_dim=768,
            scales=[16, 32, 64]
        )
        self.classifier = nn.Sequential(
            nn.Linear(768, 256),
            nn.GELU(),
            nn.Linear(256, 14)  # CheXpert 14 classes
        )
        self.temperature = nn.Parameter(torch.tensor(1.0))  # 校准温度
    
    def forward(self, x):
        # x: (B, 3, 224, 224)
        patch_features, cls_token = self.backbone(x, return_patches=True)
        # patch_features: (B, 196, 768)
        pyramid = self.pyramid(patch_features)  # dict of 3 scales
        logits = self.classifier(cls_token)    # (B, 14)
        probs = torch.sigmoid(logits / self.temperature)  # 校准后置信度
        return patch_features, pyramid, probs
```

---

## 3. Agent B：Draft Writer（报告起草师）

### 3.1 角色定义

基于 Agent A 的视觉特征，按照 Findings → Impression 结构生成报告初稿。使用检索增强和疾病感知注意力提升临床准确性。

### 3.2 Backbone 选型

| 组件 | 模型来源 | 文献依据 | 选择理由 |
|------|---------|---------|---------|
| LLM 解码器 | **Vicuna-7B + LoRA** | RaDialog, Pellegrini et al., 2023 [2] | 参数高效微调，保留对话能力，兼容教学交互 |
| 跨模态适配器 | **Q-Former**（可学习的 query 从视觉特征中池化关键信息） | CheXagent [6] / BLIP-2 | 将图像 patch 特征压缩为固定长度视觉 token（32 tokens） |
| 疾病感知增强 | **Disease-Aware Semantic Tokens (DASTs)** + 交叉注意力 | Wu et al., AAAI 2026 [7] | 疾病感知注意力提升关键病理的生成召回率 |
| 检索增强 | **Dual-Modal Similarity Retrieval (DMSR)** | Wu et al., AAAI 2026 [7] | 检索相似病例辅助生成，提升罕见病描述质量 |

### 3.3 生成流程

```
F_v(196, 768) ──► Q-Former ──► F_v_cond(32, 768)
                                       │
D_A(14,) ──► DAST Embedding ──► D_tok(14, 768)
                                       │
                                       ▼
HealthDB ──► DMSR ──► Retrieval Tokens(8, 768)
                                       │
                    ┌──────────────────┘
                    ▼
        Vicuna-7B + LoRA Decoder
                    │
                    ▼
         ┌──────────────────────┐
         │  Findings Section    │
         │  (结构化体检描述)      │
         ├──────────────────────┤
         │  Impression Section  │
         │  (诊断结论与建议)      │
         └──────────────────────┘
```

### 3.4 输出

报告初稿 `R_0`，结构化格式：

```xml
<findings>
**心脏**: 心影大小未见明显异常...
**肺**: 双肺野清晰，未见实变或渗出...
**胸腔**: 肋膈角锐利...
**骨骼**: 所见骨质结构完整...
</findings>
<impression>
1. 双肺野清晰，未见活动性病变。
2. 心影大小正常。
</impression>
```

---

## 4. Agent C：DDx Critic（鉴别诊断批评师）

### 4.1 角色定义 ⭐ **核心创新**

对 Draft Writer 生成的报告进行鉴别诊断审查。不是简单的多标签分类校对，而是模拟放射科医生的 **"讨论-鉴别"思考链**：针对每个发现和诊断，生成候选鉴别诊断列表，交叉验证视觉证据，输出结构化的鉴别分析报告。

### 4.2 Backbone 选型

| 组件 | 模型来源 | 文献依据 | 选择理由 |
|------|---------|---------|---------|
| 推理 LLM | **Vicuna-13B + LoRA**（与 Agent B 共享 base，但独立 LoRA） | RaDialog [2]; XrayClaw [12] 的 CPO 范式 | 同源架构便于共享 tokenizer 和 embedding 层，独立 LoRA 实现专业化角色 |
| 标签空间接口 | **CheXbert 标签映射器** | Smit et al., 2020 | 将 CheXpert 14 类 + RadGraph 实体标准化，作为推理的离散空间 |
| 推理引擎 | **Chain-of-Thought + 结构化输出约束** | 本文设计 | 显式建模"发现→候选→区分→结论"的思考链 |

### 4.3 鉴别诊断推理逻辑：讨论-鉴别 (Discuss-Differentiate) 思考链

这是 LobsterCXR 的核心技术贡献。DDx Critic 的推理分为四个阶段：

#### 阶段 1：发现提取（Extract Findings）

解析 `R_0` 中的 Findings 段落，使用 CheXbert 提取每个解剖区域的关键发现：

```
输入: R_0 的 Findings 文本
输出: 结构化发现列表 F_findings = [(region, observation, severity), ...]

示例:
[
  ("肺", "双肺门周围磨玻璃影", "中度"),
  ("心脏", "心影增大", "可疑"),
  ("胸腔", "肋膈角变钝", "轻度")
]
```

#### 阶段 2：鉴别空间构建（Build Differential Space）

对每个发现，利用疾病-发现关联知识图谱（从 CheXpert 标签空间 + RadGraph 实体关系构建）生成候选诊断集：

```
对于发现 "双肺门周围磨玻璃影" 的候选诊断：
  D_candidates = {
    "肺水肿": 支持证据 = [心影增大, 肋膈角变钝], 视觉置信度 = D_A["肺水肿"],
    "肺炎（病毒性）": 支持证据 = [磨玻璃影分布, 临床病史], 视觉置信度 = D_A["肺炎"],
    "间质性肺病": 支持证据 = [分布模式], 视觉置信度 = D_A["间质性肺病"]
  }
```

#### 阶段 3：区分分析（Discriminate）

对每对易混淆诊断，基于视觉特征、D_A 置信度、报告隐状态进行对比推理：

```python
def discriminate(d1, d2, findings, F_v, D_A, R_hidden):
    """
    对两个候选诊断进行视觉证据的对比分析
    输出鉴别理由 + 倾向性得分
    """
    # Step 1: 查找区分特征（从医学知识图谱获取）
    discriminating_features = medical_kb.get_discriminating_features(d1, d2)
    # e.g., ("心影增大" 区分肺水肿 vs 肺炎)
    
    # Step 2: 检查 Found vs Not Found
    evidence_for_d1 = []
    evidence_for_d2 = []
    for feat in discriminating_features:
        if feat in findings:
            support_d1 = medical_kb.supports(feat, d1)
            support_d2 = medical_kb.supports(feat, d2)
            if support_d1 and not support_d2:
                evidence_for_d1.append(feat)
            elif support_d2 and not support_d1:
                evidence_for_d2.append(feat)
    
    # Step 3: 跨模态验证——用视觉 attention map 检查关键区域
    visual_evidence_d1 = check_visual_evidence(d1, F_v, D_A)
    visual_evidence_d2 = check_visual_evidence(d2, F_v, D_A)
    
    # Step 4: 生成自然语言鉴别理由
    rationale = generate_rationale(d1, d2, evidence_for_d1, evidence_for_d2,
                                   visual_evidence_d1, visual_evidence_d2)
    
    # Step 5: 倾向性得分（基于证据权重加权）
    score_d1 = (len(evidence_for_d1) * w_find + visual_evidence_d1 * w_vis) / \
               (len(evidence_for_d1) + len(evidence_for_d2) + 1e-6)
    
    return {
        "d1": d1, "d2": d2,
        "preference": "d1" if score_d1 > 0.6 else "d2" if score_d1 < 0.4 else "uncertain",
        "score": score_d1,
        "rationale": rationale,
        "suggested_revision": f"Current report states '{d1}', but the finding '{finding}' 
                               is also consistent with '{d2}'. Consider mentioning {d2} 
                               in differential and explaining why {d1} is favored."
    }
```

#### 阶段 4：输出结构化鉴别报告

DDx Critic 的最终输出是一个结构化的鉴别分析报告：

```json
{
  "report_id": "...",
  "claimed_diagnoses": ["肺水肿"],
  "differential_pairs": [
    {
      "d1": "肺水肿",
      "d2": "肺炎",
      "distinguishing_features": {"心影增大": "肺水肿", "发热": "肺炎"},
      "preference": "肺水肿 (score: 0.78)",
      "rationale": "双侧肺门周围磨玻璃影伴心影增大和肋膈角变钝，三联征高度提示肺水肿。
                   但需注意病毒性肺炎也可能出现双侧磨玻璃影。建议结合临床（是否有发热、
                   BNP水平）进一步确认。",
      "confidence_gap": 0.43,
      "suggested_revision": "Add to Impression: 'Differential diagnosis includes 
                            pulmonary edema (favored) versus viral pneumonia.'"
    }
  ],
  "missed_findings": [
    {"finding": "肺血管纹理增多", "severity": "轻度", "reported": false, 
     "importance": "支持肺水肿诊断"}
  ],
  "overall_assessment": {
    "correctness": 0.85,
    "completeness": 0.72,
    "confidence": 0.78
  }
}
```

### 4.4 关键设计：为什么这不是多标签分类

| 多标签分类 | DDx Critic 的讨论-鉴别 |
|-----------|----------------------|
| 输出 14 个独立 logits | 输出 **鉴别诊断对**，每一对包含对比推理过程 |
| 无交互证据链 | 显式链接"发现 A + 发现 B → 支持诊断 C → 排除诊断 D" |
| 置信度独立 | 置信度是**对比性**的（P(肺水肿|磨玻璃影) vs P(肺炎|磨玻璃影)） |
| 不能抓住"共现"模式 | 能处理同时存在的多种疾病（如肺水肿 + 肺炎）并说明主次关系 |
| 无反馈给起草师 | 输出结构化修订建议，直接指导报告修订 |

---

## 5. Agent D：Teaching Evaluator（教学评估师）

### 5.1 角色定义

从 **教学可读性** 维度评估报告质量。非生成式模型，而是评分模型：对报告打分，输出多维度教学质量分数，作为 Draft Writer 修订和 Consensus 判断的依据。

### 5.2 Backbone 选型

| 组件 | 模型来源 | 文献依据 | 选择理由 |
|------|---------|---------|---------|
| 文本编码器 | **PubmedBERT-base** | —— | 医学文本最优的 BERT 变体，在 14M PubMed 摘要上预训练 |
| 评分头 | 3 个独立的线性回归头（每个维度一个） | CXRMate-2 [9] 的 GRPO reward 设计启发 | 多维度可解释评分，每个维度的梯度可直接回传 |
| 知识增强 | RadGraph 实体覆盖检查器 | Jain et al., 2021; GREEN [18] | 结构化完整性需要实体级验证 |

### 5.3 评分维度

#### 维度 1：结构化评分（Structure Score, S_struct）

衡量报告是否具备清晰的教学组织结构：

| 子维度 | 测量方式 | 权重 |
|--------|---------|------|
| 头部分组 | Findings/Impression 二级标题是否明确 | 0.25 |
| 解剖区域划分 | 发现是否按解剖部位分组（心脏/肺/胸腔/骨骼） | 0.30 |
| 层级一致性 | 同一解剖组内发现表述格式是否一致 | 0.15 |
| 实体覆盖度 | RadGraph 实体（解剖结构 + 观察 + 不确定性）的完整度 | 0.30 |

```python
def compute_structure_score(report_text):
    """计算结构化评分"""
    score = 0.0
    
    # 1. 头部检查
    has_findings = "<findings>" in report_text or "**发现**" in report_text
    has_impression = "<impression>" in report_text or "**结论**" in report_text
    score += 0.25 if (has_findings and has_impression) else 0.0
    
    # 2. 解剖分区
    anatomy_regions = ["心脏", "肺", "胸腔", "骨骼", "纵隔", "膈肌"]
    found_regions = sum(1 for r in anatomy_regions if r in report_text)
    score += 0.30 * min(found_regions / 4, 1.0)
    
    # 3. RadGraph 实体覆盖（调用 RadGraph parser）
    entities = radgraph_parse(report_text)
    entity_coverage = len(entities) / expected_entity_count
    score += 0.30 * min(entity_coverage, 1.0)
    
    return min(score, 1.0)  # 归一化到 [0, 1]
```

#### 维度 2：可读性评分（Readability Score, S_read）

衡量医学生能否轻松理解报告内容：

| 子维度 | 测量方式 | 权重 |
|--------|---------|------|
| 句子长度 | 平均每句词数（目标 15-25），过长/过短扣分 | 0.20 |
| 术语密度 | 医学术语占比（目标 ≤30% 术语，以便学习者消化） | 0.30 |
| 术语解释 | 关键术语后是否有括号解释（"肺不张（肺组织塌陷）"） | 0.25 |
| 句式复杂度 | 从句嵌套层数（目标 ≤2 层） | 0.25 |

```python
def compute_readability_score(report_text):
    """计算可读性评分"""
    # 1. 句子长度
    sentences = sent_tokenize(report_text)
    avg_len = np.mean([len(s.split()) for s in sentences])
    len_score = 1.0 - min(abs(avg_len - 20) / 20, 1.0)  # 目标20词
    
    # 2. 术语密度
    medical_terms = len(re.findall(medical_term_pattern, report_text))
    total_words = len(report_text.split())
    term_density = medical_terms / total_words
    density_score = 1.0 - min(max(term_density - 0.15, 0) / 0.20, 1.0)
    # 允许15%的术语密度，超过35%扣到0
    
    # 3. 术语解释率
    explained = count_term_explanations(report_text)  # "X（Y）" 模式
    unexplained = count_unexplained_terms(report_text)
    explain_score = explained / (explained + unexplained + 1e-6)
    
    # 4. 句式复杂度
    complex_sents = sum(1 for s in sentences if count_clauses(s) > 2)
    complexity_score = 1.0 - complex_sents / len(sentences)
    
    return (0.20 * len_score + 0.30 * density_score + 
            0.25 * explain_score + 0.25 * complexity_score)
```

#### 维度 3：教学适用性评分（Teaching Suitability Score, S_teach）⭐

衡量报告是否服务于医学教育目的。这是最重要的维度：

| 子维度 | 测量方式 | 权重 |
|--------|---------|------|
| 鉴别诊断呈现 | 是否明确列出/讨论了鉴别诊断 | 0.30 |
| 证据链接 | 发现 → 诊断的推理链路是否清晰（"磨玻璃影提示可能是..."） | 0.25 |
| 临床上下文 | 是否提及解剖变异、正常变异、技术因素等教学要点 | 0.15 |
| 关键阴性发现 | 是否报告了应排除的阴性发现（如"未见气胸"） | 0.15 |
| 可操作性建议 | 是否有明确的下一步建议（如"建议CT进一步明确"） | 0.15 |

```python
def compute_teaching_score(report_text, ddx_output):
    """计算教学适用性评分"""
    score = 0.0
    
    # 1. 鉴别诊断呈现（利用 DDx Critic 的输出）
    has_ddx_discussion = ddx_output is not None and len(ddx_output["differential_pairs"]) > 0
    score += 0.30 if has_ddx_discussion else 0.0
    
    # 2. 证据链接（因果连接词检测）
    causal_markers = ["提示", "符合", "支持", "考虑", "因此", "鉴于", "由于"]
    causal_count = sum(1 for m in causal_markers if m in report_text)
    evidence_score = min(causal_count / 3, 1.0)
    score += 0.25 * evidence_score
    
    # 3. 关键阴性发现
    neg_findings = ["未见", "无", "正常", "清晰", "锐利", "未见明显异常"]
    neg_count = sum(1 for f in neg_findings if f in report_text)
    score += 0.15 * min(neg_count / 4, 1.0)
    
    # 4. 可操作性建议
    has_recommendation = any(w in report_text for w in 
                           ["建议", "推荐", "随访", "进一步", "必要时复查"])
    score += 0.15 if has_recommendation else 0.0
    
    return min(score, 1.0)
```

### 5.4 损失参与方式

Teaching Evaluator 的评分以以下三种方式参与训练和推理：

#### 方式 A：RL 奖励信号（训练阶段）

使用 GRPO（如 CXRMate-2 [9]），Teaching Evaluator 的输出作为奖励函数的一部分：

```python
def reward_function(R, D_A, D_reference):
    """GRPO 奖励函数"""
    # 临床准确性奖励（使用 CheXbert F1）
    R_clinical = compute_chexbert_f1(R, D_reference)
    
    # 教学可读性奖励
    s_struct = compute_structure_score(R)
    s_read = compute_readability_score(R)
    s_teach = compute_teaching_score(R, ddx_output)
    R_teaching = 0.25 * s_struct + 0.35 * s_read + 0.40 * s_teach
    
    # 总奖励（可配置权重）
    R_total = α * R_clinical + (1 - α) * R_teaching
    
    return R_total, {"clinical": R_clinical, "teaching": R_teaching, 
                     "struct": s_struct, "read": s_read, "teach": s_teach}
```

#### 方式 B：可微损失项（端到端微调阶段）

将 Teaching Evaluator 的评分建模为可微分的辅助损失：

```python
L_total = L_generation + λ_teach * L_teach

# L_teach 定义为 teaching score 与目标值的 MSE
# 目标值通过对训练集中高质量报告的教学评分获得
L_teach = MSE(S_pred, S_target)

# 其中 S_pred 通过 PubmedBERT + 评分头从报告隐状态回归得到
# 这使得梯度可以直接回传到 Draft Writer 的生成头
```

#### 方式 C：迭代门控（推理阶段）

Consensus 模块在迭代中使用 Teaching Evaluator 的评分作为停止条件：

```
while rounds < max_rounds:
    # 生成修订版 R_k
    # 计算教学评分
    if all(s >= threshold for s in [s_struct, s_read, s_teach]):
        break  # 教学评分达标，停止迭代
    # 否则继续修订
```

---

## 6. Consensus 融合机制

### 6.1 设计思想

借鉴 Flamingo-CXR [3] 的共识/分歧分析框架 和 XrayClaw [12] 的协同-竞争机制，设计 **置信度门控 + 加权融合** 的双层共识模块。

### 6.2 第一层：置信度门控（Confidence Gate）

基于 DDx Critic 与 Draft Writer 之间对每个疾病的置信度分歧，决定是否触发修订循环。

```
定义：
  P_B(d) = Draft Writer 对疾病 d 的隐含置信度（从生成的文本中通过 CheXbert 提取）
  P_C(d) = DDx Critic 对疾病 d 的置信度（来自鉴别分析）
  
分歧度：
  Δ(d) = |P_B(d) - P_C(d)|
  
门控信号：
  if max_d Δ(d) > τ_gate:
     触发修订 — DDx Critic 的结构化反馈送入 Draft Writer
  else:
     跳过修订，直接到 Consensus 融合
     
动态阈值：
  τ_gate = τ_0 + η · σ(Δ_rolling_mean)
  # τ_0 = 0.15（基础阈值）
  # η · σ(Δ_rolling_mean)：根据近期分歧波动自适应调整
```

### 6.3 第二层：加权共识融合（Weighted Consensus）

当修订循环结束后，将 Draft Writer 的最终报告与 DDx Critic 的鉴别分析进行加权融合，生成最终报告。

#### 疾病级加权投票

对于 CheXpert 14 类的每个疾病 d：

```
w_B = f(historical_accuracy_B[d])    # Draft Writer 在疾病 d 上的历史准确率
w_C = f(historical_accuracy_C[d])    # DDx Critic 在疾病 d 上的历史准确率
w_con = (w_B + w_C) / 2              # 共识层权重（固定，不参与投票）

P_final(d) = (w_B · P_B(d) + w_C · P_C(d) + w_con · P_con(d)) / (w_B + w_C + w_con)

最终决策：
  y_final(d) = 1 if P_final(d) > θ_d else 0
  # θ_d 为每个疾病单独校准的阈值
```

#### 报告文本级融合

对于最终的 Impression 段落，根据疾病级投票结果生成标准化结论：

```python
def fuse_impression(draft_impression, ddx_feedback, P_final):
    """
    将 Draft Writer 的 Impression 与 DDx Critic 的建议融合
    """
    # 如果共识决定新增某个诊断
    new_diagnoses = [d for d in chexpert_classes 
                     if P_final[d] > θ_d and d not in draft_impression]
    
    # 如果共识决定剔除某个诊断
    removed_diagnoses = [d for d in draft_impression 
                         if P_final[d] <= θ_d]
    
    # 对不确定的诊断对，添加鉴别说明
    uncertain_pairs = ddx_feedback["differential_pairs"] if 
                      max_d Δ(d) > τ_gate else []
    
    # 融合生成
    fused_text = draft_impression
    
    if new_diagnoses:
        fused_text += f"\nAdditionally, evidence suggests {', '.join(new_diagnoses)}."
    if removed_diagnoses:
        fused_text += f"\nNote: {', '.join(removed_diagnoses)} is less likely given current findings."
    for pair in uncertain_pairs:
        if pair["confidence_gap"] < 0.3:  # 高不确定性
            fused_text += f"\nDifferential: {pair['rationale']}"
    
    return fused_text
```

### 6.4 Consensus 的迭代停止条件

```
Stop when EITHER:
  1. max_d Δ(d) < τ_gate AND all teaching scores > η_teach
  2. rounds = max_rounds (default: 3)
  3. Draft Writer 的修订变化量 ΔR < ε (收敛)
```

### 6.5 伪代码：完整推理流程

```python
def lobstercxr_inference(image, max_rounds=3):
    """LobsterCXR 完整推理流程"""
    
    # Step 1: Vision Analysis
    F_v, pyramid, D_A = Agent_A(image)
    
    # Step 2: Initial Draft
    R_prev = None
    R_curr = Agent_B.generate(F_v, D_A, pyramid)
    
    for round_idx in range(max_rounds):
        # Step 3: DDx Critique
        C_output = Agent_C.critique(R_curr, F_v, D_A)
        
        # Step 4: Teaching Evaluation
        T_scores = Agent_D.evaluate(R_curr, C_output)
        
        # Step 5: Consensus Gate
        max_divergence = max([abs(subj.confidence - C_output.confidence[d]) 
                             for d in chexpert_classes])
        
        if max_divergence < τ_gate and all(t > η_teach for t in T_scores):
            break  # 共识达标，停止迭代
        
        # Step 6: Revision
        DDx_feedback = C_output["differential_pairs"]
        Teaching_feedback = {"struct": T_scores[0], "read": T_scores[1], 
                            "teach": T_scores[2]}
        
        R_prev = R_curr
        R_curr = Agent_B.revise(R_curr, DDx_feedback, Teaching_feedback)
        
        # Step 7: Convergence check
        if compute_similarity(R_curr, R_prev) > 0.95:
            break
    
    # Step 8: Final Consensus
    R_final = consensus_fusion(R_curr, C_output, D_A)
    
    return R_final, C_output, T_scores
```

---

## 7. 训练范式与损失函数

### 7.1 训练策略：三阶段逐步训练

鉴于四个 Agent 的复杂性和数据需求差异，采用 **分段训练 + 联合微调** 策略：

#### 阶段 1：Agent A + B 预训练（报告生成基座）

**目标：** 使 Draft Writer 能生成临床可用的报告初稿
**数据：** MIMIC-CXR 全量训练集（~190K pairs）
**损失：**

```
L_stage1 = L_ce(R_pred, R_gt) + λ_vlp * L_vlp

# L_ce：token-level 交叉熵（生成损失）
# L_vlp：视觉-语言对比损失（参照 CXR-CLIP [4] 的 ICL/TCL）
# 使用 Agent A 的视觉特征与报告文本进行对比对齐

L_ce = -Σ_t log P(w_t | w_{<t}, F_v, D_A)
L_vlp = 0.5 * ICL + 0.5 * TCL  (You et al., 2023)
```

可训练参数：
- Agent A: 全量（ViT 最后一层 + 分类头 + 温度参数）
- Agent B: Q-Former + LoRA (r=16) + DAST embedding + DMSR
- Vicuna-7B base: 冻结，仅 LoRA 更新

**Baseline 初始化：** 先用 R2Gen [1] 结构在 MIMIC-CXR 上跑出基线；然后用 Vicuna + LoRA 替换架构

#### 阶段 2：Agent C 训练（DDx Critic 专业化）

**目标：** 使 DDx Critic 能输出高质量的鉴别分析
**数据：** 从 MIMIC-CXR 构建 DDx 训练数据

**DDx 训练数据构建方法：**
- 对于每份训练报告，使用 CheXbert 提取真实的 14 类标签
- 对每个阳性诊断，从知识图谱找到其最易混淆的鉴别诊断
- 构建鉴 training pairs：「(影像, 报告首稿, 鉴别诊断对) → 正确的鉴别分析」

**损失：**

```
L_stage2 = L_ce(C_output, C_gt) + λ_pair * L_pair_margin

# L_ce：鉴别报告生成的交叉熵
# L_pair_margin：对比性 margin loss，确保鉴别对之间的置信度差距合理
#   如果 ground truth 是 d1 优于 d2，要求 P(d1) - P(d2) > margin

L_pair_margin = max(0, margin - (P_gt_d1 - P_gt_d2))
```

可训练参数：
- Agent C: Vicuna-13B 的 LoRA (r=16) + CheXbert 映射器（冻结 CheXbert）
- 推理引擎: 冻结（LLM 的 CoT 能力来自基座）

#### 阶段 3：Agent D 训练 + 联合微调（教学评估 + 全系统对齐）

**目标：** 训练 Teaching Evaluator 评分模型 + 全系统的 GRPO 联合优化

**Agent D 训练数据：**
- 从 MIMIC-CXR 随机采样 2,000 份报告
- 邀请放射科住院医师/高年资医学生标注教学评分（3 个维度的 1-5 Likert）
- 使用标注数据微调 PubmedBERT + 评分头

**损失：**

```
# Agent D 的回归损失
L_D = MSE(S_pred, S_human)   # 3 维评分 MSE

# 全系统 GRPO（参照 CXRMate-2 [9]）
L_stage3 = -E[R_total(R)]    # 最大化总奖励的负期望

# R_total 来自 [5.4 方式 A] 的奖励函数
```

可选训练配置：

| 配置 | 方案 A（推荐） | 方案 B（探索型） | 方案 C（上线后） |
|------|---------------|----------------|----------------|
| 范式 | 三阶段训练 | 端到端（仅 RL） | 人类反馈在线调优 |
| 计算量 | 中等 | 高（不稳定） | 高（需人工） |
| 性能预期 | 稳定 | 可能有突破 | 最高质量 |
| 实施 | ✅ 主路径 | ⚠️ 先跑方案 A | 📋 延后 |

### 7.2 总损失函数（三阶段整合后）

```
L_total = β_1 * L_ce(R_pred, R_gt)     — 报告生成基座
        + β_2 * L_vlp(F_v, R_gt)        — 跨模态对齐
        + β_3 * L_pair_margin(C)         — 鉴别对比
        + β_4 * L_D(S_pred, S_human)     — 教学评分回归
        - β_5 * E[R_total(R_final)]      — GRPO 奖励最大化
```

其中 β_1..β_5 是阶段可切换的：阶段 1 只有 β_1, β_2；阶段 2 新增 β_3；阶段 3 新增 β_4, β_5。

---

## 8. 与现有工作的核心区别

### 8.1 与最相关 4 个方法的结构化对比

| 维度 | **MARL-Rad** (2026) | **XrayClaw** (2026) | **MAARTA** (2025) | **CXRMate-2** (2026) | **LobsterCXR (本工作)** |
|------|------|------|------|------|------|
| **领域** | CXR 报告生成 | CXR 分类/标注 | 放射学教学 | CXR 报告生成 | **报告生成 + 教学** |
| **Agent 分工驱动** | 解剖区域（左肺/右肺/心脏...） | 认知角色（协同+竞争） | 教学角色（错误分析） | 单 Agent | **认知角色（视觉→起草→鉴别→教学）** |
| **鉴别诊断能力** | ❌ 无 | ✅ 分类级（竞争验证） | ❌ 无 | ❌ 无 | **✅ 报告级（讨论-鉴别思考链）** |
| **教学评估** | ❌ 无 | ❌ 无 | ✅ 依赖眼动数据 | ❌ 无 | **✅ 文本级教学可读性评分** |
| **共识机制** | ❌ 无显式共识 | ✅ CPO 协同-竞争 | ❌ 无 | ❌ 无 | **✅ 置信度门控 + 加权融合** |
| **训练范式** | GRPO 端到端 RL | DPO 离线训练 | 独立 Agent | GRPO RL | **三阶段：预训练→专业→联合RL** |
| **评估指标** | RadGraph, GREEN, CheXbert | AUC, Accuracy | 眼动指标 + 问卷 | RadGraph, GREEN + 盲审 | **RadGraph, GREEN, CheXbert + 教学评分** |
| **报告输出** | 单一报告 | 无（分类输出） | 教学反馈 | 单一报告 | **最终报告 + DDx 说明 + 教学评分报告** |
| **硬件依赖** | GPU | GPU | **GPU + 眼动仪** | GPU | **GPU（无需额外硬件）** |
| **发表出处** | arXiv 2026 | arXiv 2026 | MICCAI 2025 | arXiv 2026 | **目标：MICCAI/MedIA** |

### 8.2 关键差异化要点

1. **与 MARL-Rad 的区别**
   - MARL-Rad 的 Agent 按解剖区域划分（左肺 Agent、右肺 Agent...），本质上是视觉空间拆分，每个 Agent 负责一个局部区域。我们的 Agent 按认知角色划分，每个 Agent 拥有完整的输入视野但负责不同的**推理环节**。
   - MARL-Rad 无鉴别诊断回路。我们的 DDx Critic 专门为此设计。
   
2. **与 XrayClaw 的区别**
   - XrayClaw 的竞合框架在分类维度上验证了"讨论-验证"的有效性。我们将这一精神扩展到**报告生成**——这不是简单的标签扩展，而是需要在自由文本中进行推理链追踪和结构化输出约束。
   - XrayClaw 的 CPO 需要偏好对数据（paired preference），我们采用 GRPO（仅需 reward）兼容性更好。
   
3. **与 MAARTA 的区别**
   - MAARTA 需要眼动追踪硬件，限制了部署场景。我们的 Teaching Evaluator 仅基于报告文本，无需任何硬件支持。
   - MAARTA 的教学反馈面向"查看行为"，我们面向"报告质量"，两个互补维度。
   
4. **与 CXRMate-2 的区别**
   - CXRMate-2 在可读性上表现优异（盲审验证），但其优化目标只有临床准确性。我们新增了教学可读性的显式优化。
   - CXRMate-2 是单 Agent RL。我们通过 Multi-Agent 的共识门控实现了更可控的迭代优化。

---

## 9. 创新点清单

### 空白 1 → 创新 1：鉴别诊断驱动的讨论-共识推理回路

**空白：** 现有报告的生成是单阶段映射（影像→报告），缺乏显式的鉴别诊断验证。
**我们的填补：**

- ✅ 设计了 DDx Critic（Agent C），通过 **四阶段讨论-鉴别思考链**（发现提取 → 鉴别空间构建 → 区分分析 → 结构化输出）进行鉴别诊断推理
- ✅ 鉴别诊断不是简单的多标签分类校对，而是对易混淆诊断对进行 **对比性证据分析**，输出结构化鉴别理由
- ✅ 通过 Consensus 的置信度门控，DDx Critic 的鉴别反馈 → Draft Writer 的修订，形成 **闭环推理回路**
- ✅ 推理回路是可迭代的（最多 3 轮），每一次迭代都细化鉴别分析

**简要宣称：** 首个将鉴别诊断推理建模为可迭代的 Agent 间讨论回路并集成到 CXR 报告生成的工作。

### 空白 2 → 创新 2：教学可读性作为端到端可优化信号

**空白：** 所有现有评估指标和优化目标都未包含教学可读性维度。教学系统（MAARTA, IMACT-CXR）依赖额外硬件或交互式输入，无法直接端到端优化。
**我们的填补：**

- ✅ 提出 **Teaching Evaluator（Agent D）**，从结构化（S_struct）、可读性（S_read）、教学适用性（S_teach）三个维度量化报告的教学质量
- ✅ 教学评分以三种方式参与优化：GRPO 奖励（RL 训练）、可微辅助损失（端到端微调）、迭代停止门控（推理）
- ✅ **无需眼动追踪或交互式输入**，仅基于报告文本，大大降低了部署门槛
- ✅ 教学评估与临床准确性并行优化，不是替代关系

**简要宣称：** 首个将教学可读性建模为多维度可微分评分并纳入 CXR 报告生成端到端优化的工作。

### 空白 3 → 创新 3：统一的"鉴别诊断 + 教学评估"多智能体框架

**空白：** 现有工作中，缺乏能同时覆盖多角色 Agent 协同 + 鉴别诊断推理 + 教学可读性评估的统一框架。
**我们的填补：**

- ✅ 四 Agent 按 **认知角色分工**（视觉分析 → 报告起草 → 鉴别批评 → 教学评估），比解剖分工更接近放射科医生的工作流
- ✅ 设计了 **置信度门控 + 加权融合** 的双层 Consensus 机制，融合 Draft Writer 和 DDx Critic 的意见
- ✅ 全系统可端到端训练（三阶段策略），所有 Agent 共享梯度流
- ✅ 综合输出包括：最终报告 + 鉴别诊断说明 + 教学评分报告，**服务两个受众**（临床医生 + 医学生）

**简要宣称：** 首个统一了认知角色驱动多 Agent 协同、鉴别诊断推理回路和教学可读性优化的 CXR 报告生成框架。

### 创新点总结表

| # | 创新点 | 对应空白 | 新颖性等级 | 验证方式 |
|---|--------|---------|-----------|---------|
| 1 | 讨论-鉴别思考链 + Agent 间闭环推理回路 | 空白 1 | ⭐⭐⭐ | 消融：有无 DDx Critic 的 CheXbert F1 差值 |
| 2 | 教学可读性的三维度评分 + RL 奖励参与 | 空白 2 | ⭐⭐⭐ | 消融：+Teaching 前后教学评分的提升 |
| 3 | 统一多 Agent 认知角色框架 + 双层 Consensus | 空白 3 | ⭐⭐ | 模块消融 / 盲审：多 Agent vs 单 Agent |
| 4 | 置信度门控自适应修订机制 | 空白 1 | ⭐⭐ | 不同 τ 值的消融 / 修订轮次分析 |

---

## 10. 实验方案

### 10.1 实验目的

1. 验证 LobsterCXR 在**临床准确性**指标上达到或超过 SOTA
2. 验证 LobsterCXR 在**教学可读性**维度上的显著优势
3. 通过消融实验确认每个 Agent 和 Consensus 模块的边际贡献
4. 通过盲审验证系统的临床应用价值和教学价值

### 10.2 数据集

| 数据集 | 用途 | 规模 | 说明 |
|--------|------|------|------|
| **MIMIC-CXR** | 主训练 + 测试 | ~190K train / ~3K test | 标准分割（已有） |
| **IU X-Ray** | 跨域泛化测试 | ~7K（5.2K train） | 不同机构分布 |
| **CheXpert Plus** | DDx Critic 预训练数据构建 | ~200K | 结构化标注 |

### 10.3 评估指标

| 类别 | 指标 | 说明 |
|------|------|------|
| **临床准确性** | CheXbert F1 (macro/micro) | 14 类疾病标签一致性 |
| | RadGraph F1 | 实体级临床信息覆盖 |
| | GREEN | 细粒度临床有效性 |
| | RadCliQ | 复合指标 |
| **教学可读性** | **S_struct, S_read, S_teach** | 本文提出的三维度评分 |
| | Human teaching rating (1-5) | 医学生/住院医师盲审 |
| **NLG** | BLEU-4, ROUGE-L, METEOR | 辅助参考 |
| **临床实用性** | 放射科医生盲审 | Two-alternative forced choice |
| | 教学偏好测试 | 医学生偏好选择 |

### 10.4 Baseline 选择

| Baseline | 选择理由 | 复现方式 |
|----------|---------|---------|
| **R2Gen** (Chen et al., 2020) | 报告生成奠基工作 | 官方实现 |
| **RaDialog** (Pellegrini et al., 2023) | VLM 基线，与 Agent B 同源 | 参照论文 + LoRA |
| **MARL-Rad** (Baba et al., 2026) | 最接近的多 Agent 方法 | 论文复现（联系作者） |
| **CXRMate-2** (Nicolson et al., 2026) | 临床 SOTA + GRPO | 论文复现 |
| **LobsterCXR (Ours)** | 本文方法 | — |

此外，做以下消融变体：
- `Ours -DDx`：去掉 DDx Critic，仅 A+B+D+Consensus
- `Ours -Teaching`：去掉 Teaching Evaluator，仅 A+B+C+Consensus（用 CheXbert F1 做 reward）
- `Ours -Consensus`：直接输出 Agent B 的最终修订结果，无 Consensus 融合
- `Ours (1-round)`：限制仅 1 轮修订，无迭代

### 10.5 实验矩阵

```
┌────────────────────────────────────────────────────────────┐
│  表：MIMIC-CXR 测试集上的主要结果                          │
├──────────────┬───────┬───────┬──────┬───────┬─────────────┤
│ Model        │CheXbert│RadGr.│GREEN │教学评分│ 盲审偏好率   │
├──────────────┼───────┼───────┼──────┼───────┼─────────────┤
│ R2Gen        │       │       │      │       │             │
│ RaDialog     │       │       │      │       │             │
│ MARL-Rad     │       │       │      │       │             │
│ CXRMate-2    │       │       │      │       │             │
│ LobsterCXR   │  ?    │  ?    │  ?   │  ?    │  ?          │
└──────────────┴───────┴───────┴──────┴───────┴─────────────┘

┌────────────────────────────────────────────────────────────┐
│  表：消融实验（MIMIC-CXR）                                 │
├────────────────────┬───────┬───────┬───────┬──────────────┤
│ Variant            │CheXbert│GREEN │教学评分│ 修订轮次 avg │
├────────────────────┼───────┼───────┼───────┼──────────────┤
│ Ours (full)        │       │       │       │              │
│ Ours -DDx          │       │       │       │              │
│ Ours -Teaching     │       │       │       │              │
│ Ours -Consensus    │       │       │       │              │
│ Ours (1-round)     │       │       │       │              │
└────────────────────┴───────┴───────┴───────┴──────────────┘

┌────────────────────────────────────────────────────────────┐
│  表：跨域泛化测试（IU X-Ray）                              │
├──────────────┬───────┬───────┬──────┬──────┬─────────────┤
│ Model        │CheXbert│RadGr.│GREEN │教学评分│ Δ from in-dist│
├──────────────┼───────┼───────┼──────┼───────┼─────────────┤
│ ...          │       │       │      │       │             │
└────────────────────────────────────────────────────────────┘
```

### 10.6 盲审设计

| 维度 | 方法 |
|------|------|
| **参与者** | ① 3 名放射科住院医师（临床评估）② 5 名高年资医学生（教学评估） |
| **临床盲审** | 随机展示 100 对（LobsterCXR 报告 vs Baseline best），盲评"哪个更好/无差异" |
| **教学盲审** | 同上 100 对，但评阅者为医学生，额外填写教学评分 1-5 |
| **指标** | 偏好率 + Cohen's κ 一致性 + 教学评分均值/方差 |

### 10.7 计算资源与实施计划

| 阶段 | 所需 GPU | 预计时间 | 前置条件 |
|------|---------|---------|---------|
| Stage 1 (A+B 预训练) | 1× A100 (80GB) | ~3 天 | MIMIC-CXR 数据准备完成 |
| Stage 2 (C 训练) | 1× A100 (80GB) | ~2 天 | Stage 1 模型 |
| Stage 3 (D + 联合微调) | 1× A100 (80GB) | ~4 天 | Stage 1+2 模型 + 教学标注数据 |
| 消融实验 | 1× A100 | ~2 天 | 全模型 |
| 盲审 | — | ~1 周（人时） | 测试集推理结果 |

**总预计：** ~2 周实验周期 + 1 周结果分析

### 10.8 预期结果与风险缓解

| 风险 | 概率 | 缓解措施 |
|------|------|---------|
| DDx Critic 生成质量欠佳 | 中 | 先用 CheXbert + 规则引擎做冷启动，再过渡到 LLM |
| GRPO 训练不稳定 | 中 | 先从 KL 惩罚系数调起；备选方案：PPO + 约束 |
| 教学评分与临床准确性存在 trade-off | 低 | 通过 α 权重调节（见 5.4），保留多个 α 配置的结果 |
| 盲审参与者缺勤 | 中 | 多预留 2 名候选评审者 |

---

## 11. 附录：Skill 备忘——投稿格式适配

待创建的 Skill：**submission-formatter**

**触发条件：** 用户给出期刊/会议名 + 论文草稿

**自动调整项：**
1. **页数/字数限制：** 按目标会议官网要求裁剪
2. **单栏/双栏：** 自动切换模板
3. **引用格式：** IEEE / ACM / Nature / LNCS 等自动转换 BibTeX
4. **图表编号与位置：** 重编号、调整表格格式
5. **Section 命名：** 按目标会议要求（如 MICCAI 的 Introduction→Methods→Results）
6. **Abstract 字数：** 裁切至要求范围
7. **字体与行距：** 匹配官方模板

**优先级：** 🔴 写作阶段激活。先存，后面再说。

---

## 版本记录

| 版本 | 日期 | 修改内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-05-21 | 初始完整设计 | Lobster 🦞 |

---

> **下一步行动建议：**
> 1. ✅ 方法定稿（本文完成）
> 2. 🔲 技术可行性验证：跑 R2Gen baseline on MIMIC-CXR
> 3. 🔲 DDx 知识图谱构建（从 CheXpert + RadGraph 提取疾病-发现关联）
> 4. 🔲 Agent A Quick Test：用 CheXagent 视觉 backbone 在 MIMIC-CXR 上跑 CheXpert 分类结果
> 5. 🔲 教学标注数据收集方案设计（问卷 + 标注平台）
> 6. 🔲 如果以上都 OK → 开始 Stage 1 训练
