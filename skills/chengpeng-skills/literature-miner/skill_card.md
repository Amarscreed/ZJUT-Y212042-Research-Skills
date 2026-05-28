# Skill Card: literature-miner

## 1. Basic Information

| Item | Content |
|------|---------|
| Skill Name | literature-miner |
| Group | 程鹏211125120093、诸葛梦豪221125120224、施贵峰221125120167 |
| Research Scenario | 文献挖掘 / Literature Mining |
| Target Users | 研究生、论文作者、研究组长 |
| GitHub 路径 | chengpeng-skills/literature-miner/ |

## 2. Research Pain Point

写 Related Work 和找创新点时常需要大量阅读最新顶会论文，但时间有限。可能遗漏了重要相关工作。

## 3. What This Skill Does

### This skill can:
1. 按主题关键词搜索内置论文数据库（20+ 已验证的 2025-2026 顶会/顶刊论文）
2. 解析用户论文，识别当前方法
3. 对照已知论文数据库，生成具体的创新增强建议
4. 每条建议标注启发论文和具体适配方法
5. 输出结构化 MD 报告

### This skill does not aim to:
1. 不连接学术搜索引擎做实时全网搜索
2. 不判断引用是否真正拓展了论文的方法
3. 不保证建议的可行性

## 4. Required Inputs

The skill expects one or more of the following inputs:
- 论文 .tex 文件
- 搜索主题关键词

### Example input files:
```
examples/input/
├── paper.tex
```

## 5. Expected Outputs

The skill produces:
- 文献挖掘报告 .md
- 创新增强建议 .md

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
1. 搜索模式：根据主题关键词匹配内置论文数据库
2. 分析模式：解析用户论文 -> 识别当前方法 -> 对照已知论文 -> 生成增强建议
3. 每条建议包括：增强领域、启发论文、具体适配方法、预期效果
4. 生成结构化报告

## 7. Group-Specific Feature

内置 20+ 篇精心整理的 2025-2026 顶会论文，覆盖 CXR 报告生成、多智能体医学 AI、医学教育三大方向

## 8. Demo Case

### Demo Input
See: examples/input/

### Demo Output
See: examples/output/

## 9. Evaluation

| Criterion | Description |
|-----------|-------------|
| Relevance | Do search results match the topic? |
| Suggestion quality | Are enhancement suggestions concrete and actionable? |
| Coverage | Does the database cover the main research directions? |

## 10. Limitations

This skill may fail when:
- 数据库规模有限（20+ 篇），非全面搜索
- 增强建议基于规则生成，可能不适合所有论文
- 无法实时更新论文数据库

## 11. Safety and Privacy

This skill should not:
- Read private files unrelated to the research task
- Store or expose personal data
- Fabricate experimental results or paper references
- Claim certainty when evidence is insufficient

## 12. Future Improvements

- 连接到 Semantic Scholar / Google Scholar API
- 增加论文影响力评分（引用量、h-index）
- 支持按时间范围、venue 层级过滤

## 13. Repository Information

| Item | Content |
|------|---------|
| Folder Path | chengpeng-skills/literature-miner/ |
| Main File | SKILL.md |
| Skill Card | skill_card.md |
| Example Input | examples/input/ |
| Example Output | examples/output/ |
