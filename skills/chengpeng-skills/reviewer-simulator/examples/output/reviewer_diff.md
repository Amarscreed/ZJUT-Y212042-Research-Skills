# Diff of Auto-Fixes

```diff
--- original

+++ fixed

@@ -40,10 +40,10 @@

 %% Box for key formula
 \newsavebox{\keybox}
 \newcommand{\keyformula}[2][eq:key]{%
-  \vspace{2mm}\noindent
-  \fbox{\parbox{0.92\textwidth}{\centering\vspace{2mm}%
-    \begin{math}\displaystyle\begin{aligned} #2 \end{aligned}\end{math}%
-  \vspace{2mm}}}\vspace{2mm}\label{#1}}
+ \vspace{2mm}\noindent
+ \fbox{\parbox{0.92\textwidth}{\centering\vspace{2mm}%
+ \begin{math}\displaystyle\begin{aligned} #2 \end{aligned}\end{math}%
+ \vspace{2mm}}}\vspace{2mm}\label{#1}}
 
 %% Column types
 \newcolumntype{C}{>{\centering\arraybackslash}m{2.1cm}}
@@ -64,9 +64,9 @@

 \maketitle
 
 \begin{abstract}
-Automated chest X-ray (CXR) report generation has advanced considerably, yet existing methods lack three critical capabilities: (1) an explicit differential diagnosis reasoning loop for distinguishing confusable diseases; (2) evaluation systems that incorporate pedagogical readability alongside clinical accuracy; and (3) a unified multi-agent framework simultaneously addressing both reasoning and education.
-
-Our framework, \textbf{LobsterCXR}, teams up four cognitively-role-driven agents: \textbf{Vision Analyst} (CheXagent ViT-L/14 encoding with multi-scale features and 14-class CheXpert confidence calibration), \textbf{Draft Writer} (Vicuna-7B + LoRA generation with Q-Former cross-modal compression and retrieval augmentation), \textbf{DDx Critic} (a four-stage ``Discuss-Differentiate'' reasoning chain producing structured comparative rationales for confusable diagnostic pairs), and \textbf{Teaching Evaluator} (three-dimensional pedagogical scoring across structure, readability, and teaching suitability). A dual-layer consensus mechanism coordinates inter-agent outputs via confidence gating and weighted fusion, with end-to-end optimization combining language modeling, contrastive discrimination, and GRPO reinforcement learning.
+Automated chest X-ray (CXR) report generation has advanced considerably, yet existing methods lack three critical capabilities: (1) an explicit differential diagnosis reasoning loop for distinguishing confusable diseases; (2) evaluation systems that incorporate pedagogical readability alongside clinical accuracy; and (3) an unified multi-agent framework simultaneously addressing both reasoning and education.
+
+Our framework, \\textbf{LobsterCXR}, teams up four cognitively-role-driven agents: \\textbf{Vision Analyst} (CheXagent ViT-L/14 encoding with multi-scale features and 14-class CheXpert confidence calibration), \\textbf{Draft Writer} (Vicuna-7B + LoRA generation with Q-Former cross-modal compression and retrieval augmentation), \\textbf{DDx Critic} (a four-stage ``Discuss-Differentiate'' reasoning chain producing structured comparative rationales for confusable diagnostic pairs), and \\textbf{Teaching Evaluator} (three-dimensional pedagogical scoring across structure, readability, and teaching suitability). A dual-layer consensus mechanism coordinates inter-agent outputs via confidence gating and weighted fusion, with end-to-end optimization combining language modeling, contrastive discrimination, and GRPO reinforcement learning.
 
 Experiments on MIMIC-CXR and IU X-Ray demonstrate that LobsterCXR matches or exceeds state-of-the-art clinical accuracy (CheXbert F1, RadGraph F1, GREEN) while significantly outperforming baselines on pedagogical readability metrics. Ablation studies confirm the marginal contribution of each agent and the consensus module.
 
@@ -80,18 +80,18 @@

 
 Chest X-ray (CXR) is the most widely performed radiological examination globally, with over 1.4 billion procedures conducted annually~\cite{chexagent}. The global shortage of radiologists leads to prolonged report turnaround times and increased diagnostic error rates~\cite{tanno2023}. Automated CXR report generation has progressed from early RNN-based models~\cite{r2gen} to large vision-language models~\cite{radialog,chexagent,cxrmate2}, yet through systematic analysis of over 20 SOTA works we identify three critical gaps:
 
-\textbf{Gap 1: Absence of differential diagnosis reasoning loops.} Every existing method~\cite{r2gen,chexagent,riha,cxrmate2} maps images straight to text in one pass---no ``generate-criticize-revise'' loop in sight. MARL-Rad~\cite{marlrad} adopts region-based multi-agent design but divides by anatomical regions rather than cognitive roles. No prior work integrates differential diagnosis critique as an optimizable reasoning loop within report generation.
-
-\textbf{Gap 2: Pedagogical assessment absent from end-to-end optimization.} All standard metrics (RadGraph F1~\cite{radgraph}, CheXbert F1, GREEN~\cite{green}) focus exclusively on clinical completeness. MAARTA~\cite{maarta} and IMACT-CXR~\cite{imactcxr} serve educational purposes but require eye-tracking hardware or interactive input, precluding automated deployment.
-
-\textbf{Gap 3: Lack of a unified framework.} No existing work simultaneously covers multi-role agent collaboration, differential diagnosis reasoning, and pedagogical readability optimization.
+\\textbf{Gap 1: Absence of differential diagnosis reasoning loops.} Every existing method~\cite{r2gen,chexagent,riha,cxrmate2} maps images straight to text in one pass---no ``generate-criticize-revise'' loop in sight. MARL-Rad~\cite{marlrad} adopts region-based multi-agent design but divides by anatomical regions rather than cognitive roles. No prior work integrates differential diagnosis critique as an optimizable reasoning loop within report generation.
+
+\\textbf{Gap 2: Pedagogical assessment absent from end-to-end optimization.} All standard metrics (RadGraph F1~\cite{radgraph}, CheXbert F1, GREEN~\cite{green}) focus exclusively on clinical completeness. MAARTA~\cite{maarta} and IMACT-CXR~\cite{imactcxr} serve educational purposes but require eye-tracking hardware or interactive input, precluding automated deployment.
+
+\\textbf{Gap 3: Lack of an unified framework.} No existing work simultaneously covers multi-role agent collaboration, differential diagnosis reasoning, and pedagogical readability optimization.
 
 LobsterCXR tackles these gaps head-on. Concretely:
 \begin{enumerate}
-    \item \textbf{A cognitive-role-driven multi-agent architecture} for CXR report generation (\S3.1)---instead of splitting by anatomy, we split by thinking stage.
-    \item \textbf{A discuss-consensus reasoning loop} (\S3.4) implementing explicit comparative differential diagnosis via a four-stage ``Extract$\to$Build$\to$Discriminate$\to$Output'' chain.
-    \item \textbf{Pedagogical readability as an end-to-end optimizable objective} (\S3.5), introducing a three-dimensional teaching quality scoring system that participates in optimization through GRPO rewards, differentiable auxiliary losses, and inference gating.
-    \item \textbf{A dual-layer consensus mechanism} (\S3.6) combining confidence gating and weighted fusion to manage inter-agent disagreement and enable iterative report refinement.
+ \item \\textbf{A cognitive-role-driven multi-agent architecture} for CXR report generation (\S3.1)---instead of splitting by anatomy, we split by thinking stage.
+ \item \\textbf{A discuss-consensus reasoning loop} (\S3.4) implementing explicit comparative differential diagnosis via a four-stage ``Extract$\to$Build$\to$Discriminate$\to$Output'' chain.
+ \item \\textbf{Pedagogical readability as an end-to-end optimizable objective} (\S3.5), introducing a three-dimensional teaching quality scoring system that participates in optimization through GRPO rewards, differentiable auxiliary losses, and inference gating.
+ \item \\textbf{A dual-layer consensus mechanism} (\S3.6) combining confidence gating and weighted fusion to manage inter-agent disagreement and enable iterative report refinement.
 \end{enumerate}
 
 %% ============================================================
@@ -100,7 +100,7 @@

 \section{Related Work}
 
 \subsection{CXR Report Generation}
-R2Gen~\cite{r2gen} combines DenseNet-121 with memory-driven Transformer decoders. RaDialog~\cite{radialog} introduces Vicuna-7B as decoder with LoRA fine-tuning. CheXagent~\cite{chexagent} trains a multimodal LLM on 28 CXR datasets. CXRMate-2~\cite{cxrmate2} introduces GRPO reinforcement learning. RIHA~\cite{riha} employs three-level optimal transport cross-modal alignment. Wu et al.~\cite{diseaseaware} propose disease-aware semantic tokens (DASTs) and dual-modal retrieval. All adopt single-model encoder-decoder architectures without inter-agent discussion or explicit differential diagnosis reasoning.
+R2Gen~\cite{r2gen} combines DenseNet-121 with memory-driven Transformer decoders. RaDialog~\cite{radialog} introduces Vicuna-7B as decoder with LoRA fine-tuning. CheXagent~\cite{chexagent} trains a multimodal LLM on 28 CXR datasets. CXRMate-2~\cite{cxrmate2} introduces GRPO reinforcement learning. RIHA~\cite{riha} employs three-level optimal transport cross-modal alignment. Wu et al..~\cite{diseaseaware} propose disease-aware semantic tokens (DASTs) and dual-modal retrieval. All adopt single-model encoder-decoder architectures without inter-agent discussion or explicit differential diagnosis reasoning.
 
 \subsection{Multi-Agent Medical AI}
 AutoGen~\cite{autogen} provides general multi-agent conversation orchestration. MARL-Rad~\cite{marlrad} applies multi-agent RL to CXR report generation with anatomy-specific agents (left lung, right lung, heart) and a global integrator. XrayClaw~\cite{xrayclaw} proposes cooperative-competitive agents for CXR classification using competitive preference optimization. These works validate agent-based architectures for medical tasks but target classification rather than report generation with differential diagnosis.
@@ -109,7 +109,7 @@

 MAARTA~\cite{maarta} (MICCAI~2025) is the first multi-agent radiology teaching assistant, identifying perceptual errors via gaze pattern comparison between experts and trainees. IMACT-CXR~\cite{imactcxr} (ISBI~2026) proposes an interactive multi-agent CXR tutoring system with Bayesian Knowledge Tracing. Both advance the educational dimension but require hardware or real-time interaction, making them unsuitable for automated educational report generation.
 
 \subsection{Our Positioning}
-No prior work simultaneously addresses differential diagnosis reasoning loops, pedagogical readability as an optimization target, and multi-agent collaboration for CXR report generation. LobsterCXR aims to fill all three gaps within a unified framework.
+No prior work simultaneously addresses differential diagnosis reasoning loops, pedagogical readability as an optimization target, and multi-agent collaboration for CXR report generation. LobsterCXR aims to fill all three gaps within an unified framework.
 
 %% ============================================================
 %% 3. METHOD
@@ -118,7 +118,7 @@

 
 \subsection{Overall Architecture}
 
-LobsterCXR mirrors how radiologists actually work: four cognitive stages---\textbf{Observe} (scanning image, localizing abnormalities), \textbf{Write} (generating initial draft), \textbf{Verify} (validating diagnoses, considering differentials), and \textbf{Teach} (structuring output for learner comprehension)---each assigned to a dedicated agent.
+LobsterCXR mirrors how radiologists actually work: four cognitive stages---\\textbf{Observe} (scanning image, localizing abnormalities), \\textbf{Write} (generating initial draft), \\textbf{Verify} (validating diagnoses, considering differentials), and \\textbf{Teach} (structuring output for learner comprehension)---each assigned to a dedicated agent.
 
 \begin{figure}[t]
 \centering
@@ -129,9 +129,9 @@

 
 \subsection{Agent A: Vision Analyst}
 
-\textbf{What it does.} Encodes the input CXR at multiple granularities so downstream agents have both broad context and fine detail.
-
-\textbf{Architecture.} The visual encoder is CheXagent's ViT-L/14~\cite{chexagent}, pre-trained on 28 CXR datasets. To capture findings at different scales, we add RIHA's Visual Feature Pyramid (VFP)~\cite{riha} with three resolution levels ($16\times/32\times/64\times$). A lightweight classification head maps the [CLS] token to CheXpert's 14 disease classes with a learned temperature-scaling calibration.
+\\textbf{What it does.} Encodes the input CXR at multiple granularities so downstream agents have both broad context and fine detail.
+
+\\textbf{Architecture.} The visual encoder is CheXagent's ViT-L/14~\cite{chexagent}, pre-trained on 28 CXR datasets. To capture findings at different scales, we add RIHA's Visual Feature Pyramid (VFP)~\cite{riha} with three resolution levels ($16\times/32\times/64\times$). A lightweight classification head maps the [CLS] token to CheXpert's 14 disease classes with a learned temperature-scaling calibration.
 
 Let input image be $\mathbf{x} \in \mathbb{R}^{3 \times H \times W}$ with $H=W=224$:
 \begin{equation}
@@ -148,9 +148,9 @@

 
 \subsection{Agent B: Draft Writer}
 
-\textbf{Role.} Generates the initial structured report (Findings $\to$ Impression) with disease-aware attention and retrieval augmentation.
-
-\textbf{Backbone.} Vicuna-7B + LoRA ($r=16$)~\cite{radialog}. Q-Former (32 learnable queries)~\cite{chexagent} for cross-modal compression. Disease-Aware Semantic Tokens (DASTs) and Dual-Modal Similarity Retrieval (DMSR)~\cite{diseaseaware}.
+\\textbf{Role.} Generates the initial structured report (Findings $\to$ Impression) with disease-aware attention and retrieval augmentation.
+
+\\textbf{Backbone.} Vicuna-7B + LoRA ($r=16$)~\cite{radialog}. Q-Former (32 learnable queries)~\cite{chexagent} for cross-modal compression. Disease-Aware Semantic Tokens (DASTs) and Dual-Modal Similarity Retrieval (DMSR)~\cite{diseaseaware}.
 
 Q-Former compressed features:
 \begin{equation}
@@ -171,40 +171,40 @@

 
 \subsection{Agent C: DDx Critic (Core Innovation)}
 
-\textbf{Role.} Critically reviews the draft $R_0$ for differential diagnosis quality via a ``Discuss-Differentiate'' reasoning chain.
-
-\textbf{Backbone.} Vicuna-13B + LoRA ($r=16$), independent adapter for role specialization. Label space interface: CheXbert~\cite{chexpert} for standardized entity mapping.
-
-\textbf{Stage 1---Extract Findings.} Parse $R_0$ via CheXbert:
+\\textbf{Role.} Critically reviews the draft $R_0$ for differential diagnosis quality via a ``Discuss-Differentiate'' reasoning chain.
+
+\\textbf{Backbone.} Vicuna-13B + LoRA ($r=16$), independent adapter for role specialization. Label space interface: CheXbert~\cite{chexpert} for standardized entity mapping.
+
+\\textbf{Stage 1---Extract Findings.} Parse $R_0$ via CheXbert:
 \begin{equation}
 \mathcal{F} = \{ (a_i, o_i, s_i) \}_{i=1}^{N} = \text{CheXbert}(R_0) \label{eq:extract}
 \end{equation}
 
-\textbf{Stage 2---Build Differential Space.} Query disease-finding knowledge graph $\mathcal{K}$:
+\\textbf{Stage 2---Build Differential Space.} Query disease-finding knowledge graph $\mathcal{K}$:
 \begin{equation}
 \mathcal{D}_i = \mathcal{K}.\text{query}(f_i) = \{ (d_j, \text{evidence}_j, w_j) \} \label{eq:diffspace}
 \end{equation}
 
-\textbf{Stage 3---Discriminate (Core).} For each confusable pair $(d_p, d_q)$, cross-modal contrastive reasoning:
+\\textbf{Stage 3---Discriminate (Core).} For each confusable pair $(d_p, d_q)$, cross-modal contrastive reasoning:
 \begin{equation}
 \boxed{
 \Stotal(d_p, d_q) = \frac{
-    \sum_{e \in \Ksep(d_p, d_q)} \mathbf{1}[e \in \mathcal{F}] \cdot r(e, d_p)
-    + \alpha \cdot v(d_p)
+ \sum_{e \in \Ksep(d_p, d_q)} \mathbf{1}[e \in \mathcal{F}] \cdot r(e, d_p)
+ + \alpha \cdot v(d_p)
 }{
-    \sum_{e \in \Ksep(d_p, d_q)} \mathbf{1}[e \in \mathcal{F}] \cdot (r(e, d_p) + r(e, d_q))
-    + \alpha \cdot (v(d_p) + v(d_q))
+ \sum_{e \in \Ksep(d_p, d_q)} \mathbf{1}[e \in \mathcal{F}] \cdot (r(e, d_p) + r(e, d_q))
+ + \alpha \cdot (v(d_p) + v(d_q))
 }
 } \label{eq:disc}
 \end{equation}
 where $\Ksep$ are discriminating features between $d_p$ and $d_q$, $r(e,d)$ indicates feature-disease support, $v(d)=\yhat_A[d]$ is visual confidence, $\alpha$ weights visual evidence.
 
-\textbf{Stage 4---Structured Output:}
+\\textbf{Stage 4---Structured Output:}
 \begin{equation}
 \Cout = \{\text{claimed\_dx},\ \text{pairs}: (d_p,d_q,\Stotal,\text{rationale}),\ \text{missed},\ \text{overall}\} \label{eq:ddxout}
 \end{equation}
 
-\textbf{Key insight:} Eq.~\eqref{eq:disc} performs comparative reasoning over diagnosis \emph{pairs}, not independent per-disease logits. This enables explicit multi-evidence chain reasoning and competitive diagnosis differentiation---fundamentally different from all existing multi-label classification approaches.
+\\textbf{Key insight:} Eq.~\eqref{eq:disc} performs comparative reasoning over diagnosis \emph{pairs}, not independent per-disease logits. This enables explicit multi-evidence chain reasoning and competitive diagnosis differentiation---fundamentally different from all existing multi-label classification approaches.
 
 \begin{figure}[t]
 \centering
@@ -215,9 +215,9 @@

 
 \subsection{Agent D: Teaching Evaluator}
 
-\textbf{Role.} Non-generative scoring model quantifying pedagogical quality across three dimensions.
-
-\textbf{Backbone.} PubmedBERT-base + 3 independent linear regression heads. RadGraph entity coverage~\cite{green}.
+\\textbf{Role.} Non-generative scoring model quantifying pedagogical quality across three dimensions.
+
+\\textbf{Backbone.} PubmedBERT-base + 3 independent linear regression heads. RadGraph entity coverage~\cite{green}.
 
 Three-dimensional scores $\mathbf{S} \in [0,1]^3 = (\Sstruct, \Sread, \Steach)$:
 \begin{align}
@@ -228,11 +228,11 @@

 &\quad + 0.15 \cdot \mathbb{1}[\text{has\_rec}] + 0.15 \cdot \text{context\_score} \label{eq:steach}
 \end{align}
 
-\textbf{Optimization participation:} (a) GRPO reward: $\Rteach = \mathbf{w}^\top \mathbf{S}$ with $\mathbf{w}=[0.25,0.35,0.40]$; (b) differentiable auxiliary loss: $\Lteach = \text{MSE}(\mathbf{S}_{\text{pred}}, \mathbf{S}_{\text{target}})$; (c) inference gating: stop iteration when $\min(\mathbf{S}) \geq \eta_{\text{teach}}$.
+\\textbf{Optimization participation:} (a) GRPO reward: $\Rteach = \mathbf{w}^\top \mathbf{S}$ with $\mathbf{w}=[0.25,0.35,0.40]$; (b) differentiable auxiliary loss: $\Lteach = \text{MSE}(\mathbf{S}_{\text{pred}}, \mathbf{S}_{\text{target}})$; (c) inference gating: stop iteration when $\min(\mathbf{S}) \geq \eta_{\text{teach}}$.
 
 \subsection{Consensus Mechanism}
 
-\textbf{Layer 1---Confidence Gate.} Divergence between Draft Writer and DDx Critic for disease $d$:
+\\textbf{Layer 1---Confidence Gate.} Divergence between Draft Writer and DDx Critic for disease $d$:
 \begin{equation}
 \Delta(d) = |P_B(d) - P_C(d)| \label{eq:divergence}
 \end{equation}
@@ -243,7 +243,7 @@

 \end{cases} \label{eq:gate}
 \end{equation}
 
-\textbf{Layer 2---Weighted Fusion.}
+\\textbf{Layer 2---Weighted Fusion.}
 \begin{equation}
 P_{\text{final}}(d) = \frac{w_B \cdot P_B(d) + w_C \cdot P_C(d) + w_{\text{con}} \cdot P_{\text{con}}(d)}{w_B + w_C + w_{\text{con}}} \label{eq:fusion}
 \end{equation}
@@ -256,7 +256,7 @@

 \end{cases} \label{eq:conind}
 \end{equation}
 
-\textbf{Stop condition:}
+\\textbf{Stop condition:}
 \begin{equation}
 \text{Stop} \iff \bigl[ \max_d \Delta(d) < \tau_{\text{gate}} \land \min(\mathbf{S}) \geq \eta_{\text{teach}} \bigr] \lor [\text{rounds} \geq 3] \lor [\text{ROUGE-L} \geq 0.95] \label{eq:stop}
 \end{equation}
@@ -265,17 +265,17 @@

 
 Three-stage progressive training.
 
-\textbf{Stage 1: Agent A+B pre-training.}
+\\textbf{Stage 1: Agent A+B pre-training.}
 \begin{equation}
 \mathcal{L}_{\text{stage1}} = \Lce + \lambda_{\text{vlp}} \Lvlp \label{eq:stage1}
 \end{equation}
 
-\textbf{Stage 2: Agent C specialization.}
+\\textbf{Stage 2: Agent C specialization.}
 \begin{equation}
 \mathcal{L}_{\text{stage2}} = \Lce^{(C)} + \lambda_{\text{pair}} \max(0, \gamma - (P_{\text{gt}}(d_1) - P_{\text{gt}}(d_2))) \label{eq:stage2}
 \end{equation}
 
-\textbf{Stage 3: Joint fine-tuning (GRPO).}
+\\textbf{Stage 3: Joint fine-tuning (GRPO).}
 \begin{equation}
 \mathcal{L}_{\text{stage3}} = -\mathbb{E}_{R \sim \pi_{\theta}} [\Rtotal(R)] + \beta_{\text{KL}} \cdot \text{KL}(\pi_{\theta} \| \pi_{\text{ref}}) \label{eq:stage3}
 \end{equation}
@@ -285,7 +285,7 @@

 \Rtotal(R) = \alpha \cdot \Rclin(R; \mathbf{y}_{\text{ref}}) + (1-\alpha) \cdot \Rteach(\mathbf{S}) \label{eq:reward}
 \end{equation}
 
-\textbf{Total loss:}
+\\textbf{Total loss:}
 \keyformula[eq:total]{
 \Ltotal = &\beta_1 \Lce + \beta_2 \Lvlp + \beta_3 \Lpair \\
 &+ \beta_4 \Lteach - \beta_5 \mathbb{E}[\Rtotal] + \beta_6 \text{KL}(\pi_{\theta} \| \pi_{\text{ref}})
@@ -331,22 +331,22 @@

 
 \subsection{Baselines and Metrics}
 
-\textbf{Baselines:} R2Gen~\cite{r2gen}, RaDialog~\cite{radialog}, MARL-Rad~\cite{marlrad}, CXRMate-2~\cite{cxrmate2}. Ablation variants: Ours$-$DDx, Ours$-$Teaching, Ours$-$Consensus, Ours (1-round).
-
-\textbf{Clinical metrics:} CheXbert F1 (macro/micro), RadGraph F1~\cite{radgraph}, GREEN~\cite{green}, RadCliQ.
-\textbf{Pedagogical metrics:} $\Sstruct$, $\Sread$, $\Steach$ (ours); Human Teaching Rating (1--5).
-\textbf{Utility metrics:} Radiologist preference (2AFC), resident time saving.
+\\textbf{Baselines:} R2Gen~\cite{r2gen}, RaDialog~\cite{radialog}, MARL-Rad~\cite{marlrad}, CXRMate-2~\cite{cxrmate2}. Ablation variants: Ours$-$DDx, Ours$-$Teaching, Ours$-$Consensus, Ours (1-round).
+
+\\textbf{Clinical metrics:} CheXbert F1 (macro/micro), RadGraph F1~\cite{radgraph}, GREEN~\cite{green}, RadCliQ.
+\\textbf{Pedagogical metrics:} $\Sstruct$, $\Sread$, $\Steach$ (ours); Human Teaching Rating (1--5).
+\\textbf{Utility metrics:} Radiologist preference (2AFC), resident time saving.
 
 \subsection{Implementation Details}
 
 Hardware: 1$\times$ NVIDIA A100 (80GB). Code: \texttt{./experiments/}. Optimizer: AdamW.
 
-\noindent\textbf{Agent A:} CheXagent ViT-L/14. VFP 3-level. 2-layer MLP (768$\to$256$\to$14). $\tau$ init 1.0.
-\textbf{Agent B:} Vicuna-7B v1.5, LoRA $r=16$, $\alpha=32$. Q-Former 32 queries. DMSR Top-8.
-\textbf{Agent C:} Vicuna-13B v1.5, LoRA $r=16$. CheXbert frozen. $\mathcal{K}$ from CheXpert+RadGraph.
-\textbf{Agent D:} PubmedBERT-base (110M), 3-head regression, dropout 0.1, lr 2e-5.
-
-\noindent\textbf{Training:} Stage 1: lr 5e-5, bs 16. Stage 2: lr 3e-5, bs 16. Stage 3: lr 1e-5, bs 8, group 4, $\beta_{\text{KL}}=0.05$, $\alpha=0.7$. Consensus: $\tau_0=0.15$, $\eta=0.1$, $\eta_{\text{teach}}=0.7$.
+\noindent\\textbf{Agent A:} CheXagent ViT-L/14. VFP 3-level. 2-layer MLP (768$\to$256$\to$14). $\tau$ init 1.0.
+\\textbf{Agent B:} Vicuna-7B v1.5, LoRA $r=16$, $\alpha=32$. Q-Former 32 queries. DMSR Top-8.
+\\textbf{Agent C:} Vicuna-13B v1.5, LoRA $r=16$. CheXbert frozen. $\mathcal{K}$ from CheXpert+RadGraph.
+\\textbf{Agent D:} PubmedBERT-base (110M), 3-head regression, dropout 0.1, lr 2e-5.
+
+\noindent\\textbf{Training:} Stage 1: lr 5e-5, bs 16. Stage 2: lr 3e-5, bs 16. Stage 3: lr 1e-5, bs 8, group 4, $\beta_{\text{KL}}=0.05$, $\alpha=0.7$. Consensus: $\tau_0=0.15$, $\eta=0.1$, $\eta_{\text{teach}}=0.7$.
 
 \subsection{Main Results}
 
@@ -364,7 +364,7 @@

 MARL-Rad~\cite{marlrad} & -- & -- & -- & -- & -- \\
 CXRMate-2~\cite{cxrmate2} & -- & -- & -- & -- & -- \\
 \midrule
-\textbf{LobsterCXR} & -- & -- & -- & -- & -- \\
+\\textbf{LobsterCXR} & -- & -- & -- & -- & -- \\
 \bottomrule
 \end{tabular}
 \end{table}
@@ -383,7 +383,7 @@

 MARL-Rad & -- & -- & -- & -- \\
 CXRMate-2 & -- & -- & -- & -- \\
 \midrule
-\textbf{LobsterCXR} & -- & -- & -- & -- \\
+\\textbf{LobsterCXR} & -- & -- & -- & -- \\
 \bottomrule
 \end{tabular}
 \end{table}
@@ -421,7 +421,7 @@

 \midrule
 MARL-Rad & -- & -- & -- \\
 CXRMate-2 & -- & -- & -- \\
-\textbf{LobsterCXR} & -- & -- & -- \\
+\\textbf{LobsterCXR} & -- & -- & -- \\
 \bottomrule
 \end{tabular}
 \end{table}
@@ -458,7 +458,7 @@

 RaDialog & -- & -- & $\sim$7B + LoRA \\
 MARL-Rad & -- & -- & $\sim$7B + LoRA \\
 CXRMate-2 & -- & -- & $\sim$7B + LoRA \\
-\textbf{LobsterCXR} & -- & -- & $\sim$7B+13B + LoRA \\
+\\textbf{LobsterCXR} & -- & -- & $\sim$7B+13B + LoRA \\
 \bottomrule
 \end{tabular}
 \end{table}
@@ -470,17 +470,17 @@

 
 \subsection{Response to Three Gaps}
 
-How well does LobsterCXR plug the three holes? Let's walk through each. The DDx Critic's four-stage chain (Eq.~\eqref{eq:extract}--\eqref{eq:ddxout}) turns differential diagnosis from a black-box end-to-end mapping into explicit, evidence-based pairwise comparisons (Gap~1). The Teaching Evaluator's three-dimensional scoring (Eq.~\eqref{eq:sstruct}--\eqref{eq:steach}) is, to our knowledge, the first attempt to turn pedagogical readability into a differentiable, end-to-end optimizable signal (Gap~2). The cognitive-role-driven agent division provides a unified framework addressing both diagnosis and education (Gap~3).
+How well does LobsterCXR plug the three holes? Let's walk through each. The DDx Critic's four-stage chain (Eq.~\eqref{eq:extract}--\eqref{eq:ddxout}) turns differential diagnosis from a black-box end-to-end mapping into explicit, evidence-based pairwise comparisons (Gap~1). The Teaching Evaluator's three-dimensional scoring (Eq.~\eqref{eq:sstruct}--\eqref{eq:steach}) is, to our knowledge, the first attempt to turn pedagogical readability into a differentiable, end-to-end optimizable signal (Gap~2). The cognitive-role-driven agent division provides an unified framework addressing both diagnosis and education (Gap~3).
 
 \subsection{Comparison with Prior Work}
 
-\textbf{vs. MARL-Rad~\cite{marlrad}:} Their agents divide by anatomy (left lung, right lung, heart); ours divide by cognitive role. Each of our agents processes the full visual field but handles a distinct reasoning stage, enabling deeper per-stage specialization.
-
-\textbf{vs. XrayClaw~\cite{xrayclaw}:} Their CPO validates multi-agent verification in classification. We extend this paradigm to free-text report generation with structured output constraints and a DDx-specific reasoning chain.
-
-\textbf{vs. MAARTA~\cite{maarta}:} Their gaze-based perceptual error analysis is more granular but requires eye-tracking hardware. Our text-only approach has zero deployment overhead, enabling scalable educational report generation.
-
-\textbf{vs. CXRMate-2~\cite{cxrmate2}:} Their GRPO operates on a single agent. Our framework extends RL-based optimization with multi-agent collaboration and multi-dimensional (clinical + teaching) rewards.
+\\textbf{vs. MARL-Rad~\cite{marlrad}:} Their agents divide by anatomy (left lung, right lung, heart); ours divide by cognitive role. Each of our agents processes the full visual field but handles a distinct reasoning stage, enabling deeper per-stage specialization.
+
+\\textbf{vs. XrayClaw~\cite{xrayclaw}:} Their CPO validates multi-agent verification in classification. We extend this paradigm to free-text report generation with structured output constraints and a DDx-specific reasoning chain.
+
+\\textbf{vs. MAARTA~\cite{maarta}:} Their gaze-based perceptual error analysis is more granular but requires eye-tracking hardware. Our text-only approach has zero deployment overhead, enabling scalable educational report generation.
+
+\\textbf{vs. CXRMate-2~\cite{cxrmate2}:} Their GRPO operates on a single agent. Our framework extends RL-based optimization with multi-agent collaboration and multi-dimensional (clinical + teaching) rewards.
 
 \subsection{Limitations}
 
@@ -504,47 +504,47 @@

 %% ============================================================
 \begin{thebibliography}{21}
 
-\bibitem{r2gen} Chen, Z., et al. Generating Radiology Reports via Memory-driven Transformer. \emph{EMNLP}, 2020.
-
-\bibitem{radialog} Pellegrini, C., et al. RaDialog: A Large Vision-Language Model for Radiology Report Generation and Conversational Assistance. \emph{arXiv:2311.18681}, 2023.
-
-\bibitem{tanno2023} Tanno, R., et al. Consensus, Dissensus and Synergy Between Clinicians and Specialist Foundation Models in Radiology Report Generation. \emph{arXiv:2311.18260}, 2023.
-
-\bibitem{cxrclip} You, K., et al. CXR-CLIP: Toward Large Scale Chest X-ray Language-Image Pre-training. \emph{arXiv:2310.13292}, 2023.
-
-\bibitem{imitate} Liu, C., et al. IMITATE: Clinical Prior Guided Hierarchical Vision-Language Pre-training. \emph{arXiv:2310.07355}, 2023.
-
-\bibitem{chexagent} Chen, Z., et al. CheXagent: A Vision-Language Foundation Model to Enhance Efficiency of Chest X-ray Interpretation. \emph{arXiv:2401.12208}, 2024.
-
-\bibitem{diseaseaware} Wu, P., et al. A Disease-Aware Dual-Stage Framework for Chest X-ray Report Generation. \emph{AAAI}, 2026.
-
-\bibitem{s2dalign} Gao, J., et al. S2D-ALIGN: Shallow-to-Deep Auxiliary Learning for Anatomically-Grounded Radiology Report Generation. \emph{arXiv:2511.11066}, 2025.
-
-\bibitem{cxrmate2} Nicolson, A., et al. CXRMate-2: Structured Multimodal Temporal Embeddings and Tractable Reinforcement Learning for Clinically Acceptable Chest X-ray Radiology Report Generation. \emph{arXiv:2604.18967}, 2026.
-
-\bibitem{riha} Chen, Y., et al. RIHA: Report-Image Hierarchical Alignment for Radiology Report Generation. \emph{JBHI}, 2026.
-
-\bibitem{marlrad} Baba, K., et al. MARL-Rad: Multi-Modal Multi-Agent Reinforcement Learning for Radiology Report Generation. \emph{arXiv:2603.16876}, 2026.
+\bibitem{r2gen} Chen, Z., et al.. Generating Radiology Reports via Memory-driven Transformer. \emph{EMNLP}, 2020.
+
+\bibitem{radialog} Pellegrini, C., et al.. RaDialog: A Large Vision-Language Model for Radiology Report Generation and Conversational Assistance. \emph{arXiv:2311.18681}, 2023.
+
+\bibitem{tanno2023} Tanno, R., et al.. Consensus, Dissensus and Synergy Between Clinicians and Specialist Foundation Models in Radiology Report Generation. \emph{arXiv:2311.18260}, 2023.
+
+\bibitem{cxrclip} You, K., et al.. CXR-CLIP: Toward Large Scale Chest X-ray Language-Image Pre-training. \emph{arXiv:2310.13292}, 2023.
+
+\bibitem{imitate} Liu, C., et al.. IMITATE: Clinical Prior Guided Hierarchical Vision-Language Pre-training. \emph{arXiv:2310.07355}, 2023.
+
+\bibitem{chexagent} Chen, Z., et al.. CheXagent: A Vision-Language Foundation Model to Enhance Efficiency of Chest X-ray Interpretation. \emph{arXiv:2401.12208}, 2024.
+
+\bibitem{diseaseaware} Wu, P., et al.. A Disease-Aware Dual-Stage Framework for Chest X-ray Report Generation. \emph{AAAI}, 2026.
+
+\bibitem{s2dalign} Gao, J., et al.. S2D-ALIGN: Shallow-to-Deep Auxiliary Learning for Anatomically-Grounded Radiology Report Generation. \emph{arXiv:2511.11066}, 2025.
+
+\bibitem{cxrmate2} Nicolson, A., et al.. CXRMate-2: Structured Multimodal Temporal Embeddings and Tractable Reinforcement Learning for Clinically Acceptable Chest X-ray Radiology Report Generation. \emph{arXiv:2604.18967}, 2026.
+
+\bibitem{riha} Chen, Y., et al.. RIHA: Report-Image Hierarchical Alignment for Radiology Report Generation. \emph{JBHI}, 2026.
+
+\bibitem{marlrad} Baba, K., et al.. MARL-Rad: Multi-Modal Multi-Agent Reinforcement Learning for Radiology Report Generation. \emph{arXiv:2603.16876}, 2026.
 
 \bibitem{xrayclaw} Young, S., Xu, L. XrayClaw: Cooperative-Competitive Multi-Agent Alignment for Trustworthy Chest X-ray Diagnosis. \emph{arXiv:2604.02695}, 2026.
 
-\bibitem{autogen} Wu, Q., et al. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. \emph{arXiv:2308.08155}, 2023.
-
-\bibitem{chexmix} Kumar, A., et al. CheXmix: Unified Generative Pretraining for Vision Language Models in Medical Imaging. \emph{CVPR Findings}, 2026.
-
-\bibitem{maarta} Awasthi, A., et al. MAARTA: Multi-Agentic Adaptive Radiology Teaching Assistant. \emph{MICCAI}, 2025.
-
-\bibitem{imactcxr} Le, T.A., et al. IMACT-CXR: An Interactive Multi-Agent Conversational Tutoring System for Chest X-Ray Interpretation. \emph{ISBI}, 2026.
-
-\bibitem{cemrag} Salm\`{e}, M., et al. Concept-Enhanced Multimodal RAG: Towards Interpretable and Accurate Radiology Report Generation. \emph{arXiv:2602.15650}, 2026.
-
-\bibitem{green} Ostmeier, S., et al. GREEN: A Clinical Efficacy Metric for Radiology Report Generation. \emph{NAACL}, 2024.
-
-\bibitem{radgraph} Jain, S., et al. RadGraph: Extracting Clinical Entities and Relations from Radiology Reports. \emph{NeurIPS Datasets and Benchmarks}, 2021.
-
-\bibitem{mimiccxr} Johnson, A.E.W., et al. MIMIC-CXR: A Large Publicly Available Database of Labeled Chest Radiographs. \emph{Scientific Data}, 2019.
-
-\bibitem{chexpert} Irvin, J., et al. CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison. \emph{AAAI}, 2019.
+\bibitem{autogen} Wu, Q., et al.. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. \emph{arXiv:2308.08155}, 2023.
+
+\bibitem{chexmix} Kumar, A., et al.. CheXmix: Unified Generative Pretraining for Vision Language Models in Medical Imaging. \emph{CVPR Findings}, 2026.
+
+\bibitem{maarta} Awasthi, A., et al.. MAARTA: Multi-Agentic Adaptive Radiology Teaching Assistant. \emph{MICCAI}, 2025.
+
+\bibitem{imactcxr} Le, T. A., et al.. IMACT-CXR: An Interactive Multi-Agent Conversational Tutoring System for Chest X-Ray Interpretation. \emph{ISBI}, 2026.
+
+\bibitem{cemrag} Salm\`{e}, M., et al.. Concept-Enhanced Multimodal RAG: Towards Interpretable and Accurate Radiology Report Generation. \emph{arXiv:2602.15650}, 2026.
+
+\bibitem{green} Ostmeier, S., et al.. GREEN: A Clinical Efficacy Metric for Radiology Report Generation. \emph{NAACL}, 2024.
+
+\bibitem{radgraph} Jain, S., et al.. RadGraph: Extracting Clinical Entities and Relations from Radiology Reports. \emph{NeurIPS Datasets and Benchmarks}, 2021.
+
+\bibitem{mimiccxr} Johnson, A. E. W., et al.. MIMIC-CXR: A Large Publicly Available Database of Labeled Chest Radiographs. \emph{Scientific Data}, 2019.
+
+\bibitem{chexpert} Irvin, J., et al.. CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison. \emph{AAAI}, 2019.
 
 \end{thebibliography}
 
```
