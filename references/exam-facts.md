# 考试事实与领域权重（速查）

> 建档与考前一页纸用。**权威源是 `certifications/<体系>/program.json` 与 `tracks/<slug>.json`**，本文件是带日期的速查版；`lastVerified` 之后政策可能变化，花钱报名前必须让用户重核官方页面。

## 体系一：Claude Certification Curriculum（publisher: AI Engineering from Scratch）

`program.json` 关键字段：`lastVerified: 2026-08-09`、`guideVersion: 1.0`（2026 年 7 月生效）。

| 考试码 | 轨道 | 题数 | 时长 | 费用 | 通过线 | 有效期 | 课时（core route） |
|---|---|---|---|---|---|---|---|
| CCAO-F | Claude Certified Associate - Foundations | 60 | 120 min | $99 | **720/1000 量表** | 12 个月 | 9 lessons |
| CCDV-F | Claude Certified Developer - Foundations | 53 | 120 min | $125 | 720/1000 | 12 个月 | 15 lessons |
| CCAR-F | Claude Certified Architect - Foundations | 60 | 120 min | $125 | 720/1000 | 12 个月 | 21 lessons |
| CCAR-P | Claude Certified Architect - Professional | 63 | 120 min | $175 | 720/1000 | 12 个月 | 25 lessons |

- 题型：Multiple-choice and multiple-response；交付：线上监考或考试中心
- **路线依赖**：Associate ← 共享地基；Developer ← 地基；Architect-F ← Developer；Architect-P ← Architect-F（先考前轨再考后轨）

### 三段声明（建档必读，照原文口径）

1. **报考资格**：截至 2026-08-09，官方考试报名限 Claude Partner Network 组织人员，需认可的合作企业邮箱。本开放课程人人可学；**付费或排期前先核当前资格**，规则会变。
2. **分数口径**：本课程练习百分比是原始分，**不等同**于 Anthropic 的 100-1000 量表分，**不能预测**官方结果。
3. **性质声明**：独立社区课程，与 Anthropic 无隶属/授权关系，**不含真题**；官方考试指南与现行政策永远优先。

### CCAO-F 领域权重（示例，其余轨道用 `cert.py track <slug>` 查）

| domain | 权重% |
|---|---|
| output-evaluation-validation | 21 |
| workflow-integration-solution-design | 16 |
| governance-risk-responsible-use | 15 |
| prompting-task-execution | 14 |
| product-model-selection | 12 |
| configuration-knowledge-management | 12 |
| troubleshooting-optimization | 10 |

**排课原则：权重 × 当前得分率 = 补课优先级**，两个都差的领域排最前。

### 内置学习计划

每轨 `studyPlans` 自带 **14 天** 和 **28 天** 两版（`ccao-f-14-day` / `ccao-f-28-day`），按考试日期二选一，别自己发明排期。

## 体系二：MCPA（Agentic AI Foundation / Linux Foundation Training）

`mcpa/program.json` 关键字段：`lastVerified: 2026-09-24`、guide 2026 年 9 月生效。

| 项 | 值 |
|---|---|
| 考试 | Model Context Protocol Associate（MCPA） |
| 级别 | Beginner |
| 时长 | 90 min（注意：官网列 90 分钟，发布公告曾写 120 分钟——**以官网当前值为准**） |
| 费用 | $250 |
| 题型 | Multiple choice，线上监考 |
| 依据规范 | MCP spec dated 2026-07-28 |
| 有效期 | 2 年 |
| 重考 | 含 1 次重考；报考窗口 12 个月 |
| 官方题数/通过分 | **未公布**——本课程 3 套 60 题模拟卷是自拟练习集，长度非官方，百分比不能预测官方结果 |
| 课时 | 34 lessons |

每个考务事实与检索日期记录在仓库 `research/source-verification-ledger.md`——要引用细节就去那里核。

## 两套体系的备考节奏差异

| | Claude 四轨 | MCPA |
|---|---|---|
| 模考量 | 每轨 diagnostic(25min) + mock-01(120min) | diagnostic + **mock-01/02/03** 三套 |
| 计划 | 14/28 天 studyPlans | 按 34 课自排（建议 21-28 天） |
| 分数线 | 明确 720/1000 | 未知 → 只看原始分趋势 |
| 领域 | 每轨 6-7 个 domain 带权重 | 见 mcpa track JSON |
| 重考政策 | 未在本仓库说明 → 查官方 FAQ | 含 1 次重考 |

## 引用规范

- 报告/一页纸里每个数字后标来源：`track JSON (lastVerified 2026-08-09)` 或 `official page (访问日期)`
- 任何与本文件冲突的用户记忆 → 以 JSON 为准，当场 `cert.py track <slug>` 打出来看
