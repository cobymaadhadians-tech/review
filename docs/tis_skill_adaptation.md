# 将 `research-skills` 从“医学影像综述”改造成“TIS（时间干涉刺激）综述”技能

## 1) 先改元数据（触发词）

在该 skill 的 `SKILL.md` frontmatter 中：

- `name`：改为能体现 TIS 的名字（如 `tis-review-writer`）。
- `description`：明确触发条件，至少包含以下关键词：
  - `temporal interference stimulation`
  - `TIS`
  - `non-invasive deep brain stimulation`
  - `electric field modeling`
  - `safety / dosage / protocol`
  - `literature review / systematic review`

目标：让模型在“写 TIS 综述、比较 TIS 参数与机制、整理实验与临床证据”时自动触发，而不是被“医学影像”限定。

---

## 2) 重写 SKILL.md 主流程（从影像流程切换到神经调控流程）

建议把主流程固定为 7 步：

1. **定义综述问题（PICO/PECO）**：
   - 人群/模型（健康受试者、患者、动物、仿真）
   - 干预（carrier frequency、beat frequency、electrode montage、电流强度、时长）
   - 对照（sham、tACS/tDCS、基线）
   - 结局（行为、EEG/fMRI、生理指标、不良事件）

2. **检索与纳入排除标准**：
   - 数据库：PubMed、Web of Science、Scopus、IEEE Xplore（仿真/工程文献很关键）
   - 时间窗、语言、文章类型

3. **证据分层**：
   - 机制/理论
   - 仿真（电场、头模型）
   - 动物
   - 人体（健康）
   - 临床

4. **参数标准化抽取**（核心）：
   - carrier/beat 频率
   - 电极位置与数量
   - 电流与电流密度
   - 刺激时长与会话数
   - 目标脑区与深部聚焦证据

5. **偏倚与质量评估**：
   - 随机化、盲法、样本量、预注册、统计功效

6. **跨研究可比性处理**：
   - 单位统一（mA、Hz、min）
   - 协变量标注（头模型、组织电导率、个体解剖差异）

7. **输出结构化综述草稿**：
   - 机制、疗效、安全性、参数建议、证据缺口、未来研究路线图

---

## 3) 新增 references（把“影像专有内容”替换为“TIS 专有知识”）

建议目录：

- `references/tis_search_strategy.md`
- `references/tis_data_extraction_schema.md`
- `references/tis_risk_of_bias.md`
- `references/tis_safety_and_ethics.md`
- `references/tis_reporting_template.md`

其中最关键的是 `tis_data_extraction_schema.md`，建议至少包含字段：

- 文献信息：作者、年份、研究类型
- 对象：样本量、年龄、疾病/模型
- 刺激参数：carrier、beat、波形、相位关系
- 电极与设备：montage、接触面积、设备型号
- 剂量：峰值电流、总电荷、会话次数
- 建模信息：头模型来源、网格、组织电导率、仿真软件
- 结果：行为/神经指标、效应量、统计显著性
- 安全性：皮肤不适、头痛、严重不良事件
- 证据等级与偏倚风险

---

## 4) 增加 scripts（减少重复劳动）

推荐加入：

- `scripts/build_query.py`：自动拼接 TIS 检索式（PubMed/WoS/Scopus 版本）
- `scripts/extract_table.py`：把文献笔记整理为统一 CSV/JSON 表头
- `scripts/check_units.py`：自动检查 Hz/mA/min 单位一致性
- `scripts/make_outline.py`：生成综述章节骨架（机制→证据→安全→展望）

这样可以把“容易错、重复高”的部分低自由度固定下来。

---

## 5) 在 SKILL.md 中加入“条件加载”

按 skill-creator 的 progressive disclosure 思路，把细节移到 references，只在需要时加载：

- 用户问“检索式怎么写”→ 读 `tis_search_strategy.md`
- 用户问“参数表怎么提取”→ 读 `tis_data_extraction_schema.md`
- 用户问“安全性如何写”→ 读 `tis_safety_and_ethics.md`

这样不会把上下文塞满，也更稳定。

---

## 6) 给出可直接复用的输出模板

在 `references/tis_reporting_template.md` 预置：

- 摘要模板
- 方法（检索、筛选、质量评估）模板
- 结果模板（按证据层级）
- 讨论模板（机制解释 + 争议 + 临床转化）
- 结论与研究建议模板

并要求每一节都输出：

- 已证实结论
- 尚不一致证据
- 高优先级研究空白

---

## 7) 最小可行改造（你可以先做这三件）

1. 改 `SKILL.md` 的 `description`，加入 TIS 触发词。
2. 新建 `references/tis_data_extraction_schema.md`。
3. 新建 `scripts/build_query.py`。

只做这三步，skill 就能从“影像综述助手”转成“TIS 综述助手”的可用版本。

---

## 8) 示例：TIS 检索词骨架（可放入脚本）

```text
("temporal interference" OR "temporal interference stimulation" OR TIS)
AND
(brain OR cortical OR deep brain)
AND
(stimulation OR neuromodulation)
AND
(modeling OR simulation OR clinical OR human OR animal)
NOT
("temporal interference microscopy")
```

可再加疾病词（如 depression, Parkinson, epilepsy）形成主题子检索。
