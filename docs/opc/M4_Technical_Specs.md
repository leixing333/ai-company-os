# M4: OPC 10 个技术问题完整解决方案 (Technical Specs)

本模块将前期调研和架构设计中提出的 10 个核心技术问题，转化为**可执行的系统规范**。这些规范是开发 `opc-cli` 和配置 Agent 时的硬性约束。

---

## 1. Agent 身份与工作范畴定义规范
**问题**：如何确保每个 Agent 明确自己的职责边界，不越界、不遗漏？
**规范**：
- 每个 Agent 目录下必须存在一个 `AGENT_CARD.md` 文件。
- 该文件必须包含以下字段：`Role_Name`, `Identity_Description`, `Scope_of_Work`, `Input_Interfaces` (监听的目录/文件), `Output_Interfaces` (写入的目录/文件), `Permission_Boundaries` (禁止访问的目录)。
- **执行**：在启动 Agent 进程前，系统必须先读取并注入该文件作为 System Prompt 的第一部分。

## 2. Agent 间协作协议 (A2A Protocol)
**问题**：如何确保 Agent A 的输出能被 Agent B 正确消费？
**规范**：
- 废弃自然语言交接。所有跨 Agent 协作必须通过写入结构化文件完成。
- 必须在 `3_production/shared_workspace/` 下定义全局 JSON Schema（如 `BRIEF_SCHEMA.json`, `DELIVERABLE_SCHEMA.json`）。
- **执行**：接收方 Agent 在读取文件时，必须先进行 Schema 校验。如果格式错误，直接报错并打回给发送方，不进行业务处理。

## 3. 状态机与工作流跟进 (State Machine)
**问题**：CEO 如何知道一个客户订单现在在哪个环节？
**规范**：
- 每个项目目录下必须存在一个 `status.json` 文件。
- 状态流转必须是单向的（除非发生 Escalation 或客户要求修改）。
- **执行**：开发 `opc-cli status <project_id>` 命令，该命令读取 `status.json` 并以可视化进度条的形式在终端展示当前阶段、耗时和当前负责人。

## 4. 权限隔离 (Fail-closed Security)
**问题**：如何防止一个 Agent 的幻觉破坏整个项目？
**规范**：
- 实施基于目录的 Fail-closed 权限控制。
- 默认情况下，Agent 只能读写自己专属的 `workspace-{agent_name}/` 目录。
- **执行**：在底层文件读写工具（如 `file_read`, `file_write`）中加入路径拦截器。如果 Agent 尝试访问未授权的目录（如 `1_strategy/`），工具直接返回 `Permission Denied`。

## 5. 人类在环 (Human-in-the-loop)
**问题**：哪些节点需要 CEO 审核？
**规范**：
- 定义全局 `ESCALATION_TRIGGERS.json`，包含硬性拦截条件（如：金额 > $5000，退款请求，生产超时 > 48h）。
- **执行**：当触发条件满足时，系统自动将状态置为 `ESCALATED`，并在 `1_strategy/ESCALATIONS/` 生成报警文件。此时该项目的所有 Agent 进程挂起，直到 CEO 执行 `opc-cli resolve <escalation_id>`。

## 6. 记忆与自我进化 (Memory & Evolution)
**问题**：Agent 如何从过去的项目中学习？
**规范**：
- 继承龙虾军团的 KO (Knowledge Officer) 机制。
- 项目状态变为 `COMPLETED` 后，触发 KO 扫描该项目的执行轨迹。
- **执行**：KO 提取成功解决问题的 Prompt 和 Action 序列，提炼为 `SKILL.md`，存入 `3_production/global_skills/`。下次类似项目启动时，相关 Agent 会自动加载该技能。

## 7. 商业闭环的收入追踪 (Finance Tracking)
**问题**：如何追踪收入与 API 成本，计算真实利润？
**规范**：
- 在 `1_strategy/` 下维护 `finance_tracker.csv`。
- **执行**：
  - 收入端：通过 Stripe Webhook 自动追加收入记录。
  - 支出端：在底层 LLM 调用接口处，拦截 Token 消耗，按模型费率计算成本并追加记录。
  - 开发 `opc finance report` 命令，按月汇总 ROI。

## 8. 双团队交接协议 (Design-Dev Handoff)
**问题**：设计团队输出的图片/规范如何标准化传递给开发团队？
**规范**：
- 制定 `DESIGN_HANDOFF_SPEC.md`。
- 设计团队（小运）必须将最终产物按以下结构放入 `shared_workspace/design_handoffs/{Project_ID}/`：
  - `assets/` (所有导出的 PNG/SVG)
  - `tokens.json` (颜色、字体、间距的 Design Tokens)
  - `layout.md` (页面结构的 Markdown 描述)
- **执行**：FE (前端) 启动时，强制检查上述三个文件是否存在，缺失则拒绝开工。

## 9. 资源需求管理 (Resource Provisioning)
**问题**：如果需要额外资源（如 Stripe 账号、特定 API），如何管理？
**规范**：
- 当 Agent 发现缺少必要资源（如找不到 API Key）时，不允许自行伪造或停止工作。
- **执行**：Agent 必须生成一份标准化的 `RESOURCE_REQUEST.md`（包含资源名称、用途、预计成本），存入 `1_strategy/ESCALATIONS/`，触发人类在环审批。

## 10. 第一个产品的 MVP 路径 (MVP Launch Path)
**问题**：如何在最短时间内上线第一个可收费的产品？
**规范**：
- 采用"产品化 AI 设计服务"作为首个 MVP。
- 设定 72 小时极限交付 SLA（Service Level Agreement）。
- **执行**：
  - T+0h: 客户付款，生成 Brief。
  - T+12h: 设计团队完成 `design_handoffs`。
  - T+60h: 开发团队完成编码与测试。
  - T+72h: Ops 部署上线，小服发送交付邮件。
  - 任何环节超时，立即触发 Escalation 报警。

---
*本模块解决了 OPC 运行的底层技术约束。下一模块 (M5) 将给出将这一切变为现实的分阶段开发路线图。*
