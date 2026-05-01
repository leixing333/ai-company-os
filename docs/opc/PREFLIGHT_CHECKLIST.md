# OPC 工作台开发前置更新完成清单

> 本文件记录了在开始 OPC 可视化工作台开发前，对系统文件进行的所有规范化更新。
> 完成时间：2026-05-02

## 更新状态总览

| 编号 | 涉及文件/目录 | 更新内容 | 状态 |
|---|---|---|---|
| 1 | `1_company/agents/ceo/` | 新建目录，创建 CEO SOUL.md | ✅ 已完成 |
| 2 | `2_strategy/agents/strategist/` | 新建目录，创建策略官 SOUL.md | ✅ 已完成 |
| 3 | 全部 19 个现有 SOUL.md | 统一添加 YAML Frontmatter（role/name/team/model/layer/channel） | ✅ 已完成 |
| 4 | `kairos_logs/FORMAT.md` | 制定 JSON Lines 统一日志格式规范 | ✅ 已完成 |
| 5 | `kairos_logs/2026-04-29.jsonl` | 创建符合新格式的示例日志文件 | ✅ 已完成 |
| 6 | `1_strategy/finance_tracker.csv` | 规范化列名，补充财务数据结构 | ✅ 已完成 |
| 7 | `.opc/config.json` | 新增 `ui` 配置块和 `kairos_logs`/`finance_tracker`/`souls` 路径 | ✅ 已完成 |

## SOUL.md Frontmatter 规范

所有 SOUL.md 现在包含以下统一的 YAML Frontmatter：

```yaml
---
role: "角色英文名称"
name: "角色中文名 (英文名)"
team: "所属团队 (company/strategy/marketing/production/design/operations)"
model: "使用的 LLM 模型"
layer: "所在层级目录"
channel: "#频道名"
---
```

## kairos_logs JSON Lines 格式规范

每条日志为独立 JSON 对象，必须包含：
- `timestamp`：ISO 8601 格式时间戳
- `agent`：操作的 Agent 名称
- `action_type`：DECISION / STATUS / ESCALATION / MILESTONE / TASK_ASSIGN
- `task_id`：关联的项目 ID
- `summary`：一句话摘要
- `details`：详细信息对象（DECISION 类型必须包含 reason/alternatives/final_choice）

## 下一步
系统文件前置更新已全部完成，可以开始 OPC 工作台的 Phase 1 开发。
