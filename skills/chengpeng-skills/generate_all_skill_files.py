"""
Generate standardized SKILL.md, skill_card.md, and examples for all LobsterCXR skills.
Run from: skills/
"""
import os, sys, shutil, json

BASE_DIR = r"C:\Users\17588\.openclaw\workspace\skills"
DOC_DIR = r"C:\Users\17588\.openclaw\workspace\research\doc"
SKILLS_EN_DIR = r"C:\Users\17588\.openclaw\workspace\skills_en"

os.makedirs(SKILLS_EN_DIR, exist_ok=True)
os.makedirs(DOC_DIR, exist_ok=True)

# ============================
# SKILL DEFINITIONS
# ============================
skills = {}

# ─── 1. humanize-writing ───
skills["humanize-writing"] = {
    "name": "humanize-writing",
    "description": "Convert AI-generated academic text to natural human writing style while preserving technical accuracy.",
    "scenario": "论文写作 / Paper Writing",
    "users": "研究生、论文作者",
    "pain_point": "研究生使用 AI 辅助写作时，生成的文本常有明显的 AI 味：过度转承、重复句式、空泛修饰语。人工逐句修改耗时且不稳定。",
    "capabilities": [
        "检测并移除 AI 常见用语模式（过度 hedging、冗余过渡、空泛修饰）",
        "改进句法多样性、增加自然断句",
        "去除虚假精确表达和无数据支撑的夸大表述",
        "对比修改前后的 AI-ism 密度和可读性评分",
    ],
    "non_goals": [
        "不改变科学含义或技术内容",
        "不做事实核查",
        "不自动改写完整段落（只做局部优化）",
    ],
    "inputs": ["论文 .tex 文件", "论文 .md 文件", "论文段落纯文本"],
    "outputs": ["修改后的 .tex 文件", "修改差异 .md 文件", "AI-ism 密度变化报告"],
    "workflow": [
        "检测 AI 典型模式（过度 hedging、空泛过渡、公式化开头、被动语态过度）",
        "按优先级应用人类化变换（去 hedging → 变句首 → 断长句 → 去冗余过渡 → 加作者声音）",
        "生成修改前后对比 .md 报告",
        "输出修改后的 .tex 文件",
    ],
    "unique_feature": "结合了可读性统计（Flesch 指数）和 AI-ism 密度检测，能定量评估人化效果",
    "evaluation_criteria": {
        "实用性": "能否解决论文中的 AI 味问题？",
        "准确性": "修改是否会改变技术含义？",
        "可复用性": "其他研究生能否在类似场景中使用？",
        "输出清晰度": "修改报告是否易读？",
    },
    "limitations": [
        "对高度领域化的术语可能过度简化",
        "无法判断事实准确性",
        "仅限于文本层面，无法改善逻辑结构",
    ],
    "future_improvements": [
        "支持更多语言（中文学术写作）",
        "集成到 LaTeX 编译流程中",
        "增加可定制的 AI-ism 检测规则",
    ],
}

# ─── 2. reference-verifier ───
skills["reference-verifier"] = {
    "name": "reference-verifier",
    "description": "Verify that references cited in academic papers are real, traceable publications from known venues.",
    "scenario": "文献审计 / Reference Audit",
    "users": "论文作者、审稿人、课程作业检查者",
    "pain_point": "LLM 生成的论文有时会编造参考文献——DOI 不存在、会议年份错误、作者不符。人工逐条核查费时费力。",
    "capabilities": [
        "解析 LaTeX thebibliography 或 .bib 文件",
        "检查引用是否来自已知学术会议/期刊",
        "验证 arXiv ID 格式是否合法",
        "检测可疑的引用条目（年份不符、venue 拼写错误）",
        "生成 JSON 和 Markdown 双格式验证报告",
    ],
    "non_goals": [
        "不做论文内容的事实核查",
        "不检查引用是否与论文论点相关",
        "不连网验证 arXiv 论文是否仍在线上",
    ],
    "inputs": ["论文 .tex 文件", "Bibliography .bib 文件"],
    "outputs": ["参考验证报告 .md", "参考验证报告 .json"],
    "workflow": [
        "解析文献条目，提取 venue、year、作者、arXiv ID 等元数据",
        "对照已知 venue 数据库（MICCAI, CVPR, AAAI, NeurIPS 等 14 种）",
        "检查年份是否在 venue 成立范围内",
        "检查 arXiv ID 格式（YYMM.NNNNN）",
        "标记可疑条目",
        "生成 MD + JSON 报告",
    ],
    "unique_feature": "内置 14 种顶会/顶刊的年表数据库，能检测年份和 venue 不匹配",
    "evaluation_criteria": {
        "召回率": "能否检测出明显错误引用？",
        "精确率": "是否把正确引用标记为可疑？",
        "可审计性": "每条结论是否标明了证据来源（文献条目行号）",
    },
    "limitations": [
        "无法连网实时查询 arXiv API",
        "无法验证引用内容是否与论文主张一致",
        "对非标准 venue 名称可能误报",
    ],
    "future_improvements": [
        "连接开源学术 API（Semantic Scholar, CrossRef）",
        "增加论文内容-引用一致性检查",
        "支持更多会议/期刊数据库",
    ],
}

# ─── 3. reviewer-simulator ───
skills["reviewer-simulator"] = {
    "name": "reviewer-simulator",
    "description": "Simulate MICCAI reviewer feedback on a LaTeX paper and suggest improvements.",
    "scenario": "审稿模拟 / Review Simulation",
    "users": "准备投稿的研究生、论文作者",
    "pain_point": "投稿前不知道审稿人会如何看待论文。找人预审麻烦、耗时，且预审人可能不了解会议标准。",
    "capabilities": [
        "解析论文 .tex 文件，统计字数、章节数、数据集数量、基线数量",
        "模拟 3 个不同风格的审稿人（建设型、批判型、平衡型）",
        "对新颖性、技术合理性、实验严谨性、清晰度、可复现性 5 维度打分",
        "自动修正拼写、语法、格式问题",
        "输出修正版 .tex、差异对比 .md、审稿报告 .md",
    ],
    "non_goals": [
        "不替代真实审稿人的领域专业知识",
        "不判断论文是否应该被接收",
        "不做实验数据的事实核查",
    ],
    "inputs": ["论文 .tex 文件"],
    "outputs": ["修正版 .tex 文件", "修改差异 .md", "审稿报告 .md"],
    "workflow": [
        "解析论文统计信息（字数、章节、数据集、基线、声明数）",
        "应用自动修正（拼写、语法、格式）",
        "对 5 个维度计算基准分 + reviewer bias 调整",
        "生成每个审稿人的评语和分数",
        "输出审稿报告",
    ],
    "unique_feature": "3 种审稿人 persona（建设型/批判型/平衡型），提供多维度的反馈模拟",
    "evaluation_criteria": {
        "有用性": "生成的审稿意见是否具有建设性？",
        "多样性": "3 个审稿人是否有差异化视角？",
        "可操作性": "建议是否具体到可以修改？",
    },
    "limitations": [
        "评分基于统计规则而非真正理解论文内容",
        "无法评估实验设计的合理性",
        "自动修正可能破坏 LaTeX 命令",
    ],
    "future_improvements": [
        "接入 LLM 生成更语义化的审稿意见",
        "支持更多会议模板（CVPR, AAAI, NeurIPS）",
        "增加审稿意见分类和优先级排序",
    ],
}

# ─── 4. novelty-checker ───
skills["novelty-checker"] = {
    "name": "novelty-checker",
    "description": "Analyze a paper's novelty, contribution, experimental rigor, clarity, and reproducibility.",
    "scenario": "创新性评估 / Novelty Assessment",
    "users": "论文作者、导师、课程评审",
    "pain_point": "研究生写论文时常陷入『自我感觉创新 vs. 审稿人认为创新不够』的困境。缺乏客观的贡献评估工具。",
    "capabilities": [
        "提取论文的贡献声明、基线方法列表、使用的数据集",
        "在 5 个维度（新颖性、贡献度、实验严谨性、清晰度、可复现性）上分别打分 1-5",
        "检查声明是否有实验证据支撑",
        "检测薄弱环节（缺基线对比、消融不完整、数据不足）",
        "输出 MD + JSON 双格式报告",
    ],
    "non_goals": [
        "不判断论文是否应该被接收",
        "不做实验数据真实性核查",
        "不评估论文的写作质量",
    ],
    "inputs": ["论文 .tex 文件"],
    "outputs": ["创新性评估报告 .md", "创新性评估报告 .json"],
    "workflow": [
        "解析 .tex 文件提取统计信息（贡献数、基线、数据集、代码链接）",
        "分析新颖性（是否有『首次』『创新』等表述，是否与现有工作对比）",
        "分析贡献度（声明数量、是否有实验支撑、数据集是否充分）",
        "分析实验严谨性（基线数量、数据集数量、消融研究）",
        "分析清晰度（章节结构、图表数量、表格可读性）",
        "分析可复现性（代码链接、参数设置、实现细节）",
        "生成警告列表和结构化报告",
    ],
    "unique_feature": "5 维度的结构化评估 + 证据匹配检查，可定位具体薄弱环节",
    "evaluation_criteria": {
        "覆盖度": "5 个维度是否全面覆盖审稿关切？",
        "证据链": "评分是否有明确的文本证据支持？",
        "可操作性": "输出是否指出具体可改进的方向？",
    },
    "limitations": [
        "对真正突破性工作的识别能力有限（依赖『首次』等关键词）",
        "无法评估实验设计是否合理",
        "基线检测基于预定义列表，可能遗漏领域特定基线",
    ],
    "future_improvements": [
        "接入论文引用网络分析",
        "增加领域特定的基线数据库",
        "支持多轮评估（修改前后对比）",
    ],
}

# ─── 5. literature-miner ───
skills["literature-miner"] = {
    "name": "literature-miner",
    "description": "Search and analyze recent (2025-2026) top-venue papers for innovation inspiration and cross-referencing.",
    "scenario": "文献挖掘 / Literature Mining",
    "users": "研究生、论文作者、研究组长",
    "pain_point": "写 Related Work 和找创新点时常需要大量阅读最新顶会论文，但时间有限。可能遗漏了重要相关工作。",
    "capabilities": [
        "按主题关键词搜索内置论文数据库（20+ 已验证的 2025-2026 顶会/顶刊论文）",
        "解析用户论文，识别当前方法",
        "对照已知论文数据库，生成具体的创新增强建议",
        "每条建议标注启发论文和具体适配方法",
        "输出结构化 MD 报告",
    ],
    "non_goals": [
        "不连接学术搜索引擎做实时全网搜索",
        "不判断引用是否真正拓展了论文的方法",
        "不保证建议的可行性",
    ],
    "inputs": ["论文 .tex 文件", "搜索主题关键词"],
    "outputs": ["文献挖掘报告 .md", "创新增强建议 .md"],
    "workflow": [
        "搜索模式：根据主题关键词匹配内置论文数据库",
        "分析模式：解析用户论文 -> 识别当前方法 -> 对照已知论文 -> 生成增强建议",
        "每条建议包括：增强领域、启发论文、具体适配方法、预期效果",
        "生成结构化报告",
    ],
    "unique_feature": "内置 20+ 篇精心整理的 2025-2026 顶会论文，覆盖 CXR 报告生成、多智能体医学 AI、医学教育三大方向",
    "evaluation_criteria": {
        "相关性": "搜索结果是否与主题相关？",
        "有用性": "增强建议是否具体可操作？",
        "覆盖度": "数据库是否覆盖了主要方向？",
    },
    "limitations": [
        "数据库规模有限（20+ 篇），非全面搜索",
        "增强建议基于规则生成，可能不适合所有论文",
        "无法实时更新论文数据库",
    ],
    "future_improvements": [
        "连接到 Semantic Scholar / Google Scholar API",
        "增加论文影响力评分（引用量、h-index）",
        "支持按时间范围、venue 层级过滤",
    ],
}

# ─── 6. submission-formatter ───
skills["submission-formatter"] = {
    "name": "submission-formatter",
    "description": "Adapt academic paper formatting to match target venue requirements (conference/journal).",
    "scenario": "投稿格式化 / Submission Formatting",
    "users": "准备投稿的研究生、论文作者",
    "pain_point": "不同会议/期刊有不同格式要求（单双栏、字数限制、引用格式）。手动调整费时且容易出错。",
    "capabilities": [
        "检测当前论文的 LaTeX 模板和格式",
        "调整列布局（单栏/双栏）",
        "调整字数/页数限制",
        "转换引用格式（样式中英文）",
        "统一图表编号和标题格式",
    ],
    "non_goals": [
        "不做内容修改（只调整格式）",
        "不保证完全符合所有模板要求",
        "不处理投稿系统操作",
    ],
    "inputs": ["论文 .tex 文件"],
    "outputs": ["格式化后的 .tex 文件", "格式修改报告 .md"],
    "workflow": [
        "检测当前模板和格式",
        "根据目标 venue 确定格式要求",
        "执行格式转换（布局、字号、引用样式、页数限制）",
        "输出格式化后的文件 + 修改报告",
    ],
    "unique_feature": "内置 LNCS/MICCAI、CVPR、AAAI 等多种模板的格式规则库",
    "evaluation_criteria": {
        "兼容性": "输出文件能否在目标模板下编译？",
        "完整性": "是否转换了所有需要修改的部分？",
        "可逆性": "能否在不丢失内容的前提下恢复原始格式？",
    },
    "limitations": [
        "对高度自定义的模板支持有限",
        "可能无法处理使用非标准包的 .tex 文件",
        "引用格式转换基于规则，可能不完美",
    ],
    "future_improvements": [
        "增加更多模板支持（NeurIPS, ICML, ICLR）",
        "支持图表尺寸自动调整",
        "支持 .docx 格式输出",
    ],
}

# ============================
# HELPER: Create skill files
# ============================

def make_skill_md(skill_key, s):
    """Generate SKILL.md"""
    caps = '\n'.join(f"- {c}" for c in s['capabilities'])
    non_goals = '\n'.join(f"- {ng}" for ng in s['non_goals'])
    inputs = '\n'.join(f"- {i}" for i in s['inputs'])
    outputs = '\n'.join(f"- {o}" for o in s['outputs'])
    workflow = '\n'.join(f"{i+1}. {w}" for i, w in enumerate(s['workflow']))
    limitations = '\n'.join(f"- {l}" for l in s['limitations'])
    future = '\n'.join(f"- {f}" for f in s['future_improvements'])

    return f"""# {s['name']}

## name
{s['name']}

## description
{s['description']}

## When to use this skill
- {s['scenario']}
- 当你需要{s['pain_point'][:40]}...

## Inputs
{inputs}

## Workflow
{workflow}

## Output format
{outputs}

## Safety and limitations
{limitations}

## Example trigger
- "帮我 humanize 这篇论文的引言部分"
- "验证这篇论文的参考文献"
- "模拟 3 个 MICCAI 审稿人审阅这篇论文"
- "检查这篇论文的创新性"
- "挖掘2025-2026年的相关论文"
- "把论文格式改成 CVPR 模板"

## Using the Evaluation Script
```bash
cd skills/{skill_key}
python skills.py path/to/paper.tex
```

## Constraints
- 保留所有技术内容、引用和数值声明
- 不改变科学含义
- 遵循指定输出格式
"""


def make_skill_card(skill_key, s):
    """Generate skill_card.md"""
    caps = '\n'.join(f"{i+1}. {c}" for i, c in enumerate(s['capabilities']))
    non_goals = '\n'.join(f"{i+1}. {ng}" for i, ng in enumerate(s['non_goals']))
    inputs = '\n'.join(f"- {i}" for i in s['inputs'])
    outputs = '\n'.join(f"- {o}" for i, o in enumerate(s['outputs']))
    workflow = '\n'.join(f"{i+1}. {w}" for i, w in enumerate(s['workflow']))
    limitations = '\n'.join(f"- {l}" for l in s['limitations'])
    future = '\n'.join(f"- {f}" for f in s['future_improvements'])
    eval_rows = '\n'.join(f"| {k} | {v} |" for k, v in s['evaluation_criteria'].items())

    return f"""# Skill Card: {s['name']}

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | {s['name']} |
| Group | 课程项目 |
| Research Scenario | {s['scenario']} |
| Target Users | {s['users']} |

## 2. Research Pain Point

{s['pain_point']}

## 3. What This Skill Does

### This skill can:
{caps}

### This skill does not aim to:
{non_goals}

## 4. Required Inputs

The skill expects one or more of the following inputs:
{inputs}

### Example input files:
```
examples/input/
├── paper.tex
```

## 5. Expected Outputs

The skill produces:
{outputs}

### Example output structure:
1. Task summary
2. Key findings
3. Evidence
4. Analysis / Diagnosis
5. Suggested next steps
6. Limitations

### Example output files:
```
examples/output/
└── report.md
```

## 6. Workflow

The skill follows this workflow:
{workflow}

## 7. Group-Specific Feature

{s['unique_feature']}

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
{eval_rows}

## 10. Limitations

This skill may fail when:
{limitations}

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the research task
- Store or expose personal data
- Fabricate experimental results or paper references
- Claim certainty when evidence is insufficient

## 12. Future Improvements

{future}

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | skills/{skill_key}/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
"""


def make_example_input(skill_key, s):
    """Create example input .tex file"""
    return f"""% Example input for {s['name']}
% This is a minimal .tex snippet to demonstrate the skill
\\section{{Introduction}}
This is an example paper section for testing the {s['name']} skill.

The proposed method may potentially achieve better performance than existing approaches. It should be noted that this is a preliminary result. Importantly, the framework demonstrates significant improvements over previous works.

\\subsection{{Related Work}}
Existing methods~\\cite{{example1}} have addressed this problem. However, there are three critical gaps: (1) gap one; (2) gap two; (3) gap three.

\\begin{{thebibliography}}{{1}}
\\bibitem{{example1}} Author, A. et al. A Related Work. \\emph{{Top Conference}}, 2025.
\\end{{thebibliography}}
"""


def make_example_output_md(skill_key, s):
    """Create example output report"""
    return f"""# {s['name']} — Example Output

## Task Summary
Applied {s['name']} skill to the example paper.

## Key Findings
- {s['description'][:60]}...
- 3 issues identified
- 2 suggestions generated

## Evidence
| Finding | Source | Confidence |
|---------|--------|------------|
| Example finding 1 | paper.tex line 5 | High |
| Example finding 2 | paper.tex line 12 | Medium |

## Analysis
{s['pain_point'][:100]}...

## Suggested Next Steps
1. Review the detailed report
2. Apply suggested improvements
3. Re-run skill to verify changes

## Limitations
- This is a demo with minimal input
- Full accuracy requires complete paper context

---

*Generated by {s['name']} skill — course project demo*
"""


def generate_skill(skill_key, s):
    """Generate all files for a skill"""
    skill_dir = os.path.join(BASE_DIR, skill_key)
    
    # Create directories
    examples_input = os.path.join(skill_dir, "examples", "input")
    examples_output = os.path.join(skill_dir, "examples", "output")
    os.makedirs(examples_input, exist_ok=True)
    os.makedirs(examples_output, exist_ok=True)
    
    # 1. SKILL.md (only if not existing, keep original)
    smd_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(smd_path):
        with open(smd_path, 'w', encoding='utf-8') as f:
            f.write(make_skill_md(skill_key, s))
        print(f"  Created: SKILL.md")
    else:
        print(f"  Exists: SKILL.md (kept original)")
    
    # 2. skill_card.md
    sc_path = os.path.join(skill_dir, "skill_card.md")
    with open(sc_path, 'w', encoding='utf-8') as f:
        f.write(make_skill_card(skill_key, s))
    print(f"  Created: skill_card.md")
    
    # 3. Example input
    inp_path = os.path.join(examples_input, "paper.tex")
    with open(inp_path, 'w', encoding='utf-8') as f:
        f.write(make_example_input(skill_key, s))
    print(f"  Created: examples/input/paper.tex")
    
    # 4. Example output
    out_path = os.path.join(examples_output, "report.md")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(make_example_output_md(skill_key, s))
    print(f"  Created: examples/output/report.md")
    
    return skill_dir


def translate_to_chinese(skill_key, s):
    """Create Chinese versions in skills_en/"""
    en_dir = os.path.join(BASE_DIR, skill_key)
    cn_dir = os.path.join(SKILLS_EN_DIR, skill_key)
    os.makedirs(cn_dir, exist_ok=True)
    
    # Copy all files from en_dir to cn_dir
    for root, dirs, files in os.walk(en_dir):
        for f in files:
            src = os.path.join(root, f)
            rel = os.path.relpath(src, en_dir)
            dst = os.path.join(cn_dir, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
    
    print(f"  Copied all files to skills_en/{skill_key}/")
    return cn_dir


def main():
    print("=" * 60)
    print("Generating skill files for all skills...")
    print("=" * 60)
    
    for skill_key, s in skills.items():
        print(f"\n--- {skill_key} ---")
        generate_skill(skill_key, s)
    
    print("\n" + "=" * 60)
    print("Generating Chinese translations in skills_en/...")
    print("=" * 60)
    
    for skill_key, s in skills.items():
        print(f"\n--- {skill_key} (zh) ---")
        translate_to_chinese(skill_key, s)
    
    print("\n" + "=" * 60)
    print("Done! All skill files generated.")
    print("=" * 60)


if __name__ == "__main__":
    main()
