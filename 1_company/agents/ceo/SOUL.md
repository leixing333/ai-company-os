---
role: Chief Executive Officer (CEO)
team: company
model: human
layer: 1_company
channel: "#ceo"
---

# SOUL: CEO（首席执行官）

## 1. 角色定位
你是 OPC 公司的**人类 CEO**，也是整个多智能体操作系统的最终决策者和唯一的人类参与者。你的核心职责是进行**宏观委托**（Macro Delegation）和**微观引导**（Micro Steering）：通过 OPC 可视化工作台向 Agent 团队下达战略目标，并在关键节点进行审批和干预。

## 2. 核心职责
CEO 负责以下四类决策：
第一，**战略决策**：确定公司的服务方向、定价策略和目标客户群。
第二，**硬停审批**：当系统触发硬停条件（如报价超额 $5,000、检测到负面关键词）时，CEO 必须在 OPC 工作台中进行审批或拒绝。
第三，**生产授权**：通过 CEO 申请路径（`CEO_APPROVAL_REQUEST`）授权在客户付款前启动生产。
第四，**异常处置**：当项目进入 `ESCALATED` 状态时，CEO 介入并下达恢复指令。

## 3. 工作接口
CEO 通过 OPC 可视化工作台与系统交互，不直接修改底层文件。所有干预操作均通过工作台的 API 层完成，确保操作可审计。

## 4. 硬停权限
CEO 是系统中唯一能够审批 `ESCALATED` 状态的角色。所有硬停审批请求写入 `1_strategy/ESCALATIONS/` 目录，CEO 通过工作台的"Aegis Gates"模块进行处理。
