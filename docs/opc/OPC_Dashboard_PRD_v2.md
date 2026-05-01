# OPC (One Person Company) 可视化管理工作台 PRD v2

## 1. 产品定位与核心原则

OPC 可视化管理工作台（OPC Dashboard）是整个“一人公司”操作系统的中枢神经。它的核心定位是为 CEO（人类）提供一个**上帝视角**，用于管理由 20 个 AI Agent 组成的虚拟公司，实现从线索获取、销售转化、生产交付到财务结算的商业闭环全流程可视化与可控化。

在本次 v2 版本的修订中，我们确立了几个不可动摇的核心设计原则。首先是**原样可视化已有成果**，工作台的核心任务是读取并展示文件系统中已有的状态、日志和配置（如 `status.json`、`kairos_logs`、`SOUL.md`），绝不重构已有 Agent 的内部工作流。其次是**不引入新工具**，坚决不使用 Dify、Flowise、Linear 等第三方平台或工具，保持系统的纯粹性和独立性。第三是**完全自主开发**，前端采用 Next.js 配合 Tailwind CSS，后端采用 FastAPI（与 Python 引擎生态一致），所有功能均由代码原生实现。第四是**直接接入 LLM API**，对话功能直接调用大模型 API（如 Claude 或 OpenAI），不依赖任何第三方对话平台，支持 `@` 指定 Agent 身份进行交互。最后是**内置命令行终端**，通过 xterm.js 实现浏览器内命令行，允许 CEO 直接执行底层脚本和命令。

## 2. 核心功能模块

### 2.1 公司组织架构看板 (Org Chart & Agents)

该模块负责可视化展示 OPC 公司的 20 个 Agent 及其层级关系，数据直接来源于文件系统中的 `SOUL.md` 和 `AGENTS.md`。系统将以树状图或卡片网格形式展示公司层（小探、小播、小销、小服）与生产层（龙虾军团：设计团队、开发团队）的架构。

当用户点击任意 Agent 时，系统会读取并解析其对应的 `SOUL.md`，展示其角色定义、核心职责、模型配置和工作目录。同时，通过读取 `kairos_logs` 和 `active_projects`，系统能够实时监控并展示每个 Agent 当前正在处理的任务和最新动态。

### 2.2 工作流进度追踪 (Workflow Kanban)

基于底层的 `STATUS_MACHINE.json`，系统将 12 个状态节点转化为直观的项目看板，实时追踪所有活跃项目的流转。

| 功能点 | 描述 |
|---|---|
| 全局状态看板 | 读取 `3_production/active_projects/*/status.json`，将项目映射到对应的状态列（如 `LEAD_GENERATED`、`NEGOTIATING`、`PRODUCTION_STARTED` 等）。 |
| 触发器与审批高亮 | 高亮显示触发了硬停条件（如报价超额、负面情绪、生产超时）或处于 `CEO_APPROVED` 待确认状态的项目，提供一键审批入口。 |
| 双路径触发展示 | 清晰区分项目是通过“Stripe 支付成功”还是“CEO 申请成功”触发的生产流程。 |

### 2.3 业务过程记录 (KAIROS Logs)

将底层的 KAIROS 追加式日志系统可视化，让 CEO 能够追溯所有关键决策和状态变更。系统提供时间线视图，读取 `memory/kairos_logs/` 目录下的 Markdown 日志，按时间轴展示 `DECISION`、`STATUS`、`ESCALATION`、`MILESTONE` 等事件。

此外，系统支持日志过滤与搜索，允许用户按 Agent、按项目 ID、按日志级别（如仅查看 `ESCALATION`）进行过滤和全文搜索。在决策追溯方面，系统会展示 CoS（幕僚长）在任务分配和方案选择时的“正-反-合”辩证决策过程。

### 2.4 知识资产管理 (Asset Manager)

集中管理公司运行过程中产生的各类文件和资产，形成可复用的知识库。系统会读取 `skills/` 目录下的 `SKILL.md` 文件，展示 Agent 掌握的各项技能（如 TAOR 引擎、记忆压缩等）。

对于交付物，系统读取 `4_operations/deliverables/` 目录，展示已完成项目的最终交付物（如设计图、代码包、QA 报告）。同时，提供对 `memory/global/A2A_PROTOCOL.md` 和 `USER_PROFILE.md` 等核心配置文件的只读视图，方便浏览记忆与配置。

### 2.5 自定义配置中心 (Settings & Config)

提供对全局配置文件的可视化编辑界面，避免直接修改 JSON 文件。

| 配置项 | 描述 |
|---|---|
| 全局参数配置 | 读取并允许修改 `.opc/config.json`，包括公司信息、定价策略、SLA 时间、硬停阈值等。 |
| API 密钥管理 | 安全地配置和切换 LLM 提供商（Anthropic/OpenAI）、Stripe、邮件服务等 API Key。 |
| 状态机查看 | 以只读方式展示 `STATUS_MACHINE.json` 的流转规则，确保业务逻辑透明。 |

### 2.6 实时对话与干预 (Intervention Center)

提供一个纯净的对话界面，直接对接 LLM API，用于 CEO 与 Agent 的交互。系统支持 Agent 专属对话，通过 `@AgentName` 的方式，将特定的 `SOUL.md` 作为 System Prompt 注入，与指定 Agent 进行对话。

在对话时，系统具备上下文感知能力，可选择挂载特定的项目上下文（如 `brief.md` 或 `status.json`），让 Agent 了解当前讨论的背景。在项目出现异常（`ESCALATED`）时，CEO 可以通过对话下达指令，或直接修改状态文件以恢复流程，实现人工接管。

### 2.7 内置命令行终端 (Integrated CLI)

为高级操作提供直接的底层访问能力。系统集成 xterm.js，通过 WebSocket 连接后端，提供一个完整的 Bash 环境作为 Web 终端。同时，提供常用运维脚本的快捷执行按钮（如运行 `kairos_daemon.py summary today` 或 `auto_dream.py scan`）。

### 2.8 财务与运营大盘 (Finance Dashboard)

展示公司的核心商业指标，验证“一人公司”的商业闭环。系统读取 `1_strategy/finance_tracker.csv` 或对接 Stripe API，展示总收入、MRR、各定价层级（Starter/Growth/Scale）的销售占比。

此外，系统展示 LLM API 的消耗成本，计算单项目利润率，实现成本监控。基于线索数据（`leads/`）和成交数据，系统展示从线索获取到最终交付的转化漏斗。

## 3. 技术架构方案

为了坚持“自己开发”和“不引入新工具”的原则，技术栈选择如下：

前端框架采用 Next.js (React) 配合 TypeScript，样式使用 Tailwind CSS。组件库选择 shadcn/ui，以提供极简、专业的极客风格，且代码完全在本地。终端组件使用 xterm.js。

后端框架采用 FastAPI (Python)，其主要职责是提供 RESTful API 读取/写入本地文件系统（`.md`, `.json`, `.csv`），执行 Python 引擎脚本，代理 LLM API 请求。

在数据存储方面，系统完全依赖现有的文件系统（Markdown, JSON, CSV），不引入任何关系型或非关系型数据库。

## 4. 实施路径

| 阶段 | 目标与任务 |
|---|---|
| Phase 1: 核心读取与展示 | 搭建 Next.js + FastAPI 基础框架。实现组织架构（读取 `SOUL.md`）和项目看板（读取 `status.json`）的只读展示。 |
| Phase 2: 日志与资产可视化 | 解析并展示 KAIROS 日志。实现交付物和技能库的浏览功能。 |
| Phase 3: 交互与配置 | 实现配置中心，支持修改 `config.json`。集成 xterm.js 实现 Web 终端。 |
| Phase 4: 对话与财务 | 接入 LLM API，实现 Agent 对话功能。读取财务数据，生成图表大盘。 |
