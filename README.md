# ai-cert-coach

> 开源**认证备考教练**（SKILL）——驱动 [AI Engineering from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch) 的 `certifications/` 两套体系：**Claude 四认证轨**（CCAO-F / CCDV-F / CCAR-F / CCAR-P，53-63 题、120 分钟、720/1000 分制）+ **MCPA**（Linux Foundation 体系，90 分钟、3 套模拟卷）。诊断卷摸底 → 按领域权重排课 → 限时防剧透模考 → 弱项回链补课 → 考前一页纸。

备考的两个死穴：**分数自我感觉**（"我应该能过"）和**事实凭记忆**（"好像 700 分就过"）。这个 Skill 用官方规格的监考协议和只从 JSON 引用的考试事实把两处钉死。

## 五件套定位

| Skill | 管什么 | 交付物 |
|---|---|---|
| 学习型（上课） | 输入：理解 | 考核通过的课时 |
| 特训型（练题） | 输出：手搓代码 | 毕业的练习题 |
| 面试型（被考） | 检验：定级 | 模拟面试报告 |
| 作品集型（做项目） | 产出：真东西 | 过完成测试的项目 |
| **本 Skill（备考）** | **拿凭证：考试** | **模考趋势 + 弱项清单 + 考前一页纸** |

弱领域回链的课交给学习型；`references` 指向的 `practice/` 题交给特训型；Claude 轨的 artifact 路线（治理工作流/协议应用/架构方案）交给作品集型。五件独立安装，互不依赖。

## 仓库结构

```
ai-cert-coach/
├── SKILL.md                        # 主文档：建档 + 日常三件事 + 考前一周 + 7 条铁律
├── README.md
├── LICENSE
├── references/
│   ├── exam-facts.md               # 两体系考试事实表 + 领域权重 + 三段声明原文
│   └── study-protocol.md           # 监考细则、判分回链、模考排期、考前清单
├── templates/
│   ├── cert-plan.md                # 备考计划（轨道/考试日/诊断基线/领域作战表）
│   ├── mock-report.md              # 模考报告（原始分/领域拆分/错题复述）
│   └── exam-eve.md                 # 考前一页纸
└── scripts/
    └── cert.py                     # programs/track/route/count/ask/reveal/log/status（零依赖）
```

## 两套体系（事实以仓库 JSON 为准，下表带 lastVerified）

**Claude 认证课程**（lastVerified 2026-08-09，指南 1.0 版 2026 年 7 月生效）

| 考试码 | 题数 | 时长 | 费用 | 通过线 | 有效期 | 课时 |
|---|---|---|---|---|---|---|
| CCAO-F Associate Foundations | 60 | 120 min | $99 | 720/1000 | 12 月 | 9 |
| CCDV-F Developer Foundations | 53 | 120 min | $125 | 720/1000 | 12 月 | 15 |
| CCAR-F Architect Foundations | 60 | 120 min | $125 | 720/1000 | 12 月 | 21 |
| CCAR-P Architect Professional | 63 | 120 min | $175 | 720/1000 | 12 月 | 25 |

**MCPA**（lastVerified 2026-09-24）：90 分钟 / $250 / 初级 / 34 课 / 诊断卷 + 3 套 60 题模拟卷 / 2 年有效 / 含 1 次重考 / 报考窗口 12 个月。官方题数与通过分**未公布**。

**三段声明**（建档必读）：① 报考资格——Claude 轨截至 2026-08-09 限 Partner 组织人员，付费前重核；② 分数口径——练习百分比是原始分，不等于官方量表分，不能预测官方结果；③ 性质——独立社区课程，非官方授权，不含真题。

## 核心机制

### 防剧透监考
```bash
python scripts/cert.py ask ccao-f/mock-01 1    # 只出题面+选项
# 用户作答（single 选 1 / multiple 多选须完全一致）
python scripts/cert.py reveal ccao-f/mock-01 1 # 全卷答完才亮答案+解析+回链
python scripts/cert.py log ccao-f --mock mock-01 --correct 47 --total 60 --timed
```
**整卷作答完成前不 reveal 任何一题**——真实考试没有"先看看"按钮。掐表按卷面限时（诊断 25 分钟 / Claude mock 120 分钟），到点停笔，练知识也练节奏。

### 判分三件套
原始分 % + **分领域得分率**（领域权重在 track JSON）+ 用时。报分必带后缀：*"原始分 ≠ 官方量表分，不能预测官方结果"*。

### 弱项回链
错题 `domain` → `objectives` → `references` 指向的课回炉；同领域两卷都弱 → 标红进"每日 15 分钟专项"；每条错题 `explanation` **用自己的话复述**——复述不出等于没读，下次模考必再考。

### 倒排节奏
学课期每 7 天 1 套模考找洞 → 考前 7-3 天全真限时 → 前一天只过 `exam-eve.md` 一页纸（考试事实从 track JSON 抄 + lastVerified 日期，不凭记忆）。

## 如何使用

**① 作为 Agent 技能安装**：本目录克隆/复制到你的 AI Agent 识别技能的目录，目录名保持 `ai-cert-coach`，`SKILL.md` 直接位于其内；课程仓库克隆到任意位置（脚本自动向上找）。

**② 直接当开场指令**：`SKILL.md` 全文发给 Agent，再说"带我备考 [考试码]"。

**③ 只用监考脚本**：
```bash
python scripts/cert.py programs
python scripts/cert.py track ccao-f          # 考试事实 + 领域权重
python scripts/cert.py route mcpa-f          # 34 课路线
python scripts/cert.py count ccao-f/mock-01  # 卷面信息
python scripts/cert.py ask / reveal / log / status
```

## 环境准备

| 依赖 | 用途 | 获取方式 |
|---|---|---|
| **AI Agent**（Claude Code / Codex / 其他支持 SKILL.md 的宿主） | 执行备考协议 | 你现有的工具链 |
| **课程仓库** | 题库、track/program JSON、课 | `git clone --depth 1 https://github.com/rohitg00/ai-engineering-from-scratch.git` |
| **Python ≥ 3.9** | 跑监考脚本 | 无第三方依赖 |

## 快速开始

1. 克隆课程仓库（任意位置）
2. 安装本 Skill（或把 `SKILL.md` 发给你的 Agent）
3. 说 **"带我备考"** → 四问建档（考哪个/日期/每天投入/基础）→ **读三段声明** → 诊断卷摸底 → 拿到 `cert-plan.md`
4. 日常：按 route 学课 + 每 7 天限时模考 + 弱项回链
5. 考前一周：全真模考 → `exam-eve.md` 一页纸 → 上考场

## 设计原则

1. **先答后对**——答案提前露脸，模考退化成朗读
2. **原始分只找洞不算命**——口径声明跟着每次报分走
3. **事实只从 JSON 来**——题数/费用/通过线带 lastVerified，不凭记忆
4. **资格先核**——花钱报名之前先核报考资格与最新政策
5. **弱项必回链**——domain → objective → 课，错题解析必须复述得出
6. **状态落盘**——进度双文件，换会话能接

## 常见问题

**Q：和课程仓库自带的 claude-certification / mcpa-certification skills 什么关系？**
互补。本 Skill 是独立实现的备考协议与监考记账工具，不依赖其内部状态格式（原体系进度文件是 `CLAUDE-CERTIFICATION.md`），可单独用、可裁剪。

**Q：能报上名吗？**
截至仓库 lastVerified（2026-08-09），Claude 认证限 Partner Network 组织人员；MCPA 有 12 个月报考窗口。**资格与费用都会变，付费前必须核官方页面**——这是建档铁律。

**Q：模考分数能推算能不能过吗？**
不能，两套体系都明确：练习百分比是原始分，Claude 官方是 100-1000 量表（720 过），MCPA 官方通过分未公布。分数的唯一用途是找弱领域。

**Q：题目会更新吗？**
会——本仓库不复制任何题，以课程仓库 `certifications/` 为准，上游 `git pull` 即同步；`exam-facts.md` 是带日期的速查索引，权威以 `program.json` / `track JSON` 为准。

**Q：进度文件要提交 git 吗？**
建议提交（复盘资产）；想私有加进 `.gitignore`。

## 致谢

- 课程、题库、考试事实映射与全部课件：[rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch)（MIT）
- Claude 认证与 MCPA 的官方归属其各自机构；本仓库只提供备考协议与监考工具，非官方授权、不含真题

## License

[MIT](./LICENSE)
