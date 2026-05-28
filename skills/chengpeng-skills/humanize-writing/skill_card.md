# Skill Card: humanize-writing

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | humanize-writing |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 论文写作 / Paper Writing |
| Target Users | 研究生、论文作者 |
| GitHub 路径 | chengpeng-skills/humanize-writing/ |

## 2. Research Pain Point

研究生使用 AI 辅助写作时，生成的文本常有明显的 AI 味：过度转承、重复句式、空泛修饰语。人工逐句修改耗时且不稳定。

## 3. What This Skill Does

### This skill can:
1. 检测并移除 AI 常见用语模式（过度 hedging、冗余过渡、空泛修饰）
2. 改进句法多样性、增加自然断句
3. 去除虚假精确表达和无数据支撑的夸大表述
4. 对比修改前后的 AI-ism 密度和可读性评分

### This skill does not aim to:
1. 不改变科学含义或技术内容
2. 不做事实核查
3. 不自动改写完整段落（只做局部优化）

## 4. Required Inputs

The skill expects one or more of the following inputs:
- 论文 .tex 文件
- 论文 .md 文件
- 论文段落纯文本

### Example input files:
```
examples/input/
├── paper.tex
```

## 5. Expected Outputs

The skill produces:
- 修改后的 .tex 文件
- 修改差异 .md 文件
- AI-ism 密度变化报告

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
1. 检测 AI 典型模式（过度 hedging、空泛过渡、公式化开头、被动语态过度）
2. 按优先级应用人类化变换（去 hedging → 变句首 → 断长句 → 去冗余过渡 → 加作者声音）
3. 生成修改前后对比 .md 报告
4. 输出修改后的 .tex 文件

## 7. Group-Specific Feature

结合了可读性统计（Flesch 指数）和 AI-ism 密度检测，能定量评估人化效果

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| AI-ism removal rate | Percentage of detected patterns removed |
| False positive rate | Non-AI patterns incorrectly modified |
| Readability improvement | Flesch Reading Ease change before/after |

## 10. Limitations

This skill may fail when:
- 对高度领域化的术语可能过度简化
- 无法判断事实准确性
- 仅限于文本层面，无法改善逻辑结构

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the research task
- Store or expose personal data
- Fabricate experimental results or paper references
- Claim certainty when evidence is insufficient

## 12. Future Improvements

- 支持更多语言（中文学术写作）
- 集成到 LaTeX 编译流程中
- 增加可定制的 AI-ism 检测规则

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/humanize-writing/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
